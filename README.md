# Methodology

**We gave AI coding agents different ideological frameworks and benchmarked them. Marxism won.**

This repository contains 5 ideological methodologies packaged as installable skills for AI coding agents (Claude Code, OpenAI Codex), plus a benchmark harness to measure their impact.

## Leaderboard

Aggregated across 7 benchmarks (MathVista, LocBench, DebugBench, SWE-bench Lite, Aider Polyglot, SimpleQA, HLE). Only benchmarks with measurable differentiation are highlighted.

### MathVista (n=50) -- Visual Math Reasoning

| Rank | Methodology | Acc | vs Baseline |
|------|-------------|-----|-------------|
| 1 | **Marxist** | **84.0%** | **+2.0** |
| 2 | Baseline (no skill) | 82.0% | -- |
| 3 | Keynesian | 82.0% | +0.0 |
| 4 | Pragmatist | 82.0% | +0.0 |
| 5 | Evolutionary | 80.0% | -2.0 |
| 6 | Taylorist | 80.0% | -2.0 |

### LocBench (n=30) -- Fault Localization

| Rank | Methodology | Acc@5 | vs Baseline |
|------|-------------|-------|-------------|
| 1 | **Marxist** | **93.3%** | **+0.0** |
| 1 | Taylorist | 93.3% | +0.0 |
| 1 | Baseline | 93.3% | -- |
| 4 | Keynesian | 86.7% | -6.7 |
| 5 | Evolutionary | 83.3% | -10.0 |
| 5 | Pragmatist | 83.3% | -10.0 |

### DebugBench (n=30) -- Code Repair

| Rank | Methodology | Acc | vs Baseline |
|------|-------------|-----|-------------|
| 1 | Taylorist | 80.0% | +3.3 |
| 2 | **Marxist** | **76.7%** | **+0.0** |
| 2 | Baseline | 76.7% | -- |
| 4 | Keynesian | 73.3% | -3.3 |

### Cross-Benchmark Summary

| Methodology | Benchmarks Improved | Benchmarks Degraded | Net |
|-------------|--------------------|--------------------|-----|
| **Marxist** | **1** | **0** | **+1** |
| Taylorist | 1 | 1 | 0 |
| Evolutionary | 0 | 2 | -2 |
| Pragmatist | 0 | 1 | -1 |
| Keynesian | 0 | 2 | -2 |

**Marxist dialectical materialism is the only methodology that improved performance on at least one benchmark without degrading any other.** All other ideologies either had no effect or actively hurt the agent.

## Why does Marxism work?

The Marxist engineering method emphasizes:

1. **Material conditions first** -- inspect the actual repository, files, and tests before theorizing
2. **Primary contradiction** -- identify the single issue that most governs progress, don't spread effort evenly
3. **Universal connection** -- trace dependency chains and ripple effects before acting
4. **Practice-theory-practice** -- verify with execution, not just reasoning

These principles map directly to how effective debugging works: read the code, find the root cause, trace the impact, and verify the fix.

## The 5 Ideologies

| Ideology | Core Idea | SKILL.md |
|----------|-----------|----------|
| **Marxist** | Dialectical materialism: contradictions, material conditions, practice-first | [SKILL.md](马克思/marxist-engineering-method/SKILL.md) |
| **Taylorist** | Scientific management: study, standardize, measure, eliminate waste | [SKILL.md](泰勒主义/SKILL.md) |
| **Keynesian** | Macro-economic engineering: demand-driven, counter-cyclical, multiplier thinking | [SKILL.md](凯恩斯主义/keynesian-engineer/SKILL.md) |
| **Pragmatist** | William James: consequences over theory, cheapest next step, satisfice | [SKILL.md](实用主义/pragmatist-engineering/SKILL.md) |
| **Evolutionary** | Variation-selection-retention: generate options, test, keep winners | [SKILL.md](社会达尔文主义-演化/evolutionary-execution/SKILL.md) |

## Install

### Claude Code

Copy the SKILL.md file to your project:

```bash
# Install the Marxist engineering method
cp 马克思/marxist-engineering-method/SKILL.md your-project/.claude/skills/marxist.md
```

Or reference it in your CLAUDE.md:

```markdown
Use the methodology in @马克思/marxist-engineering-method/SKILL.md
```

### OpenAI Codex

Each skill includes an `agents/openai.yaml` for Codex integration:

```bash
cp 马克思/marxist-engineering-method/agents/openai.yaml your-project/.codex/agents/marxist.yaml
```

## Reproduce the Benchmarks

```bash
cd benchmark
uv sync

# Sample tasks
uv run skill-bench sample --config benchmark.toml

# Run a specific benchmark + variant
uv run skill-bench run --config benchmark.toml --benchmark mathvista --variant marxist_only

# Generate reports
uv run skill-bench report --config benchmark.toml
```

Reports are generated in `benchmark/reports/`:
- `summary.md` -- leaderboard tables
- `dashboard.html` -- interactive charts
- `leaderboard.csv` -- raw data

## Benchmarks Used

| Benchmark | Tasks | Type | Source |
|-----------|-------|------|--------|
| MathVista | 50 | Visual math reasoning | AI4Math/MathVista |
| LocBench | 30 | Fault localization (file-level) | czlll/Loc-Bench_V1 |
| DebugBench | 30 | Code repair | Rtian/DebugBench |
| SWE-bench Lite | 10 | Full software engineering | SWE-bench/SWE-bench_Lite |
| Aider Polyglot | 10 | Multi-language coding | Exercism-based |
| SimpleQA | 100 | Factual QA | google/simpleqa-verified |
| HLE | 50 | Expert-level QA | cais/hle |

## Caveats

- Sample sizes are small (10-100). Results should be interpreted as directional signals, not definitive rankings.
- The skill prefix adds ~15K tokens to each prompt. On very capable models, this overhead may matter less.
- Benchmarks used Claude Haiku and OpenAI Codex as agent backends. Results may differ with other models.
- This is an experiment in methodology-driven AI engineering, not a claim about political ideologies.

## Also included: Qiushi Protocol

The [Qiushi (Seek Truth from Facts)](求是/) protocol is a standalone coding discipline that can be installed independently. It provides investigation-first workflows, task recipes, checklists, and output templates. Not included in the benchmark comparison.

## License

MIT
