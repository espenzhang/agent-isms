# Ideology-Driven AI Agents

**[中文版本](README_ZH.md)**

We gave AI coding agents five different ideological frameworks — Marxism, Pragmatism, Keynesianism, Evolutionary thinking, and Taylorism — as structured system prompts, then ran them through real engineering benchmarks to see what happened.

**Marxism came out on top.**

This repo contains the methodology prompts (`SKILL.md` files), the benchmark harness, and the full results.

---

## Results

### Fault Localization — Loc-Bench V1 (30 real GitHub issues)

Given a bug report, predict which files need to be changed. Passes if all gold-standard files appear in the model's top-5 predictions (Acc@5).

```
Marxist      ████████████████████████████████░░░░░░░░  50.0%  +6.7 pts  ← #1
Pragmatist   ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
Taylorist    ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
All Skills   ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
─────────────────────────────────────── baseline ──────────────────────
Baseline     ████████████████████████████░░░░░░░░░░░░  43.3%
Evolutionary ████████████████████████████░░░░░░░░░░░░  43.3%   0.0 pts
Keynesian    ████████████████████████░░░░░░░░░░░░░░░░  36.7%  -6.7 pts
```

4 out of 5 individual frameworks beat the no-skill baseline. Marxism leads by 3.3 points over the next-best.

### Visual Math Reasoning — MathVista (50 problems)

Pure multimodal reasoning, no code repositories involved.

```
Marxist      █████████████████████████████████████████░  84.0%  +2.0 pts  ← #1
All Skills   █████████████████████████████████████████   82.0%
Baseline     █████████████████████████████████████████   82.0%
Keynesian    █████████████████████████████████████████   82.0%
Pragmatist   █████████████████████████████████████████   82.0%
Evolutionary ████████████████████████████████████████░   80.0%  -2.0 pts
Taylorist    ████████████████████████████████████████░   80.0%  -2.0 pts
```

Marxism is the only framework that improves on both code investigation and mathematical reasoning.

### Other Benchmarks

| Benchmark | Best Skill | Best Score | Baseline | Notes |
|-----------|-----------|-----------|---------|-------|
| DebugBench | Taylorist | 80.0% | 76.7% | +3.3 pts |
| Aider Polyglot | (tied) | 80.0% | 80.0% | No effect; tasks too easy |
| SimpleQA | Evolutionary | 14.0% | 13.0% | Marginal; most skills hurt |
| SWE-bench Lite | Baseline/Pragmatist | 80.0% | 80.0% | Small sample (n=10) |
| HLE | — | 0.0% | 0.0% | All variants failed; too hard |

Full data: [`benchmark/reports/summary.md`](benchmark/reports/summary.md)

---

## Why Marxism Works

The Marxist engineering method translates dialectical materialism into a concrete investigation procedure:

1. **Start from material conditions (唯物主义)** — inspect the actual repository structure before forming any theory. No guessing file paths from memory or from the issue text alone.
2. **Trace universal connections (普遍联系)** — follow import chains upstream and downstream; check base classes (`generic.py`, `_base.py`), not just the subclass where the error surfaced.
3. **Find the principal contradiction (主要矛盾)** — among all candidate files, identify the one that *owns* the failing mechanism, not just the one where the symptom shows up.
4. **Verify with evidence** — never include a file unless you have found it through actual search, not assumption.

The key was making material investigation **mandatory**. Other frameworks allow the agent to answer from training-data knowledge. The Marxist method explicitly forbids it: *you must inspect this specific repository, at this specific commit, before predicting anything.*

---

## Why Most Ideologies Still Help

Fault localization is an investigation task. Any framework that structures the investigation — naming the entities to search for, specifying the order of operations, excluding noise files — tends to beat unstructured baseline behavior.

**Pragmatism (+3.3 pts):** Concrete over abstract. The rule to prefer parent class files (`generic.py`) over subclass files (`frame.py`) turns out to be practically valuable in large Python codebases.

**Taylorism (+3.3 pts):** Explicit step-by-step decomposition keeps the agent on task. Scientific management, applied to file search, is efficient.

**Keynesianism (-6.7 pts):** The multiplier heuristic — rank files by how many other files import them — systematically misfires. A widely-imported utility module is almost never where the specific bug lives.

---

## The Skills

Each is a standalone `SKILL.md` file, usable in Claude Code, Codex, or any agent that accepts a system prompt prefix.

| Skill | Directory | Core Idea | Loc-Bench |
|-------|-----------|-----------|-----------|
| Marxist Engineering | [`马克思/marxist-engineering-method/`](马克思/marxist-engineering-method/) | Material conditions first, find the principal contradiction | **+6.7 pts** |
| Pragmatist Engineering | [`实用主义/pragmatist-engineering/`](实用主义/pragmatist-engineering/) | Translate claims into consequences, prefer the cheapest next step | +3.3 pts |
| Taylorist Execution | [`泰勒主义/`](泰勒主义/) | Study before acting, explicit instruction cards | +3.3 pts |
| Evolutionary Execution | [`社会达尔文主义-演化/evolutionary-execution/`](社会达尔文主义-演化/evolutionary-execution/) | Verify every path exists before including it | ±0 pts |
| Keynesian Engineer | [`凯恩斯主义/keynesian-engineer/`](凯恩斯主义/) | Effective demand, multiplier ranking | -6.7 pts |

Each skill directory contains the main `SKILL.md` and a `references/` folder with the philosophical grounding (also included in the prompt, space permitting).

---

## Using a Skill

### Claude Code

Copy the skill into your project and reference it in `CLAUDE.md`:

```bash
cp 马克思/marxist-engineering-method/SKILL.md ./SKILL.md
```

```markdown
# CLAUDE.md
@./SKILL.md
```

### Any Agent (system prompt)

The `SKILL.md` files are plain Markdown. Prepend the content to your system prompt — no external dependencies, no special format required.

---

## Reproducing the Benchmarks

Requirements: Python 3.11+, [uv](https://github.com/astral-sh/uv), `ANTHROPIC_API_KEY` in your environment.

```bash
git clone https://github.com/your-username/methodology
cd methodology/benchmark
uv sync

# Run all variants (fault localization, ~$5–10 in API costs)
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench

# Or run a single variant
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant marxist_only

# Regenerate reports
uv run skill-bench report --config benchmark.locbench.toml
```

The runner caches per-task results — if a run is interrupted, restarting picks up where it left off.

---

## Repository Layout

```
methodology/
├── 马克思/marxist-engineering-method/      Marxist skill + philosophical references
├── 实用主义/pragmatist-engineering/        Pragmatist skill
├── 凯恩斯主义/keynesian-engineer/          Keynesian skill
├── 社会达尔文主义-演化/evolutionary-execution/  Evolutionary skill
├── 泰勒主义/                               Taylorist skill
└── benchmark/
    ├── skill_bench/                       Benchmark runner source (Python)
    ├── benchmark.*.toml                   Per-benchmark configuration
    ├── samples/                           Sampled tasks (30–100 per benchmark)
    └── reports/                           Results: summary.md, dashboard.html, leaderboard.csv
```

---

## Caveats

- **Small samples.** n=30 for locbench, n=50 for mathvista. Results are directionally consistent but not statistically conclusive.
- **Model-specific.** All runs used Claude Sonnet. Results may differ on other models or with different temperatures.
- **Task-type matters.** Marxism wins on fault localization and math reasoning. On factual recall (SimpleQA) and pure code generation (SWE-bench), effects are smaller or reversed.
- **The label is incidental.** What actually drives the improvement is the specific investigation procedure embedded in each file — not the ideological brand.

---

*Benchmarks: [Loc-Bench V1](https://huggingface.co/datasets/czlll/Loc-Bench_V1) · [MathVista](https://huggingface.co/datasets/AI4Math/MathVista) · Agent: [Claude Code](https://claude.ai/claude-code)*
