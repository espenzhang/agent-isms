from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import tomllib


@dataclass
class SkillConfig:
    id: str
    name: str
    path: Path


@dataclass
class VariantConfig:
    id: str
    name: str
    skills: list[str]


@dataclass
class PathsConfig:
    cache_dir: Path
    samples_dir: Path
    runs_dir: Path
    reports_dir: Path
    cleanup_task_workspaces: bool = True


@dataclass
class CodexConfig:
    sandbox: str = "danger-full-access"
    skip_git_repo_check: bool = True
    extra_args: list[str] = field(default_factory=list)


@dataclass
class ClaudeConfig:
    extra_args: list[str] = field(default_factory=list)


@dataclass
class AgentConfig:
    type: str = "codex"
    model: str = ""
    timeout_sec: int = 1800
    codex: CodexConfig = field(default_factory=CodexConfig)
    claude: ClaudeConfig = field(default_factory=ClaudeConfig)


@dataclass
class BenchmarkConfig:
    id: str
    enabled: bool
    sample_size: int
    seed: int
    options: dict[str, Any]


@dataclass
class AppConfig:
    config_path: Path
    root_dir: Path
    paths: PathsConfig
    agent: AgentConfig
    skills: list[SkillConfig]
    variants: list[VariantConfig]
    benchmarks: dict[str, BenchmarkConfig]

    def skill_map(self) -> dict[str, SkillConfig]:
        return {skill.id: skill for skill in self.skills}


def _resolve_path(root_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (root_dir / path).resolve()


def load_config(config_path: str | Path) -> AppConfig:
    config_path = Path(config_path).resolve()
    root_dir = config_path.parent
    raw = tomllib.loads(config_path.read_text())

    path_cfg = raw["paths"]
    paths = PathsConfig(
        cache_dir=_resolve_path(root_dir, path_cfg["cache_dir"]),
        samples_dir=_resolve_path(root_dir, path_cfg["samples_dir"]),
        runs_dir=_resolve_path(root_dir, path_cfg["runs_dir"]),
        reports_dir=_resolve_path(root_dir, path_cfg["reports_dir"]),
        cleanup_task_workspaces=path_cfg.get("cleanup_task_workspaces", True),
    )

    # Support both new [agent] section and legacy [codex] section
    agent_raw = raw.get("agent", {})
    if agent_raw:
        codex_sub = agent_raw.get("codex", {})
        claude_sub = agent_raw.get("claude", {})
        agent = AgentConfig(
            type=agent_raw.get("type", "codex"),
            model=agent_raw.get("model", ""),
            timeout_sec=int(agent_raw.get("timeout_sec", 1800)),
            codex=CodexConfig(
                sandbox=codex_sub.get("sandbox", "danger-full-access"),
                skip_git_repo_check=bool(codex_sub.get("skip_git_repo_check", True)),
                extra_args=list(codex_sub.get("extra_args", [])),
            ),
            claude=ClaudeConfig(
                extra_args=list(claude_sub.get("extra_args", [])),
            ),
        )
    elif "codex" in raw:
        # Backward compat: legacy [codex] section
        codex_raw = raw["codex"]
        agent = AgentConfig(
            type="codex",
            model=codex_raw.get("model", ""),
            timeout_sec=int(codex_raw.get("timeout_sec", 1800)),
            codex=CodexConfig(
                sandbox=codex_raw.get("sandbox", "danger-full-access"),
                skip_git_repo_check=bool(codex_raw.get("skip_git_repo_check", True)),
                extra_args=list(codex_raw.get("extra_args", [])),
            ),
        )
    else:
        agent = AgentConfig()

    skills = [
        SkillConfig(
            id=item["id"],
            name=item["name"],
            path=_resolve_path(root_dir, item["path"]),
        )
        for item in raw.get("skills", [])
    ]
    variants = [
        VariantConfig(
            id=item["id"],
            name=item["name"],
            skills=list(item.get("skills", [])),
        )
        for item in raw.get("variants", [])
    ]

    benchmarks: dict[str, BenchmarkConfig] = {}
    for benchmark_id, item in raw.get("benchmarks", {}).items():
        options = dict(item)
        enabled = bool(options.pop("enabled", True))
        sample_size = int(options.pop("sample_size", 100))
        seed = int(options.pop("seed", 42))
        benchmarks[benchmark_id] = BenchmarkConfig(
            id=benchmark_id,
            enabled=enabled,
            sample_size=sample_size,
            seed=seed,
            options=options,
        )

    return AppConfig(
        config_path=config_path,
        root_dir=root_dir,
        paths=paths,
        agent=agent,
        skills=skills,
        variants=variants,
        benchmarks=benchmarks,
    )
