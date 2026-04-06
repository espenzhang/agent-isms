# 🔴 Ideology-Driven AI Agents

**[中文版本](README_ZH.md)**

> We gave five political ideologies to an AI coding agent and ran them through real benchmarks.
> **Marxism won.** Keynesianism made things worse. Most others helped a little.

This started as a weird idea: what if the *framing* of how an agent thinks about code — the underlying worldview — actually matters? Turns out it does. More than expected.

---

## 📊 Results

### Fault Localization — 30 real GitHub issues

*Given a bug report, predict which files to edit. Pass = all correct files appear in your top-5.*

```
🥇 Marxist      ████████████████████████████████░░░░░░░░  50.0%  +6.7 pts
   Pragmatist   ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
   Taylorist    ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
   All Skills   ██████████████████████████████░░░░░░░░░░  46.7%  +3.3 pts
   ─────────────────────────────── baseline ──────────────────
   Baseline     ████████████████████████████░░░░░░░░░░░░  43.3%
   Evolutionary ████████████████████████████░░░░░░░░░░░░  43.3%
💀 Keynesian    ████████████████████████░░░░░░░░░░░░░░░░  36.7%  -6.7 pts
```

### Visual Math Reasoning — 50 problems

```
🥇 Marxist      █████████████████████████████████████████░  84.0%  +2.0 pts
   Baseline     █████████████████████████████████████████   82.0%
   (others)     █████████████████████████████████████████   82.0%
   Evolutionary ████████████████████████████████████████░   80.0%  -2.0 pts
   Taylorist    ████████████████████████████████████████░   80.0%  -2.0 pts
```

Marxism is the only framework that improves on *both* benchmarks.

Full results: [`benchmark/reports/summary.md`](benchmark/reports/summary.md)

---

## 🤔 Why Does This Work?

The Marxist skill isn't a gimmick. It maps dialectical materialism onto a concrete investigation procedure — and the mapping is surprisingly tight.

**The core rule: you cannot answer from memory.**

Where other frameworks let the agent reason from what it already knows about a library, the Marxist method makes one thing mandatory: *inspect this specific repository before you predict anything*. Run `find`. Run `grep`. Read the actual imports. Then answer.

That sounds obvious. It isn't — agents default to pattern-matching from training data, which means wrong paths, wrong file names, wrong subsystems.

Beyond that:

- **"Appearance vs. essence"** → the file where the error surfaces ≠ the file where the cause lives
- **"Trace universal connections"** → follow imports both ways; check base classes (`generic.py`), not just subclasses (`frame.py`)
- **"Find the principal contradiction"** → rank by causal proximity, not surface relevance

The Pragmatist skill helped almost as much by adding one practical rule: *prefer parent class files over subclass files*. Simple, specific, effective.

---

## 💀 Why Does Keynesianism Hurt?

The Keynesian "multiplier heuristic" — rank files by how many others import them — sounds reasonable. It isn't.

A shared utility imported by 50 modules is almost never where a specific bug lives. The more popular a file is, the *less* likely it is to be your answer. Keynesianism systematically points the agent at the wrong place, every time.

---

## 🛠️ The Skills

Each ideology is a `SKILL.md` — a structured methodology prompt you can drop into any agent.

| Skill | Core Idea | Loc-Bench |
|-------|-----------|-----------|
| [🔴 Marxist](马克思/marxist-engineering-method/SKILL.md) | Material conditions first. Find the principal contradiction. Trace connections. | **+6.7 pts** |
| [🔧 Pragmatist](实用主义/pragmatist-engineering/SKILL.md) | Translate claims into consequences. Prefer parent class files. | +3.3 pts |
| [📋 Taylorist](泰勒主义/SKILL.md) | Study before acting. Explicit step-by-step process. | +3.3 pts |
| [🧬 Evolutionary](社会达尔文主义-演化/evolutionary-execution/SKILL.md) | Verify every file path exists before including it. | ±0 pts |
| [📉 Keynesian](凯恩斯主义/keynesian-engineer/SKILL.md) | Rank by import frequency. Stimulate activity. | **-6.7 pts** |

Each skill directory has the main `SKILL.md` and a `references/` folder with the philosophical grounding.

---

## ⚡ Use a Skill Now

### Claude Code

```bash
# Copy the winning skill into your project
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

## ❌ What This Isn't

- **Not a political statement.** These are engineering methodologies that happen to have ideological names.
- **Not prompt injection magic.** The improvements come from specific investigation procedures, not vibes.
- **Not universally applicable.** On factual recall (SimpleQA) and pure code writing (SWE-bench), effects are smaller or mixed.

---

## 📂 Repo Layout

```
agent-isms/
├── 马克思/marxist-engineering-method/   Marxist skill + references
├── 实用主义/pragmatist-engineering/     Pragmatist skill
├── 凯恩斯主义/keynesian-engineer/       Keynesian skill
├── 社会达尔文主义-演化/                 Evolutionary skill
├── 泰勒主义/                           Taylorist skill
└── benchmark/
    ├── skill_bench/                    Benchmark runner (Python)
    ├── benchmark.*.toml               Config
    ├── samples/                        30–100 tasks per benchmark
    └── reports/                        summary.md, dashboard.html, leaderboard.csv
```

---

## 🙏 Inspiration

- [HughYau/qiushi-skill](https://github.com/HughYau/qiushi-skill) — the original idea that Maoist methodology translates into engineering practice

---

*Benchmarks: [Loc-Bench V1](https://huggingface.co/datasets/czlll/Loc-Bench_V1) · [MathVista](https://huggingface.co/datasets/AI4Math/MathVista) · Agent: [Claude Code](https://claude.ai/claude-code)*
