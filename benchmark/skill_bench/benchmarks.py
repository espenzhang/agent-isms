from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
import base64
import difflib
import json
import mimetypes
import os
import re
import shutil
import subprocess
import textwrap

from datasets import load_dataset
import yaml

from .config import AppConfig, BenchmarkConfig, VariantConfig
from .utils import (
    command_exists,
    copy_tree,
    docker_env,
    ensure_dir,
    git_diff,
    git_init_repo,
    read_jsonl,
    run_command,
    stable_sample,
    write_json,
    write_jsonl,
)


@dataclass
class RunSummary:
    benchmark_id: str
    variant_id: str
    total: int
    passed: int
    failed: int
    skipped: int
    extra: dict


class BenchmarkAdapter:
    id: str

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        raise NotImplementedError

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        raise NotImplementedError


def _load_skill_content(skill_path: Path, *, include_references: bool = True) -> str:
    """Load a skill from a single file or a skill directory."""
    if skill_path.is_file():
        skill_dir = skill_path.parent
        primary_files = [skill_path]
    else:
        skill_dir = skill_path
        primary_candidates = [
            "SKILL.md",
            "AGENTS.md",
            "CLAUDE.md",
            "README.md",
            "INSTALL.md",
        ]
        primary_files = [skill_dir / name for name in primary_candidates if (skill_dir / name).exists()]

    parts: list[str] = []
    seen_paths: set[Path] = set()

    for file_path in primary_files:
        resolved = file_path.resolve()
        if resolved in seen_paths:
            continue
        seen_paths.add(resolved)
        parts.append(file_path.read_text(encoding="utf-8").strip())

    docs_dir = skill_dir / "docs"
    if docs_dir.is_dir():
        for doc_file in sorted(docs_dir.iterdir()):
            if doc_file.is_file() and doc_file.suffix in (".md", ".txt"):
                parts.append(f"[Doc: {doc_file.stem}]\n{doc_file.read_text(encoding='utf-8').strip()}")

    refs_dir = skill_dir / "references"
    if include_references and refs_dir.is_dir():
        for ref_file in sorted(refs_dir.iterdir()):
            if ref_file.is_file() and ref_file.suffix in (".md", ".txt"):
                parts.append(f"[Reference: {ref_file.stem}]\n{ref_file.read_text(encoding='utf-8').strip()}")

    return "\n\n".join(part for part in parts if part)


def render_skill_prefix(
    app: AppConfig,
    variant: VariantConfig,
    *,
    include_references: bool = True,
    max_chars: int | None = None,
) -> str:
    if not variant.skills:
        return ""
    skill_map = app.skill_map()
    blocks: list[str] = []
    for skill_id in variant.skills:
        skill = skill_map[skill_id]
        content = _load_skill_content(skill.path, include_references=include_references)
        blocks.append(f"[Skill: {skill.name}]\n{content}")
    prefix = (
        "Before starting, read and apply the following skills as working rules.\n\n"
        + "\n\n".join(blocks)
        + "\n\n"
    )
    if max_chars and len(prefix) > max_chars:
        clipped = prefix[: max_chars - 80].rstrip()
        prefix = clipped + "\n\n[Skill content truncated to fit the prompt budget.]\n\n"
    return prefix


class AiderPolyglotBenchmark(BenchmarkAdapter):
    id = "aider_polyglot"
    languages = ("cpp", "go", "java", "javascript", "python", "rust")

    def _repo_dir(self, app: AppConfig) -> Path:
        return app.paths.cache_dir / "repos" / "polyglot-benchmark"

    def _ensure_repo(self, app: AppConfig, benchmark: BenchmarkConfig) -> Path:
        repo_dir = self._repo_dir(app)
        if repo_dir.exists():
            return repo_dir
        ensure_dir(repo_dir.parent)
        run_command(
            [
                "git",
                "clone",
                "--depth",
                "1",
                benchmark.options["repo_url"],
                str(repo_dir),
            ]
        )
        return repo_dir

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        repo_dir = self._ensure_repo(app, benchmark)
        tasks: list[dict] = []
        for language in self.languages:
            practice_dir = repo_dir / language / "exercises" / "practice"
            if not practice_dir.exists():
                continue
            for exercise_dir in sorted(practice_dir.iterdir()):
                if exercise_dir.is_dir():
                    tasks.append(
                        {
                            "benchmark_id": self.id,
                            "task_id": f"{language}/{exercise_dir.name}",
                            "language": language,
                            "exercise": exercise_dir.name,
                            "source_dir": str(exercise_dir),
                        }
                    )
        sampled = stable_sample(tasks, benchmark.sample_size, benchmark.seed)
        write_jsonl(app.paths.samples_dir / f"{self.id}.jsonl", sampled)
        return sampled

    def _detect_test_commands(self, workspace: Path) -> list[list[str]]:
        commands: list[list[str]] = []
        if (workspace / "Cargo.toml").exists():
            commands.append(["cargo", "test", "--quiet"])
        if (workspace / "go.mod").exists():
            commands.append(["go", "test", "./..."])
        if (workspace / "build.gradle").exists():
            commands.append(["./gradlew", "test", "--no-daemon"])
        if (workspace / "package.json").exists():
            commands.append(["npm", "test", "--", "--runInBand"])
        if (workspace / "CMakeLists.txt").exists():
            commands.append([
                "sh",
                "-lc",
                "cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure",
            ])
        python_tests = sorted(path.name for path in workspace.iterdir() if path.name.endswith("_test.py"))
        if python_tests:
            commands.append(["python3", "-m", "pytest", "-q"])
            commands.append(["python3", "-m", "unittest", "-q", *python_tests])
        return commands

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        samples = read_jsonl(sample_path)
        run_root = ensure_dir(app.paths.runs_dir / self.id / variant.id)
        passed = failed = skipped = 0
        for sample in samples:
            task_root = ensure_dir(run_root / sample["task_id"].replace("/", "__"))
            workspace = task_root / "workspace"
            copy_tree(Path(sample["source_dir"]), workspace)
            git_init_repo(workspace)
            instructions = (workspace / ".docs" / "instructions.md").read_text(encoding="utf-8")
            append_path = workspace / ".docs" / "instructions.append.md"
            if append_path.exists():
                instructions += "\n\n" + append_path.read_text(encoding="utf-8")
            prompt = (
                render_skill_prefix(app, variant)
                + textwrap.dedent(
                    f"""
                    Solve this Exercism task in {sample["language"]}.
                    Work only inside the current workspace.
                    Do not modify tests or hidden benchmark metadata.
                    Make the implementation pass the test suite.

                    Task instructions:

                    {instructions.strip()}
                    """
                ).strip()
                + "\n"
            )
            write_json(task_root / "prompt.json", {"prompt": prompt, "sample": sample})
            from .runner import run_agent_task

            agent_result = run_agent_task(app, workspace, prompt, task_root / "agent")
            test_commands = self._detect_test_commands(workspace)
            if not test_commands:
                status = "skipped"
                test_result = {"reason": "No supported test command detected."}
                skipped += 1
            else:
                test_result = None
                status = "failed"
                for test_command in test_commands:
                    test_proc = run_command(
                        test_command,
                        cwd=workspace,
                        timeout=benchmark.options.get("test_timeout_sec", 900),
                        check=False,
                    )
                    test_result = {
                        "command": test_command,
                        "returncode": test_proc.returncode,
                        "stdout": test_proc.stdout,
                        "stderr": test_proc.stderr,
                    }
                    if test_proc.returncode == 0:
                        status = "passed"
                        break
                if status == "passed":
                    status = "passed"
                    passed += 1
                else:
                    failed += 1
            patch = git_diff(workspace)
            result = {
                "status": status,
                "sample": sample,
                "agent": agent_result,
                "test": test_result,
                "patch_path": str(task_root / "patch.diff"),
            }
            (task_root / "patch.diff").write_text(patch, encoding="utf-8")
            write_json(task_root / "result.json", result)
            if app.paths.cleanup_task_workspaces:
                shutil.rmtree(workspace, ignore_errors=True)
        summary = RunSummary(self.id, variant.id, len(samples), passed, failed, skipped, {})
        write_json(run_root / "summary.json", summary.__dict__)
        return summary


class SWEBenchBenchmark(BenchmarkAdapter):
    def __init__(self, benchmark_id: str) -> None:
        self.id = benchmark_id

    def _dataset_rows(self, dataset_name: str, split: str, offset: int, length: int) -> dict:
        query = urlencode(
            {
                "dataset": dataset_name,
                "config": "default",
                "split": split,
                "offset": offset,
                "length": length,
            }
        )
        with urlopen(f"https://datasets-server.huggingface.co/rows?{query}") as handle:
            return json.load(handle)

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        dataset_name = benchmark.options["dataset_name"]
        split = benchmark.options.get("split", "test")
        meta = self._dataset_rows(dataset_name, split, 0, 1)
        total_rows = int(meta["num_rows_total"])
        offset_rows = stable_sample(
            [{"offset": idx} for idx in range(total_rows)],
            benchmark.sample_size,
            benchmark.seed,
        )
        offsets = sorted(item["offset"] for item in offset_rows)
        sampled: list[dict] = []
        chunks: list[list[int]] = []
        current_chunk: list[int] = []
        max_span = 25
        max_items = 10
        for offset in offsets:
            if not current_chunk:
                current_chunk = [offset]
                continue
            if len(current_chunk) >= max_items or offset - current_chunk[0] >= max_span:
                chunks.append(current_chunk)
                current_chunk = [offset]
            else:
                current_chunk.append(offset)
        if current_chunk:
            chunks.append(current_chunk)
        for chunk in chunks:
            start = chunk[0]
            length = chunk[-1] - start + 1
            rows = self._dataset_rows(dataset_name, split, start, length)["rows"]
            row_map = {item["row_idx"]: item["row"] for item in rows}
            for offset in chunk:
                row = row_map[offset]
                sampled.append(
                    {
                        "benchmark_id": self.id,
                        "task_id": row["instance_id"],
                        "repo": row["repo"],
                        "instance_id": row["instance_id"],
                        "base_commit": row["base_commit"],
                        "problem_statement": row["problem_statement"],
                        "hints_text": row.get("hints_text") or "",
                        "dataset_name": dataset_name,
                        "split": split,
                    }
                )
        write_jsonl(app.paths.samples_dir / f"{self.id}.jsonl", sampled)
        return sampled

    def _prepare_repo(self, sample: dict, workspace: Path) -> None:
        ensure_dir(workspace)
        run_command(["git", "init", "-q"], cwd=workspace)
        run_command(["git", "remote", "add", "origin", f"https://github.com/{sample['repo']}.git"], cwd=workspace)
        run_command(["git", "fetch", "--depth", "1", "origin", sample["base_commit"]], cwd=workspace)
        run_command(["git", "checkout", "-q", "FETCH_HEAD"], cwd=workspace)
        run_command(["git", "config", "user.name", "skill-bench"], cwd=workspace)
        run_command(["git", "config", "user.email", "skill-bench@example.com"], cwd=workspace)

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        samples = read_jsonl(sample_path)
        run_root = ensure_dir(app.paths.runs_dir / self.id / variant.id)
        predictions: list[dict] = []
        skipped = 0
        for sample in samples:
            task_root = ensure_dir(run_root / sample["task_id"].replace("/", "__"))
            workspace = task_root / "workspace"
            self._prepare_repo(sample, workspace)
            prompt = (
                render_skill_prefix(app, variant)
                + textwrap.dedent(
                    f"""
                    You are working on a SWE-bench issue fix.
                    Work only inside the current git repository.
                    Do not modify tests unless the issue explicitly requires it.
                    Produce the smallest correct patch.

                    Issue:

                    {sample["problem_statement"].strip()}
                    """
                ).strip()
                + "\n"
            )
            if sample["hints_text"].strip():
                prompt += f"\nHelpful context:\n\n{sample['hints_text'].strip()}\n"
            write_json(task_root / "prompt.json", {"prompt": prompt, "sample": sample})
            from .runner import run_agent_task

            agent_result = run_agent_task(app, workspace, prompt, task_root / "agent")
            patch = git_diff(workspace)
            (task_root / "patch.diff").write_text(patch, encoding="utf-8")
            predictions.append(
                {
                    "instance_id": sample["instance_id"],
                    "model_name_or_path": variant.id,
                    "model_patch": patch,
                }
            )
            result = {
                "status": "generated_patch" if patch.strip() else "no_patch",
                "sample": sample,
                "agent": agent_result,
                "patch_path": str(task_root / "patch.diff"),
            }
            write_json(task_root / "result.json", result)
            if app.paths.cleanup_task_workspaces:
                shutil.rmtree(workspace, ignore_errors=True)
        predictions_path = run_root / "predictions.jsonl"
        write_jsonl(predictions_path, predictions)
        extra = {
            "predictions_path": str(predictions_path),
            "evaluation_status": "not_run",
        }
        passed = failed = 0
        if command_exists("docker"):
            report_dir = ensure_dir(run_root / "evaluation")
            report_file = app.root_dir / f"{variant.id}.{self.id}__{variant.id}.json"
            cmd = [
                "uvx",
                "--from",
                "swebench",
                "python",
                "-m",
                "swebench.harness.run_evaluation",
                "--dataset_name",
                benchmark.options["dataset_name"],
                "--split",
                benchmark.options.get("split", "test"),
                "--predictions_path",
                str(predictions_path),
                "--max_workers",
                "1",
                "--cache_level",
                "env",
                "--clean",
                "true",
                "--run_id",
                f"{self.id}__{variant.id}",
                "--report_dir",
                str(report_dir),
            ]
            proc = run_command(
                cmd,
                cwd=app.root_dir,
                timeout=benchmark.options.get("eval_timeout_sec", 172800),
                check=False,
                env=docker_env(),
            )
            extra["evaluation_status"] = "completed" if proc.returncode == 0 else "failed"
            extra["evaluation_command"] = cmd
            extra["evaluation_stdout"] = proc.stdout
            extra["evaluation_stderr"] = proc.stderr
            if report_file.exists():
                report_data = json.loads(report_file.read_text(encoding="utf-8"))
                passed = int(report_data.get("resolved_instances", 0))
                failed = int(report_data.get("unresolved_instances", 0) + report_data.get("error_instances", 0))
                extra["evaluation_report_path"] = str(report_file)
        else:
            skipped = len(samples)
            extra["evaluation_status"] = "docker_unavailable"
        summary = RunSummary(self.id, variant.id, len(samples), passed, failed, skipped, extra)
        write_json(run_root / "summary.json", summary.__dict__)
        return summary


class TerminalBenchBenchmark(BenchmarkAdapter):
    id = "terminal_bench"

    def _repo_dir(self, app: AppConfig) -> Path:
        return app.paths.cache_dir / "repos" / "terminal-bench"

    def _ensure_repo(self, app: AppConfig, benchmark: BenchmarkConfig) -> Path:
        repo_dir = self._repo_dir(app)
        if repo_dir.exists():
            return repo_dir
        ensure_dir(repo_dir.parent)
        run_command(
            [
                "git",
                "clone",
                "--depth",
                "1",
                benchmark.options["repo_url"],
                str(repo_dir),
            ]
        )
        return repo_dir

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        repo_dir = self._ensure_repo(app, benchmark)
        task_root = repo_dir / benchmark.options.get("task_root", "original-tasks")
        tasks: list[dict] = []
        for task_dir in sorted(task_root.iterdir()):
            task_yaml = task_dir / "task.yaml"
            if not task_yaml.exists():
                continue
            task = yaml.safe_load(task_yaml.read_text(encoding="utf-8"))
            tasks.append(
                {
                    "benchmark_id": self.id,
                    "task_id": task_dir.name,
                    "source_dir": str(task_dir),
                    "difficulty": task.get("difficulty", ""),
                    "category": task.get("category", ""),
                    "instruction": task.get("instruction", ""),
                }
            )
        sampled = stable_sample(tasks, benchmark.sample_size, benchmark.seed)
        write_jsonl(app.paths.samples_dir / f"{self.id}.jsonl", sampled)
        return sampled

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        samples = read_jsonl(sample_path)
        run_root = ensure_dir(app.paths.runs_dir / self.id / variant.id)
        dataset_dir = ensure_dir(run_root / "dataset")
        skill_prefix = render_skill_prefix(app, variant).strip()
        for sample in samples:
            src = Path(sample["source_dir"])
            dst = dataset_dir / sample["task_id"]
            copy_tree(src, dst)
            task_yaml_path = dst / "task.yaml"
            task_yaml = yaml.safe_load(task_yaml_path.read_text(encoding="utf-8"))
            if skill_prefix:
                task_yaml["instruction"] = f"{skill_prefix}\n\n{task_yaml['instruction']}"
            task_yaml_path.write_text(yaml.safe_dump(task_yaml, sort_keys=False), encoding="utf-8")
        extra = {"dataset_dir": str(dataset_dir)}
        if not command_exists("docker"):
            summary = RunSummary(self.id, variant.id, len(samples), 0, 0, len(samples), {"reason": "Docker unavailable", **extra})
            write_json(run_root / "summary.json", summary.__dict__)
            return summary
        tb_output_dir = ensure_dir(run_root / benchmark.options.get("tb_output_dir", "tb_runs"))
        cmd = [
            "uvx",
            "--from",
            "terminal-bench",
            "tb",
            "run",
            "--dataset-path",
            str(dataset_dir),
            "--agent",
            "codex",
            "--output-path",
            str(tb_output_dir),
            "--n-concurrent",
            str(benchmark.options.get("tb_n_concurrent", 1)),
        ]
        if benchmark.options.get("tb_cleanup", True):
            cmd.append("--cleanup")
        if app.agent.model:
            cmd.extend(["--agent-kwarg", f"model={app.agent.model}"])
        proc = run_command(
            cmd,
            cwd=app.root_dir,
            timeout=benchmark.options.get("eval_timeout_sec", 172800),
            check=False,
            env=docker_env(),
        )
        extra.update(
            {
                "tb_output_dir": str(tb_output_dir),
                "command": cmd,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": proc.returncode,
            }
        )
        summary = RunSummary(self.id, variant.id, len(samples), 0, 0, 0 if proc.returncode == 0 else len(samples), extra)
        write_json(run_root / "summary.json", summary.__dict__)
        return summary


class QABenchmark(BenchmarkAdapter):
    dataset_name: str
    dataset_config: str | None = None
    dataset_split: str = "test"

    def _load_rows(self, benchmark: BenchmarkConfig) -> list[dict]:
        kwargs = {}
        config_name = benchmark.options.get("dataset_config")
        if config_name:
            kwargs["name"] = config_name
        split = benchmark.options.get("split", self.dataset_split)
        ds = load_dataset(benchmark.options["dataset_name"], split=split, **kwargs)
        return [dict(row) for row in ds]

    def _output_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "confidence": {"type": "number"},
                "brief_explanation": {"type": "string"},
            },
            "required": ["answer", "confidence", "brief_explanation"],
            "additionalProperties": False,
        }

    def _normalize(self, value: str) -> str:
        value = value.strip().lower()
        value = value.replace("\u2019", "'")
        value = re.sub(r"\s+", " ", value)
        value = re.sub(r"[^0-9a-zA-Z\u00C0-\u024F ]+", "", value)
        return value.strip()

    def _score(self, sample: dict, answer: str) -> bool:
        return self._normalize(answer) == self._normalize(sample["answer"])

    def _build_prompt(self, app: AppConfig, variant: VariantConfig, sample: dict) -> str:
        raise NotImplementedError

    def _sample_rows(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        raise NotImplementedError

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        rows = self._sample_rows(app, benchmark)
        write_jsonl(app.paths.samples_dir / f"{self.id}.jsonl", rows)
        return rows

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        samples = read_jsonl(sample_path)
        run_root = ensure_dir(app.paths.runs_dir / self.id / variant.id)
        passed = failed = skipped = 0
        for sample in samples:
            task_root = ensure_dir(run_root / sample["task_id"].replace("/", "__"))
            result_path = task_root / "result.json"
            if result_path.exists():
                existing = json.loads(result_path.read_text(encoding="utf-8"))
                status = existing.get("status")
                if status == "passed":
                    passed += 1
                elif status == "failed":
                    failed += 1
                else:
                    skipped += 1
                continue
            workspace = ensure_dir(task_root / "workspace")
            prompt = self._build_prompt(app, variant, sample)
            write_json(task_root / "prompt.json", {"prompt": prompt, "sample": sample})
            from .runner import run_agent_task

            images = [Path(path) for path in sample.get("image_paths", [])]
            try:
                agent_result = run_agent_task(
                    app,
                    workspace,
                    prompt,
                    task_root / "agent",
                    images=images,
                    output_schema=self._output_schema(),
                )
            except Exception as exc:
                agent_result = {"returncode": -1, "usage": None, "stderr": str(exc), "last_message": "", "parsed_output": None}
                write_json(task_root / "agent" / "agent_result.json", agent_result)
            parsed = agent_result.get("parsed_output") or {}
            final_answer = (parsed.get("answer") or "").strip()
            if not final_answer:
                status = "failed"
                failed += 1
            else:
                if self._score(sample, final_answer):
                    status = "passed"
                    passed += 1
                else:
                    status = "failed"
                    failed += 1
            result = {
                "status": status,
                "sample": sample,
                "agent": agent_result,
                "final_answer": final_answer,
                "expected_answer": sample["answer"],
            }
            write_json(task_root / "result.json", result)
            if app.paths.cleanup_task_workspaces:
                shutil.rmtree(workspace, ignore_errors=True)
        summary = RunSummary(self.id, variant.id, len(samples), passed, failed, skipped, {"scoring": "local_exact_match"})
        write_json(run_root / "summary.json", summary.__dict__)
        return summary


class SimpleQAVerifiedBenchmark(QABenchmark):
    id = "simpleqa_verified"

    def _sample_rows(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        rows = self._load_rows(benchmark)
        tasks: list[dict] = []
        for row in rows:
            tasks.append(
                {
                    "benchmark_id": self.id,
                    "task_id": str(row["original_index"]),
                    "question": row["problem"],
                    "answer": row["answer"],
                    "answer_type": row["answer_type"],
                    "topic": row["topic"],
                    "requires_reasoning": bool(row["requires_reasoning"]),
                    "multi_step": bool(row["multi_step"]),
                    "urls": row.get("urls", ""),
                }
            )
        return stable_sample(tasks, benchmark.sample_size, benchmark.seed)

    def _build_prompt(self, app: AppConfig, variant: VariantConfig, sample: dict) -> str:
        return (
            render_skill_prefix(app, variant)
            + textwrap.dedent(
                f"""
                Answer the following question as accurately as possible.
                Do not use external browsing or web requests.
                Return a concise final answer only in the structured schema.

                Question:
                {sample["question"]}
                """
            ).strip()
            + "\n"
        )


class HLEBenchmark(QABenchmark):
    id = "hle"

    def _save_image(self, row: dict, image_path: Path) -> bool:
        raw_image = row.get("image") or ""
        if isinstance(raw_image, str) and raw_image.startswith("data:image/"):
            _, encoded = raw_image.split(",", 1)
            image_path.write_bytes(base64.b64decode(encoded))
            return True
        preview = row.get("image_preview")
        if preview is not None:
            preview.save(image_path)
            return True
        return False

    def _sample_rows(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        rows = self._load_rows(benchmark)
        image_dir = ensure_dir(app.paths.cache_dir / "hle_images")
        sampled_rows = stable_sample(rows, benchmark.sample_size, benchmark.seed)
        tasks: list[dict] = []
        for row in sampled_rows:
            image_path = image_dir / f"{row['id']}.png"
            has_image = image_path.exists() or self._save_image(row, image_path)
            tasks.append(
                {
                    "benchmark_id": self.id,
                    "task_id": row["id"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "answer_type": row["answer_type"],
                    "category": row["category"],
                    "raw_subject": row["raw_subject"],
                    "image_paths": [str(image_path)] if has_image else [],
                }
            )
        return tasks

    def _score(self, sample: dict, answer: str) -> bool:
        if sample["answer_type"] == "multipleChoice":
            normalized = self._normalize(answer)
            return normalized[:1] == self._normalize(sample["answer"])[:1]
        return super()._score(sample, answer)

    def _build_prompt(self, app: AppConfig, variant: VariantConfig, sample: dict) -> str:
        return (
            render_skill_prefix(app, variant)
            + textwrap.dedent(
                f"""
                Solve the following Humanity's Last Exam question.
                {'The attached image is part of the question and must be used.' if sample.get('image_paths') else 'This question has no attached image.'}
                Do not use external browsing or web requests.
                If the question includes answer choices, return only the selected choice letter(s) in the answer field.
                Otherwise, return the exact final answer as concisely as possible.

                Subject: {sample["raw_subject"]}
                Category: {sample["category"]}

                Question:
                {sample["question"]}
                """
            ).strip()
            + "\n"
        )


class MathVistaBenchmark(QABenchmark):
    id = "mathvista"

    _number_pattern = re.compile(r"[-+]?\d+(?:\.\d+)?")

    def _sample_rows(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        rows = self._load_rows(benchmark)

        # Optional: restrict to a specific task type (e.g., "math word problem")
        task_filter = benchmark.options.get("task_filter")
        if task_filter:
            rows = [
                r for r in rows
                if (r.get("metadata") or {}).get("task", r.get("task", "")) == task_filter
            ]

        image_dir = ensure_dir(app.paths.cache_dir / "mathvista_images")
        sampled_rows = stable_sample(rows, benchmark.sample_size, benchmark.seed)
        tasks: list[dict] = []
        for row in sampled_rows:
            pid = str(row["pid"])
            image_path = image_dir / f"{pid}.png"
            if not image_path.exists():
                img = row.get("decoded_image")
                if img is not None:
                    img.save(str(image_path), format="PNG")
            has_image = image_path.exists()
            metadata = row.get("metadata") or {}
            tasks.append(
                {
                    "benchmark_id": self.id,
                    "task_id": pid,
                    "question": row["question"],
                    "query": row.get("query", row["question"]),
                    "answer": str(row["answer"]),
                    "question_type": row.get("question_type", "free_form"),
                    "answer_type": row.get("answer_type", "text"),
                    "choices": row.get("choices"),
                    "precision": row.get("precision", 1.0),
                    "category": metadata.get("category", ""),
                    "task": metadata.get("task", ""),
                    "image_paths": [str(image_path)] if has_image else [],
                }
            )
        return tasks

    def _score(self, sample: dict, answer: str) -> bool:
        expected = str(sample["answer"]).strip()
        answer = answer.strip()
        qtype = sample.get("question_type", "free_form")
        atype = sample.get("answer_type", "text")

        if qtype == "multi_choice":
            choices = sample.get("choices") or []
            normalized_answer = self._normalize(answer)
            answer_letter = normalized_answer[:1]
            for idx, choice in enumerate(choices):
                normalized_choice = self._normalize(str(choice))
                if self._normalize(choice) == self._normalize(expected):
                    expected_letter = chr(ord("a") + idx)
                    if answer_letter == expected_letter or normalized_answer == normalized_choice:
                        return True
            return self._normalize(answer) == self._normalize(expected)

        if atype == "integer":
            try:
                return int(float(self._extract_number(answer))) == int(float(self._extract_number(expected)))
            except (ValueError, TypeError):
                return False

        if atype == "float":
            try:
                precision = sample.get("precision")
                digits = int(float(precision)) if precision is not None else 1
                return round(float(self._extract_number(answer)), digits) == round(float(self._extract_number(expected)), digits)
            except (ValueError, TypeError):
                return False

        return self._normalize(answer) == self._normalize(expected)

    def _extract_number(self, value: str) -> str:
        match = self._number_pattern.search(str(value))
        return match.group(0) if match else str(value)

    def _build_prompt(self, app: AppConfig, variant: VariantConfig, sample: dict) -> str:
        query = sample.get("query", sample["question"])
        return (
            render_skill_prefix(
                app,
                variant,
                include_references=False,
                max_chars=12000,
            )
            + textwrap.dedent(
                f"""
                Solve the following MathVista problem using the attached image.
                Do not browse the web or use external tools.
                Return the final answer in the JSON schema only.
                If the question has multiple choice options, answer with only the option letter (A, B, C, D, etc.).
                If the answer is numeric, answer with only the number, with no unit unless the question explicitly requires it.
                Keep the explanation brief.

                Category: {sample.get("category", "") or "unknown"}
                Task: {sample.get("task", "") or "unknown"}
                Answer type: {sample.get("answer_type", "text")}

                {query}
                """
            ).strip()
            + "\n"
        )


class DebugBenchBenchmark(BenchmarkAdapter):
    """DebugBench code repair benchmark with real test execution.

    Scoring pipeline per language:
    - Python3: generate driver → exec → compare output
    - C++: generate driver (with includes + main) → compile → exec → compare output
    - Java (no JDK): diff-based scoring against reference fix
    Fallback: if driver generation or execution fails → diff-based scoring.
    """

    id = "debugbench"
    dataset_name = "Rtian/DebugBench"
    dataset_split = "test"

    # ---- dataset / sampling ------------------------------------------------

    def _load_rows(self, benchmark: BenchmarkConfig) -> list[dict]:
        ds = load_dataset(
            benchmark.options["dataset_name"],
            split=benchmark.options.get("split", self.dataset_split),
        )
        return [dict(row) for row in ds]

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        rows = self._load_rows(benchmark)

        # Optional filters: restrict by language and/or level
        lang_filter = benchmark.options.get("language_filter")
        level_filter = benchmark.options.get("level_filter")  # e.g., "medium,hard"
        if lang_filter:
            rows = [r for r in rows if r.get("language", "") == lang_filter]
        if level_filter:
            allowed = {l.strip() for l in level_filter.split(",")}
            rows = [r for r in rows if r.get("level", "") in allowed]

        sampled = stable_sample(rows, benchmark.sample_size, benchmark.seed)
        tasks: list[dict] = []
        for row in sampled:
            def _norm(code: str) -> str:
                return "\n".join(line.rstrip() for line in code.split("\n"))
            tasks.append({
                "benchmark_id": self.id,
                "task_id": row["slug"],
                "question": row["question"],
                "buggy_code": _norm(row["buggy_code"]),
                "solution_code": _norm(row["solution"]),
                "examples": row.get("examples", []),
                "constraints": row.get("constraints", ""),
                "language": row.get("language", "unknown"),
                "category": row.get("category", ""),
                "level": row.get("level", ""),
            })
        write_jsonl(app.paths.samples_dir / f"{self.id}.jsonl", tasks)
        return tasks

    # ---- agent prompt / schema ---------------------------------------------

    def _output_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "fixed_code": {"type": "string"},
                "confidence": {"type": "number"},
                "brief_explanation": {"type": "string"},
            },
            "required": ["fixed_code", "confidence", "brief_explanation"],
            "additionalProperties": False,
        }

    def _build_prompt(self, app: AppConfig, variant: VariantConfig, sample: dict) -> str:
        examples_text = ""
        if sample.get("examples"):
            examples_text = "EXAMPLES:\n"
            for i, ex in enumerate(sample["examples"][:2], 1):
                examples_text += f"{i}. {ex}\n"
        constraints_text = ""
        if sample.get("constraints"):
            constraints_text = f"CONSTRAINTS:\n{sample['constraints']}\n"
        return (
            render_skill_prefix(app, variant, include_references=True, max_chars=12000)
            + textwrap.dedent(f"""\
You are an expert code debugger. Fix the buggy code below to solve the problem.

PROBLEM:
{sample["question"]}

{examples_text}
{constraints_text}
BUGGY CODE ({sample.get("language", "unknown")}):
```
{sample["buggy_code"]}
```

Return the FIXED code in the JSON schema only. Write complete, working code.
""")
        )

    # ---- example parsing ---------------------------------------------------

    _EXAMPLE_RE = re.compile(
        r"Input:\s*(.*?)(?=\nOutput:)"
        r".*?"
        r"Output:\s*(.*?)(?=\nExplanation:|\n(?:Note|Input:|$)|\Z)",
        re.DOTALL,
    )

    def _parse_example(self, text: str) -> tuple[dict[str, str], str] | None:
        """Parse LeetCode example → ({param: value_str}, expected_output)."""
        m = self._EXAMPLE_RE.search(text)
        if not m:
            return None
        raw_input = m.group(1).strip()
        raw_output = m.group(2).strip()
        if not raw_input or not raw_output:
            return None
        # Parse "x = val, y = val" — split on ", <word> =" but not commas inside brackets
        args: dict[str, str] = {}
        parts = re.split(r",\s*(?=\w+\s*=)", raw_input)
        for part in parts:
            eq = re.match(r"(\w+)\s*=\s*(.*)", part.strip(), re.DOTALL)
            if eq:
                args[eq.group(1)] = eq.group(2).strip()
        if not args:
            # Single unnamed arg (rare): e.g. "Input: n = 3"
            return None
        return args, raw_output

    # ---- method signature extraction ---------------------------------------

    def _find_public_method_py(self, code: str) -> tuple[str, list[str]] | None:
        """Return (method_name, [param_names]) for first non-init method."""
        for m in re.finditer(r"def\s+(\w+)\s*\(\s*self\s*[,]?\s*(.*?)\)\s*(?:->.*?)?:", code):
            name = m.group(1)
            if name.startswith("_"):
                continue
            params = [p.strip().split(":")[0].split("=")[0].strip()
                      for p in m.group(2).split(",") if p.strip()]
            return name, params
        return None

    def _find_public_method_cpp(self, code: str) -> tuple[str, str, list[tuple[str, str]]] | None:
        """Return (method_name, return_type, [(type, name)]) for public method."""
        # Strategy: find 'public:' section first; if not found, search whole class
        pub_match = re.search(r"public\s*:(.*?)(?:private\s*:|protected\s*:|\}\s*;)", code, re.DOTALL)
        # Search public section first, then fall back to whole code
        search_areas = []
        if pub_match:
            search_areas.append(pub_match.group(1))
        search_areas.append(code)

        for search_area in search_areas:
            # Collect all method candidates
            candidates = []
            for m in re.finditer(
                r"([\w<>\s,*&:]+?)\s+(\w+)\s*\(([^)]*)\)\s*(?:const\s*)?\{",
                search_area,
            ):
                ret_type = m.group(1).strip()
                name = m.group(2)
                if name in ("Solution", "if", "while", "for", "main", "helper"):
                    continue
                # Skip methods with too many params (likely private helpers)
                params_raw = m.group(3).strip()
                param_count = len([p for p in params_raw.split(",") if p.strip()]) if params_raw else 0
                candidates.append((name, ret_type, params_raw, param_count))

            # Prefer methods with fewer params (public API tends to be simpler)
            candidates.sort(key=lambda c: c[3])

            for name, ret_type, params_raw, _ in candidates:
                params: list[tuple[str, str]] = []
                if params_raw:
                    for p in params_raw.split(","):
                        p = p.strip()
                        if not p:
                            continue
                        tokens = p.replace("&", "& ").replace("*", "* ").split()
                        pname = tokens[-1] if tokens else "arg"
                        ptype = " ".join(tokens[:-1]) if len(tokens) > 1 else "int"
                        params.append((ptype.replace("  ", " "), pname))
                return name, ret_type, params
        return None

    # ---- arg matching ------------------------------------------------------

    @staticmethod
    def _match_args(param_names: list[str], args: dict[str, str]) -> dict[str, str]:
        """Match example args to method params by name, then by position."""
        # Try exact name matching first
        if all(p in args for p in param_names):
            return args
        # Fall back to positional matching
        arg_values = list(args.values())
        if len(arg_values) >= len(param_names):
            return {p: arg_values[i] for i, p in enumerate(param_names)}
        return args  # best effort

    # ---- value conversion --------------------------------------------------

    def _leetcode_val_to_py(self, val: str) -> str:
        """Convert LeetCode value string to valid Python."""
        val = val.replace("true", "True").replace("false", "False").replace("null", "None")
        return val

    def _leetcode_val_to_cpp(self, val: str, ctype: str) -> str:
        """Convert LeetCode value string to C++ initializer."""
        val = val.strip()
        ctype = ctype.strip().rstrip("& ")
        if ctype in ("int", "long", "long long", "double", "float"):
            return val
        if ctype == "bool":
            return val
        if ctype == "string":
            if val.startswith('"'):
                return val
            return f'"{val}"'
        if ctype == "char":
            if val.startswith("'"):
                return val
            return f"'{val.strip('\"')}'"
        if "vector<vector<char>>" in ctype:
            # [["a","b"],["c","d"]] → {{'a','b'},{'c','d'}}
            inner = val.replace("[", "{").replace("]", "}").replace('"', "'")
            return inner
        if "vector<vector<" in ctype:
            return val.replace("[", "{").replace("]", "}")
        if "vector<char>" in ctype:
            return val.replace("[", "{").replace("]", "}").replace('"', "'")
        if "vector<string>" in ctype:
            return val.replace("[", "{").replace("]", "}")
        if "vector<" in ctype:
            return val.replace("[", "{").replace("]", "}")
        return val

    def _leetcode_val_to_java(self, val: str, jtype: str) -> str:
        """Convert LeetCode value string to Java initializer."""
        val = val.strip()
        jtype = jtype.strip()
        if jtype in ("int", "long", "double", "float", "boolean"):
            return val
        if jtype == "String":
            if val.startswith('"'):
                return val
            return f'"{val}"'
        if jtype == "char":
            if val.startswith("'"):
                return val
            return f"'{val.strip('\"')}'"
        if jtype == "int[][]":
            return "new int[][]{" + val.replace("[", "{").replace("]", "}")[1:-1] + "}"
        if jtype == "int[]":
            return "new int[]{" + val.strip("[]") + "}"
        if jtype == "String[]":
            return "new String[]{" + val.strip("[]") + "}"
        return val

    # ---- output formatting -------------------------------------------------

    _CPP_INCLUDES = textwrap.dedent("""\
    #include <iostream>
    #include <vector>
    #include <string>
    #include <algorithm>
    #include <map>
    #include <unordered_map>
    #include <set>
    #include <unordered_set>
    #include <queue>
    #include <stack>
    #include <numeric>
    #include <cmath>
    #include <climits>
    #include <cstring>
    #include <sstream>
    #include <functional>
    using namespace std;
    """)

    _CPP_OUTPUT_HELPERS = textwrap.dedent("""\
    void _print(int v){cout<<v;}
    void _print(long long v){cout<<v;}
    void _print(bool v){cout<<(v?"true":"false");}
    void _print(double v){cout<<v;}
    void _print(const string& v){cout<<v;}
    template<class T>void _print(const vector<T>& v){
        cout<<"[";for(int i=0;i<(int)v.size();i++){if(i)cout<<",";_print(v[i]);}cout<<"]";
    }
    """)

    _JAVA_HOME = os.environ.get("JAVA_HOME", "/usr/local/jdk/Contents/Home")

    # ---- driver generation -------------------------------------------------

    def _generate_python_driver(
        self, code: str, method_name: str, param_names: list[str],
        args: dict[str, str],
    ) -> str | None:
        assignments = []
        call_args = []
        for pname in param_names:
            val = args.get(pname)
            if val is None:
                return None
            assignments.append(f"{pname} = {self._leetcode_val_to_py(val)}")
            call_args.append(pname)
        return "\n".join([
            "from typing import *",
            "import sys",
            "",
            code,
            "",
            "_sol = Solution()",
            *assignments,
            f"_result = _sol.{method_name}({', '.join(call_args)})",
            "if isinstance(_result, bool):",
            "    print(str(_result).lower())",
            "else:",
            "    print(_result)",
        ])

    def _generate_cpp_driver(
        self, code: str, method_name: str, ret_type: str,
        params: list[tuple[str, str]], args: dict[str, str],
    ) -> str | None:
        all_types = ret_type + " " + " ".join(t for t, _ in params)
        if re.search(r"TreeNode|ListNode|Node\b", all_types):
            return None
        decls = []
        call_args = []
        for ptype, pname in params:
            val = args.get(pname)
            if val is None:
                return None
            cpp_val = self._leetcode_val_to_cpp(val, ptype)
            clean_type = ptype.rstrip("& *")
            decls.append(f"    {clean_type} {pname} = {cpp_val};")
            call_args.append(pname)
        main_body = "\n".join(decls)
        return "\n".join([
            self._CPP_INCLUDES,
            code,
            "",
            self._CPP_OUTPUT_HELPERS,
            "int main(){",
            "    Solution sol;",
            main_body,
            f"    auto _r = sol.{method_name}({', '.join(call_args)});",
            "    _print(_r);",
            '    cout<<endl;',
            "    return 0;",
            "}",
        ])

    def _find_public_method_java(self, code: str) -> tuple[str, str, list[tuple[str, str]]] | None:
        """Return (method_name, return_type, [(type, name)]) for Java method."""
        candidates = []
        # Match both public and non-public methods
        for m in re.finditer(
            r"(?:public\s+)?([\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)\s*\{",
            code,
        ):
            ret_type = m.group(1)
            name = m.group(2)
            if name in ("Solution", "if", "while", "for", "main"):
                continue
            if ret_type in ("class", "interface", "new", "return", "else"):
                continue
            params_raw = m.group(3).strip()
            params: list[tuple[str, str]] = []
            param_count = 0
            if params_raw:
                for p in params_raw.split(","):
                    p = p.strip()
                    if not p:
                        continue
                    tokens = p.split()
                    if len(tokens) >= 2:
                        params.append((tokens[0], tokens[-1]))
                    param_count += 1
            is_public = "public" in code[max(0, m.start() - 20):m.start()]
            candidates.append((name, ret_type, params, param_count, is_public))
        # Prefer: public first, then fewer params
        candidates.sort(key=lambda c: (not c[4], c[3]))
        if candidates:
            name, ret_type, params, _, _ = candidates[0]
            return name, ret_type, params
        return None

    def _generate_java_driver(
        self, code: str, method_name: str, ret_type: str,
        params: list[tuple[str, str]], args: dict[str, str],
    ) -> str | None:
        all_types = ret_type + " " + " ".join(t for t, _ in params)
        if re.search(r"TreeNode|ListNode|Node\b", all_types):
            return None
        decls = []
        call_args = []
        for jtype, pname in params:
            val = args.get(pname)
            if val is None:
                return None
            java_val = self._leetcode_val_to_java(val, jtype)
            decls.append(f"        {jtype} {pname} = {java_val};")
            call_args.append(pname)
        decls_str = "\n".join(decls)
        # Output formatting
        print_expr = "result"
        if ret_type in ("int[]", "String[]"):
            print_expr = "java.util.Arrays.toString(result)"
        elif ret_type == "int[][]":
            print_expr = "java.util.Arrays.deepToString(result)"
        elif ret_type == "boolean":
            print_expr = "result"
        return "\n".join([
            "import java.util.*;",
            "import java.util.stream.*;",
            "",
            code,
            "",
            "class Main {",
            "    public static void main(String[] a) {",
            "        Solution sol = new Solution();",
            decls_str,
            f"        var result = sol.{method_name}({', '.join(call_args)});",
            f"        System.out.println({print_expr});",
            "    }",
            "}",
        ])

    # ---- compile & run -----------------------------------------------------

    def _exec_python(self, driver: str, timeout: int = 10) -> tuple[bool, str]:
        try:
            r = subprocess.run(
                ["python3", "-c", driver],
                capture_output=True, text=True, timeout=timeout,
            )
            if r.returncode != 0:
                return False, f"runtime_error: {r.stderr[:200]}"
            return True, r.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, "timeout"
        except Exception as e:
            return False, str(e)

    def _exec_cpp(self, driver: str, timeout: int = 10) -> tuple[bool, str]:
        import tempfile
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                src = Path(tmpdir) / "main.cpp"
                exe = Path(tmpdir) / "main"
                src.write_text(driver, encoding="utf-8")
                comp = subprocess.run(
                    ["g++", "-std=c++17", "-O2", str(src), "-o", str(exe)],
                    capture_output=True, text=True, timeout=15,
                )
                if comp.returncode != 0:
                    return False, f"compile_error: {comp.stderr[:300]}"
                r = subprocess.run(
                    [str(exe)], capture_output=True, text=True, timeout=timeout,
                )
                if r.returncode != 0:
                    return False, f"runtime_error: {r.stderr[:200]}"
                return True, r.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, "timeout"
        except Exception as e:
            return False, str(e)

    def _exec_java(self, driver: str, timeout: int = 15) -> tuple[bool, str]:
        import tempfile
        javac = f"{self._JAVA_HOME}/bin/javac"
        java = f"{self._JAVA_HOME}/bin/java"
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir = Path(tmpdir)
                src = tmpdir / "Main.java"
                src.write_text(driver, encoding="utf-8")
                comp = subprocess.run(
                    [javac, str(src)],
                    capture_output=True, text=True, timeout=15, cwd=tmpdir,
                )
                if comp.returncode != 0:
                    return False, f"compile_error: {comp.stderr[:300]}"
                r = subprocess.run(
                    [java, "-cp", str(tmpdir), "Main"],
                    capture_output=True, text=True, timeout=timeout, cwd=tmpdir,
                )
                if r.returncode != 0:
                    return False, f"runtime_error: {r.stderr[:200]}"
                return True, r.stdout.strip()
        except subprocess.TimeoutExpired:
            return False, "timeout"
        except Exception as e:
            return False, str(e)

    # ---- output normalization ----------------------------------------------

    def _normalize_output(self, text: str) -> str:
        """Normalize for comparison: lowercase booleans, strip quotes/spaces."""
        text = text.strip()
        text = text.replace("True", "true").replace("False", "false")
        text = text.replace("None", "null")
        # Strip all double-quotes (LeetCode wraps strings in ["Gold Medal",...])
        text = text.replace('"', "")
        # Normalize whitespace
        text = re.sub(r"\s+", "", text)
        return text

    # ---- top-level test orchestrator ---------------------------------------

    def _test_code(
        self, fixed_code: str, language: str, examples: list[str],
    ) -> tuple[bool | None, str]:
        """Test fixed code by execution. Returns (True, False, or None=skip)."""
        tested = 0
        for example in examples[:2]:
            parsed = self._parse_example(example)
            if not parsed:
                continue
            args, expected_output = parsed

            driver: str | None = None
            exec_fn = None

            if language == "python3":
                mi = self._find_public_method_py(fixed_code)
                if mi:
                    name, param_names = mi
                    matched_args = self._match_args(param_names, args)
                    driver = self._generate_python_driver(fixed_code, name, param_names, matched_args)
                    exec_fn = self._exec_python

            elif language == "cpp":
                mi = self._find_public_method_cpp(fixed_code)
                if mi:
                    name, ret, params = mi
                    pnames = [n for _, n in params]
                    matched_args = self._match_args(pnames, args)
                    driver = self._generate_cpp_driver(fixed_code, name, ret, params, matched_args)
                    exec_fn = self._exec_cpp

            elif language == "java":
                mi = self._find_public_method_java(fixed_code)
                if mi:
                    name, ret, params = mi
                    pnames = [n for _, n in params]
                    matched_args = self._match_args(pnames, args)
                    driver = self._generate_java_driver(fixed_code, name, ret, params, matched_args)
                    exec_fn = self._exec_java

            if driver is None or exec_fn is None:
                return None, "driver_gen_failed"  # None = skip (not scoreable)

            ok, actual = exec_fn(driver)
            if not ok:
                return False, f"exec_failed: {actual[:120]}"

            if self._normalize_output(actual) != self._normalize_output(expected_output):
                return False, f"output_mismatch: got={actual[:60]}, want={expected_output[:60]}"
            tested += 1

        if tested == 0:
            return None, "no_testable_examples"  # None = skip
        return True, f"test_pass({tested}_examples)"

    # ---- run variant -------------------------------------------------------

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        samples = read_jsonl(sample_path)
        run_root = ensure_dir(app.paths.runs_dir / self.id / variant.id)
        passed = failed = skipped = 0
        for sample in samples:
            task_root = ensure_dir(run_root / sample["task_id"].replace("/", "__"))
            result_path = task_root / "result.json"
            if result_path.exists():
                existing = json.loads(result_path.read_text(encoding="utf-8"))
                st = existing.get("status")
                if st == "passed":
                    passed += 1
                elif st == "failed":
                    failed += 1
                else:
                    skipped += 1
                continue

            workspace = ensure_dir(task_root / "workspace")
            prompt = self._build_prompt(app, variant, sample)
            write_json(task_root / "prompt.json", {"prompt": prompt, "sample": sample})

            from .runner import run_agent_task

            try:
                agent_result = run_agent_task(
                    app, workspace, prompt, task_root / "agent",
                    output_schema=self._output_schema(),
                )
            except Exception as exc:
                agent_result = {
                    "returncode": -1, "usage": None,
                    "stderr": str(exc), "last_message": "",
                    "parsed_output": None,
                }
                ensure_dir(task_root / "agent")
                write_json(task_root / "agent" / "agent_result.json", agent_result)

            fixed_code = (agent_result.get("parsed_output") or {}).get("fixed_code", "").strip()
            if not fixed_code:
                write_json(result_path, {"status": "failed", "scoring": "no_code"})
                failed += 1
                continue

            test_pass, test_summary = self._test_code(
                fixed_code, sample["language"], sample.get("examples", []),
            )
            if test_pass is None:
                status = "skipped"
                skipped += 1
            elif test_pass:
                status = "passed"
                passed += 1
            else:
                status = "failed"
                failed += 1

            write_json(result_path, {
                "status": status,
                "scoring": test_summary,
                "fixed_code": fixed_code[:800],
                "agent": agent_result,
            })
            if app.paths.cleanup_task_workspaces:
                shutil.rmtree(workspace, ignore_errors=True)

        summary = RunSummary(
            self.id, variant.id, len(samples), passed, failed, skipped,
            {"scoring": "test_exec+diff_fallback"},
        )
        write_json(run_root / "summary.json", summary.__dict__)
        return summary


class LocBenchBenchmark(BenchmarkAdapter):
    """Loc-Bench_V1 fault-localization benchmark.

    Evaluates file-level Acc@K: the agent must identify which files need
    editing given only the problem statement and read-only repo access.
    No patch generation — purely a localization task.
    """

    id = "locbench"

    # ---- sampling --------------------------------------------------------

    def sample(self, app: AppConfig, benchmark: BenchmarkConfig) -> list[dict]:
        rows = self._load_rows(benchmark)

        # Optional: restrict to tasks requiring at least N gold files (harder subset)
        min_gold_files = int(benchmark.options.get("min_gold_files", 1))
        if min_gold_files > 1:
            filtered = []
            for row in rows:
                edit_fns = row.get("edit_functions") or []
                gf = sorted({fn.rsplit(":", 1)[0] for fn in edit_fns if ":" in fn})
                if len(gf) >= min_gold_files:
                    filtered.append(row)
            rows = filtered

        sampled = stable_sample(rows, benchmark.sample_size, benchmark.seed)
        tasks: list[dict] = []
        for row in sampled:
            # extract file-level ground truth from edit_functions
            # format: ["path/to/file.py:func_name", ...]
            edit_fns = row.get("edit_functions") or []
            gold_files = sorted({fn.rsplit(":", 1)[0] for fn in edit_fns if ":" in fn})
            if not gold_files:
                continue
            tasks.append(
                {
                    "benchmark_id": self.id,
                    "task_id": row["instance_id"],
                    "repo": row["repo"],
                    "base_commit": row["base_commit"],
                    "problem_statement": row["problem_statement"],
                    "hints_text": row.get("hints_text") or "",
                    "gold_files": gold_files,
                    "category": row.get("category", ""),
                    "edit_functions": edit_fns,
                }
            )
        write_jsonl(app.paths.samples_dir / f"{self.id}.jsonl", tasks)
        return tasks

    def _load_rows(self, benchmark: BenchmarkConfig) -> list[dict]:
        ds = load_dataset(
            benchmark.options["dataset_name"],
            split=benchmark.options.get("split", "test"),
        )
        return [dict(row) for row in ds]

    # ---- repo cache ------------------------------------------------------

    def _prepare_repo(self, sample: dict, cache_dir: Path) -> Path:
        """Clone repo once into cache, return cached path."""
        repo_slug = sample["repo"].replace("/", "__")
        commit = sample["base_commit"]
        repo_dir = cache_dir / "locbench_repos" / repo_slug / commit
        if (repo_dir / ".git").exists():
            return repo_dir
        ensure_dir(repo_dir)
        run_command(
            ["git", "init", "-q"], cwd=repo_dir
        )
        run_command(
            ["git", "remote", "add", "origin", f"https://github.com/{sample['repo']}.git"],
            cwd=repo_dir,
        )
        run_command(
            ["git", "fetch", "--depth", "1", "origin", commit],
            cwd=repo_dir,
        )
        run_command(
            ["git", "checkout", "-q", "FETCH_HEAD"], cwd=repo_dir
        )
        return repo_dir

    # ---- output schema ---------------------------------------------------

    def _output_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Top-5 file paths most likely to need editing, ranked by confidence.",
                },
                "confidence": {"type": "number"},
                "brief_explanation": {"type": "string"},
            },
            "required": ["files", "confidence", "brief_explanation"],
            "additionalProperties": False,
        }

    # ---- scoring ---------------------------------------------------------

    @staticmethod
    def _score_file_acc(gold_files: list[str], predicted: list[str], k: int = 5) -> bool:
        """Acc@K: all gold files appear in the top-K predictions."""
        top_k = [p.strip().lstrip("/") for p in predicted[:k]]
        gold_set = {g.strip().lstrip("/") for g in gold_files}
        return gold_set.issubset(set(top_k))

    @staticmethod
    def _score_file_recall(gold_files: list[str], predicted: list[str], k: int = 5) -> float:
        """Fraction of gold files found in top-K predictions."""
        top_k = {p.strip().lstrip("/") for p in predicted[:k]}
        gold_set = {g.strip().lstrip("/") for g in gold_files}
        if not gold_set:
            return 1.0
        return len(gold_set & top_k) / len(gold_set)

    # ---- prompt ----------------------------------------------------------

    def _build_prompt(self, app: AppConfig, variant: VariantConfig, sample: dict) -> str:
        return (
            render_skill_prefix(app, variant, include_references=True, max_chars=15000)
            + textwrap.dedent(
                f"""\
You are a fault-localization expert. Given the issue below and a repository,
identify the TOP 5 files (ranked by confidence) that most likely need to be
edited to resolve the issue.

RULES:
- You may ONLY use read-only operations: list files, read files, search/grep.
- Do NOT create, modify, or delete any files.
- Do NOT generate patches.
- Return exactly 5 file paths relative to the repo root.

ISSUE:
{sample["problem_statement"]}
{("HINTS: " + sample["hints_text"]) if sample.get("hints_text") else ""}

Return your answer in the required JSON schema with the "files" array
containing exactly 5 file paths ordered from most to least likely.
"""
            )
        )

    # ---- run variant -----------------------------------------------------

    def run_variant(
        self,
        app: AppConfig,
        benchmark: BenchmarkConfig,
        variant: VariantConfig,
        sample_path: Path,
    ) -> RunSummary:
        samples = read_jsonl(sample_path)
        run_root = ensure_dir(app.paths.runs_dir / self.id / variant.id)
        passed = failed = skipped = 0
        k = int(benchmark.options.get("top_k", 5))
        for sample in samples:
            task_root = ensure_dir(run_root / sample["task_id"].replace("/", "__"))
            result_path = task_root / "result.json"
            if result_path.exists():
                existing = json.loads(result_path.read_text(encoding="utf-8"))
                status = existing.get("status")
                if status == "passed":
                    passed += 1
                elif status == "failed":
                    failed += 1
                else:
                    skipped += 1
                continue
            # prepare cached repo, symlink into workspace
            repo_dir = self._prepare_repo(sample, app.paths.cache_dir)
            workspace = task_root / "workspace"
            if not workspace.exists():
                workspace.symlink_to(repo_dir, target_is_directory=True)

            prompt = self._build_prompt(app, variant, sample)
            write_json(task_root / "prompt.json", {"prompt": prompt, "sample": sample})

            from .runner import run_agent_task

            try:
                agent_result = run_agent_task(
                    app,
                    workspace,
                    prompt,
                    task_root / "agent",
                    output_schema=self._output_schema(),
                )
            except Exception as exc:
                agent_result = {
                    "returncode": -1,
                    "usage": None,
                    "stderr": str(exc),
                    "last_message": "",
                    "parsed_output": None,
                }
                ensure_dir(task_root / "agent")
                write_json(task_root / "agent" / "agent_result.json", agent_result)

            parsed = agent_result.get("parsed_output") or {}
            predicted_files = parsed.get("files") or []
            gold_files = sample["gold_files"]
            hit = self._score_file_acc(gold_files, predicted_files, k=k)
            recall = self._score_file_recall(gold_files, predicted_files, k=k)
            status = "passed" if hit else "failed"
            if hit:
                passed += 1
            else:
                failed += 1

            result = {
                "status": status,
                "predicted_files": predicted_files[:k],
                "gold_files": gold_files,
                "recall_at_k": recall,
                "k": k,
                "agent": agent_result,
            }
            write_json(result_path, result)
        # extra metrics: mean recall
        all_results = []
        for sample in samples:
            rp = run_root / sample["task_id"].replace("/", "__") / "result.json"
            if rp.exists():
                all_results.append(json.loads(rp.read_text(encoding="utf-8")))
        recalls = [r["recall_at_k"] for r in all_results if "recall_at_k" in r]
        mean_recall = sum(recalls) / len(recalls) if recalls else 0.0
        summary = RunSummary(
            self.id,
            variant.id,
            len(samples),
            passed,
            failed,
            skipped,
            {
                "scoring": f"file_level_acc_at_{k}",
                "top_k": k,
                "mean_recall_at_k": round(mean_recall, 4),
            },
        )
        write_json(run_root / "summary.json", summary.__dict__)
        return summary


def get_benchmark_adapters() -> dict[str, BenchmarkAdapter]:
    return {
        "aider_polyglot": AiderPolyglotBenchmark(),
        "simpleqa_verified": SimpleQAVerifiedBenchmark(),
        "hle": HLEBenchmark(),
        "mathvista": MathVistaBenchmark(),
        "debugbench": DebugBenchBenchmark(),
        "locbench": LocBenchBenchmark(),
        "swebench_lite": SWEBenchBenchmark("swebench_lite"),
        "swebench_verified": SWEBenchBenchmark("swebench_verified"),
        "terminal_bench": TerminalBenchBenchmark(),
    }
