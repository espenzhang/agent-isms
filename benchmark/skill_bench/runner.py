from __future__ import annotations

from pathlib import Path
import base64
import json
import mimetypes
import re
import subprocess

from .config import AppConfig
from .utils import ensure_dir, run_command, write_json


def _run_codex_task(
    app: AppConfig,
    workspace: Path,
    prompt: str,
    output_dir: Path,
    *,
    images: list[Path] | None = None,
    output_schema: dict | None = None,
) -> dict:
    ensure_dir(output_dir)
    last_message_path = output_dir / "last_message.txt"
    cfg = app.agent.codex
    import shutil as _shutil
    codex_bin = _shutil.which("codex") or "/opt/homebrew/bin/codex"
    cmd = [
        codex_bin,
        "exec",
        "--json",
        "--ephemeral",
        "--cd",
        str(workspace),
        "--sandbox",
        cfg.sandbox,
        "--output-last-message",
        str(last_message_path),
    ]
    if images:
        for image_path in images:
            cmd.extend(["--image", str(image_path)])
    if output_schema:
        schema_path = output_dir / "output_schema.json"
        schema_path.write_text(json.dumps(output_schema, indent=2) + "\n", encoding="utf-8")
        cmd.extend(["--output-schema", str(schema_path)])
    if cfg.skip_git_repo_check:
        cmd.append("--skip-git-repo-check")
    if app.agent.model:
        cmd.extend(["--model", app.agent.model])
    cmd.extend(cfg.extra_args)
    cmd.append(prompt)
    proc = run_command(cmd, cwd=workspace, timeout=app.agent.timeout_sec, check=False)
    raw_log = output_dir / "codex.jsonl"
    raw_log.write_text(proc.stdout, encoding="utf-8")
    events: list[dict] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    usage = next((event.get("usage") for event in reversed(events) if event.get("type") == "turn.completed"), None)
    result = {
        "returncode": proc.returncode,
        "usage": usage,
        "stderr": proc.stderr,
        "last_message_path": str(last_message_path),
        "last_message": last_message_path.read_text(encoding="utf-8").strip() if last_message_path.exists() else "",
    }
    try:
        result["parsed_output"] = json.loads(result["last_message"]) if result["last_message"] else None
    except json.JSONDecodeError:
        result["parsed_output"] = None
    write_json(output_dir / "agent_result.json", result)
    return result


def _run_claude_task(
    app: AppConfig,
    workspace: Path,
    prompt: str,
    output_dir: Path,
    *,
    images: list[Path] | None = None,
    output_schema: dict | None = None,
) -> dict:
    ensure_dir(output_dir)
    cfg = app.agent.claude

    if output_schema:
        schema_text = json.dumps(output_schema, indent=2)
        prompt += (
            "\n\nYou MUST respond with valid JSON matching this schema:\n"
            f"```json\n{schema_text}\n```\n"
            "Return ONLY the JSON object, no other text.\n"
        )

    # Embed images as base64 data URIs in the prompt (claude -p has no --image flag)
    if images:
        img_parts: list[str] = []
        for image_path in images:
            mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
            b64 = base64.b64encode(image_path.read_bytes()).decode()
            img_parts.append(f"![image](data:{mime};base64,{b64})")
        prompt = "\n".join(img_parts) + "\n\n" + prompt

    # Write prompt to file for debugging, pass via stdin to avoid arg length limits
    prompt_file = output_dir / "claude_prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    import shutil as _shutil
    claude_bin = _shutil.which("claude") or "/opt/homebrew/bin/claude"
    cmd = [
        claude_bin,
        "-p",
        "-",
        "--output-format", "json",
    ]
    if app.agent.model:
        cmd.extend(["--model", app.agent.model])
    cmd.extend(cfg.extra_args)
    try:
        import os as _os
        merged_env = _os.environ.copy()
        # Ensure Homebrew and common Node/tool paths are in PATH for subprocesses
        extra_paths = ["/opt/homebrew/bin", "/usr/local/bin"]
        current_path = merged_env.get("PATH", "")
        for p in extra_paths:
            if p not in current_path:
                merged_env["PATH"] = p + ":" + merged_env.get("PATH", "")
        with subprocess.Popen(
            cmd,
            cwd=str(workspace),
            env=merged_env,
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as popen:
            try:
                stdout, stderr = popen.communicate(input=prompt, timeout=app.agent.timeout_sec)
            except subprocess.TimeoutExpired:
                popen.kill()
                popen.communicate()
                raise
        proc = subprocess.CompletedProcess(cmd, popen.returncode, stdout, stderr)
    except subprocess.TimeoutExpired:
        result = {
            "returncode": -1,
            "usage": None,
            "stderr": f"Timed out after {app.agent.timeout_sec}s",
            "last_message_path": str(output_dir / "last_message.txt"),
            "last_message": "",
            "parsed_output": None,
        }
        write_json(output_dir / "agent_result.json", result)
        return result

    raw_log = output_dir / "claude.jsonl"
    raw_log.write_text(proc.stdout, encoding="utf-8")

    # Parse Claude JSON output to extract the result and usage
    last_message = ""
    usage = None
    try:
        output = json.loads(proc.stdout)
        # Claude --output-format json returns {"result": "...", "usage": {...}, ...}
        last_message = output.get("result", "")
        usage = output.get("usage")
    except (json.JSONDecodeError, TypeError):
        # Fallback: treat raw stdout as the message
        last_message = proc.stdout.strip()

    last_message_path = output_dir / "last_message.txt"
    last_message_path.write_text(last_message, encoding="utf-8")

    # Strip markdown code blocks if present (```json ... ```)
    stripped = last_message.strip()
    md_match = re.search(r"```(?:json)?\s*\n(.*?)```", stripped, re.DOTALL)
    if md_match:
        stripped = md_match.group(1).strip()

    result = {
        "returncode": proc.returncode,
        "usage": usage,
        "stderr": proc.stderr,
        "last_message_path": str(last_message_path),
        "last_message": stripped,
    }
    try:
        result["parsed_output"] = json.loads(stripped) if stripped else None
    except json.JSONDecodeError:
        result["parsed_output"] = None
    write_json(output_dir / "agent_result.json", result)
    return result


def run_agent_task(
    app: AppConfig,
    workspace: Path,
    prompt: str,
    output_dir: Path,
    *,
    images: list[Path] | None = None,
    output_schema: dict | None = None,
) -> dict:
    if app.agent.type == "claude":
        return _run_claude_task(
            app, workspace, prompt, output_dir,
            images=images, output_schema=output_schema,
        )
    return _run_codex_task(
        app, workspace, prompt, output_dir,
        images=images, output_schema=output_schema,
    )


# Backward compat alias
run_codex_task = run_agent_task
