# ⚙️ Methodology-Driven AI Agents

**[中文版本](README_ZH.md)**

> Humans get better at solving problems by learning systematic ways of thinking. Does the same apply to AI agents?
> We picked five classic schools of thought, turned each into an agent prompt, and ran benchmarks to find out.
> **Marxism won.** Keynesianism made things worse. The rest helped a bit.

Turns out the reasoning framework matters — a lot. Here's the data.

---

## 📊 Results

### Fault Localization — 30 real GitHub issues

*Given a bug report, predict which files to edit. Pass = all correct files appear in your top-5.*

```
🥇 Marxist      ████████████████████████████████░░░░░░░░  50.0%  +6.7 pts
   Pragmatist   ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
   Taylorist    ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
   All Methods  ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
   ─────────────────────────────── baseline ──────────────────
   Baseline     ████████████████████████████░░░░░░░░░░░░  43.3%
   Evolutionary ████████████████████████████░░░░░░░░░░░░  43.3%
   Keynesian    ████████████████████████░░░░░░░░░░░░░░░░  36.7%  -6.7 pts
```

### Visual Math Reasoning — 50 problems

```
🥇 Marxist      █████████████████████████████████████████░  84.0%  +2.0 pts
   Baseline     █████████████████████████████████████████   82.0%
   (others)     █████████████████████████████████████████   82.0%
   Evolutionary ████████████████████████████████████████░   80.0%  -2.0 pts
   Taylorist    ████████████████████████████████████████░   80.0%  -2.0 pts
```

The Marxist method is the only one that improves on *both* benchmarks.

Full results: [`benchmark/reports/summary.md`](benchmark/reports/summary.md)

---

## 🤔 Why Does the Marxist Method Work?

It's not a gimmick. Dialectical materialism maps onto code investigation surprisingly well.

**The core rule: you cannot answer from memory.**

Where other methods let the agent reason from what it already knows about a library, the Marxist method makes one thing mandatory: *inspect this specific repository before you predict anything*. Run `find`. Run `grep`. Read the actual imports. Then answer.

That sounds obvious. It isn't — agents default to pattern-matching from training data, which means wrong paths, wrong file names, wrong subsystems.

Beyond that:

- **"Appearance vs. essence"** → the file where the error surfaces ≠ the file where the cause lives
- **"Trace universal connections"** → follow imports both ways; check base classes (`generic.py`), not just subclasses (`frame.py`)
- **"Find the principal contradiction"** → rank by causal proximity, not surface relevance

The Pragmatist method helped almost as much, via one concrete rule: *prefer parent class files over subclass files*. Simple, specific, effective.

---

## 📉 Why Does the Keynesian Method Hurt?

The Keynesian "multiplier heuristic" — rank files by how many others import them — sounds reasonable. It isn't.

A shared utility imported by 50 modules is almost never where a specific bug lives. The more popular a file is, the *less* likely it is to be your answer. The Keynesian method systematically points the agent at the wrong place, every time.

---

## 🛠️ The Methods

Each is a `SKILL.md` — a structured reasoning prompt you can drop into any agent.

| Method | Core Idea | Loc-Bench |
|--------|-----------|-----------|
| [🏆 Marxist](马克思/marxist-engineering-method/SKILL.md) | Material conditions first. Find the principal contradiction. Trace connections. | **+6.7 pts** |
| [🔧 Pragmatist](实用主义/pragmatist-engineering/SKILL.md) | Translate claims into consequences. Prefer parent class files. | +3.3 pts |
| [📋 Taylorist](泰勒主义/SKILL.md) | Study before acting. Explicit step-by-step process. | +3.3 pts |
| [🧬 Evolutionary](社会达尔文主义-演化/evolutionary-execution/SKILL.md) | Verify every file path exists before including it. | ±0 pts |
| [📉 Keynesian](凯恩斯主义/keynesian-engineer/SKILL.md) | Rank by import frequency. Stimulate activity. | **-6.7 pts** |

Each directory has the main `SKILL.md` and a `references/` folder with the philosophical grounding.

---

## ⚡ Use a Method Now

### Claude Code

```bash
# Copy the best-performing method into your project
cp 马克思/marxist-engineering-method/SKILL.md ./SKILL.md
```

Add to your `CLAUDE.md`:
```
@./SKILL.md
```

### Any Agent

The `SKILL.md` files are plain Markdown. Prepend the content to your system prompt. No dependencies, no setup.

---

## 🔬 Reproduce

Requirements: Python 3.11+, [uv](https://github.com/astral-sh/uv), `ANTHROPIC_API_KEY`.

```bash
git clone https://github.com/espenzhang/agent-isms
cd agent-isms/benchmark
uv sync

# Run fault localization (all variants, ~$5–10)
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench

# Single variant
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant marxist_only

# Report
uv run skill-bench report --config benchmark.locbench.toml
```

Interrupted runs pick up where they left off.

---

## 📂 Repo Layout

```
agent-isms/
├── 马克思/marxist-engineering-method/   Marxist method + references
├── 实用主义/pragmatist-engineering/     Pragmatist method
├── 凯恩斯主义/keynesian-engineer/       Keynesian method
├── 社会达尔文主义-演化/                 Evolutionary method
├── 泰勒主义/                           Taylorist method
└── benchmark/
    ├── skill_bench/                    Benchmark runner (Python)
    ├── benchmark.*.toml               Config
    ├── samples/                        30–100 tasks per benchmark
    └── reports/                        summary.md, dashboard.html, leaderboard.csv
```

---

## 🙏 Inspiration

- [HughYau/qiushi-skill](https://github.com/HughYau/qiushi-skill) — the original idea that classical methodology translates directly into engineering practice

---

*Benchmarks: [Loc-Bench V1](https://huggingface.co/datasets/czlll/Loc-Bench_V1) · [MathVista](https://huggingface.co/datasets/AI4Math/MathVista) · Agent: [Claude Code](https://claude.ai/claude-code)*
