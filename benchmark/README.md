# Skill Benchmark Harness

This repository contains a lightweight, storage-aware benchmark harness for
measuring how much a set of Codex skills improves agent performance.

It supports:

- Aider Polyglot: sampled locally from the official Exercism-based repository.
- SWE-bench Lite / Verified: sampled from the official Hugging Face datasets.
- Terminal-Bench: sampled from the official task repository and executed through
  the official `tb` CLI when Docker is available.
- SimpleQA Verified / HLE: text-first QA benchmarks sampled from Hugging Face.
- MathVista: multimodal math and visual reasoning sampled from Hugging Face and
  evaluated locally with image attachments.

## Design goals

- Keep disk usage small by sampling first and materializing tasks lazily.
- Reuse the same agent runner across baseline and skill variants.
- Save raw logs, patches, prompts, and machine-readable summaries.
- Let heavy benchmarks degrade gracefully when Docker is unavailable.

## Quick start

1. Sync dependencies:

```bash
uv sync
```

2. Review and edit the config:

```bash
sed -n '1,240p' benchmark.toml
```

3. Generate a sampled benchmark plan:

```bash
uv run skill-bench sample --config benchmark.toml
```

4. Run one benchmark family:

```bash
uv run skill-bench run --config benchmark.toml --benchmark aider_polyglot
```

5. Build a combined report:

```bash
uv run skill-bench report --config benchmark.toml
```

## Docker notes

`SWE-bench` and `Terminal-Bench` require Docker. On this machine the harness is
configured to work with `colima`, and the evaluation layer exports
`DOCKER_HOST=unix://~/.colima/default/docker.sock` automatically when
calling Docker-based backends.

Useful checks:

```bash
docker info
docker compose version
colima status
```

## Notes

- `Aider Polyglot` can run fully locally if the language toolchains are
  installed.
- `SWE-bench` uses `codex exec` to generate patches, then optionally calls the
  official `swebench.harness.run_evaluation` command if Docker is installed.
- `Terminal-Bench` uses the official `tb run` CLI and is only enabled for full
  execution when Docker is installed.
- `MathVista` attaches cached images to the agent prompt and uses benchmark-
  specific local answer normalization for multiple-choice and numeric questions.
- To save disk, the harness clones repositories shallowly, fetches exact commits
  for SWE-bench instances, and can delete per-task workspaces after each run.

## Key outputs

- `samples/<benchmark>.jsonl`: sampled task metadata.
- `runs/<benchmark>/<variant>/...`: per-task artifacts and summaries.
- `reports/summary.json`: aggregate report across all benchmarks and variants.
- `reports/summary.md`: quick human-readable leaderboard.
- `reports/leaderboard.csv`: flat table for spreadsheets or notebooks.
- `reports/dashboard.html`: local dashboard with charts and ranking tables.
