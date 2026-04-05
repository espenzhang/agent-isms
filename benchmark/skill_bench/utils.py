from __future__ import annotations

from pathlib import Path
from typing import Iterable
import json
import os
import random
import shlex
import shutil
import subprocess


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def run_command(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: int | None = None,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    with subprocess.Popen(
        args,
        cwd=str(cwd) if cwd else None,
        env=merged_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as proc:
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            raise
    completed = subprocess.CompletedProcess(args, proc.returncode, stdout, stderr)
    if check and completed.returncode != 0:
        raise RuntimeError(
            f"Command failed ({completed.returncode}): {shlex.join(args)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def write_json(path: Path, payload: object) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def stable_sample(items: list[dict], size: int, seed: int) -> list[dict]:
    if size >= len(items):
        return list(items)
    rng = random.Random(seed)
    return rng.sample(items, size)


def copy_tree(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst, dirs_exist_ok=True)


def git_init_repo(path: Path) -> None:
    run_command(["git", "init", "-q"], cwd=path)
    run_command(["git", "config", "user.name", "skill-bench"], cwd=path)
    run_command(["git", "config", "user.email", "skill-bench@example.com"], cwd=path)
    run_command(["git", "add", "."], cwd=path)
    run_command(["git", "commit", "-q", "-m", "baseline"], cwd=path)


def git_diff(path: Path) -> str:
    return run_command(["git", "diff", "--binary"], cwd=path, check=False).stdout


def shell_join(args: list[str]) -> str:
    return shlex.join(args)


def docker_env() -> dict[str, str]:
    candidates = [
        Path.home() / ".colima" / "default" / "docker.sock",
        Path.home() / ".colima" / "docker.sock",
    ]
    for candidate in candidates:
        if candidate.exists():
            value = f"unix://{candidate}"
            return {
                "DOCKER_HOST": value,
                "TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE": str(candidate),
            }
    return {}
