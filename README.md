# Ideology-Driven AI Agents

We gave AI agents five ideological frameworks — Marxism, Pragmatism, Keynesian Economics, Evolutionary Darwinism, and Taylorism — and measured their performance on real engineering benchmarks.

**Socialism won.**

---

## Results

### Fault Localization (Loc-Bench V1, n=30)

Given a GitHub issue, identify which files need to be edited. Scored by Acc@5: the agent predicts 5 files, and passes if every gold-standard file appears in the list.

| Rank | Ideology | Pass Rate | vs Baseline |
|------|----------|-----------|-------------|
| 🥇 1 | **Marxist Engineering** | **50.0%** | **+6.7 pts** |
| 2 | Pragmatist Engineering | 46.7% | +3.3 pts |
| 2 | Taylorist Execution | 46.7% | +3.3 pts |
| 2 | All Skills Combined | 46.7% | +3.3 pts |
| 5 | Baseline (no skill) | 43.3% | — |
| 5 | Evolutionary Execution | 43.3% | ±0.0 pts |
| 7 | Keynesian Engineer | 36.7% | **-6.7 pts** |

**4 out of 5 individual skill frameworks beat the no-skill baseline. Marxism leads by 3.3 points over the next-best ideologies.**

### Math & Visual Reasoning (MathVista, n=50)

Multimodal math reasoning — no code repositories involved, pure deduction.

| Rank | Ideology | Pass Rate | vs Baseline |
|------|----------|-----------|-------------|
| 🥇 1 | **Marxist Engineering** | **84.0%** | **+2.0 pts** |
| 2 | Baseline (no skill) | 82.0% | — |
| 2 | Keynesian Engineer | 82.0% | ±0.0 pts |
| 2 | Pragmatist Engineering | 82.0% | ±0.0 pts |
| 5 | Evolutionary Execution | 80.0% | -2.0 pts |
| 5 | Taylorist Execution | 80.0% | -2.0 pts |

**Marxism is the only framework that improves performance on both code investigation and mathematical reasoning.**

---

## Why Marxism Works

The Marxist engineering method translates dialectical materialism into a concrete investigation procedure:

1. **Start from material conditions (唯物主义)** — inspect the actual repository structure before forming any theory. Do not trust prior knowledge about how a library is organized.
2. **Trace universal connections (普遍联系)** — follow import chains in both directions; the root cause is often one step upstream or downstream from the obvious symptom file.
3. **Find the principal contradiction (主要矛盾)** — among all candidate files, identify the one that *owns* the failing mechanism, not just the one where the error surfaces.
4. **Verify with evidence** — never claim a file is responsible unless you have found it through actual search, not assumption.

The **mandatory material investigation** is the key differentiator. Where other frameworks allow the agent to reason from training-data knowledge, the Marxist method forbids it: _you must inspect this specific repository, at this specific commit, before predicting anything_.

---

## Why Most Ideologies Still Help

Fault localization is an investigation task. Any framework that structures the investigation — naming the entities to search for, specifying the order of operations, excluding noise files — tends to improve over unstructured baseline behavior.

**Pragmatism (+3.3 pts):** "Translate claims into consequences; prefer the cheapest next step" biases the agent toward concrete file searches and away from broad speculation. The rule to prefer parent class files (`generic.py`, `_base.py`) over subclass files also helps with large ORM and data-science codebases.

**Taylorism (+3.3 pts):** The instruction-card format and explicit step-by-step decomposition keep the agent on track. Scientific management, applied to file search, turns out to be efficient.

## Why Keynesianism Hurts

The Keynesian "multiplier heuristic" — prioritize files imported by many others — leads the agent toward widely-used infrastructure files rather than the specific defect location. A shared utility imported by 50 modules is almost never where the bug lives. The multiplier ranking systematically misfires on fault localization, costing 6.7 percentage points.

---

## The Skills

Each ideology is packaged as a standalone `SKILL.md` installable in Claude Code, Codex, or any agent that accepts a system prompt.

| Skill | Philosophy | Loc-Bench |
|-------|------------|-----------|
| [Marxist Engineering Method](马克思/marxist-engineering-method/SKILL.md) | Dialectical materialism: material conditions → contradiction mapping → connection tracing | **+6.7 pts** |
| [Pragmatist Engineering](实用主义/pragmatist-engineering/SKILL.md) | William James: translate claims into consequences, prefer the cheapest next step | +3.3 pts |
| [Taylorist Execution](泰勒主义/SKILL.md) | Scientific management: study before acting, explicit standards, instruction cards | +3.3 pts |
| [Evolutionary Execution](社会达尔文主义-演化/evolutionary-execution/SKILL.md) | Variation-selection-retention: generate options, select by evidence, retain gains | ±0 pts |
| [Keynesian Engineer](凯恩斯主义/keynesian-engineer/SKILL.md) | Effective demand, multiplier effects, active intervention under uncertainty | -6.7 pts |

---

## Install a Skill

### Claude Code

```bash
# Copy the winning skill to your project
cp 马克思/marxist-engineering-method/SKILL.md ./SKILL.md
```

Then reference it in your project's `CLAUDE.md`:

```markdown
@./SKILL.md
```

### Any Agent (system prompt)

Prepend the `SKILL.md` content to your system prompt. The skill files are plain Markdown with no external dependencies.

---

## Reproduce the Benchmarks

```bash
cd benchmark
uv sync

# Fault localization (runs via claude -p)
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant baseline
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant marxist_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant pragmatist_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant taylorism_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant keynesian_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant evolutionary_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant all_skills

# Generate report
uv run skill-bench report --config benchmark.locbench.toml
```

Results appear in `benchmark/reports/summary.md` and `benchmark/reports/dashboard.html`.

---

## Caveats

- **Small sample sizes** (n=30 locbench, n=50 mathvista). Results are directionally consistent but not statistically definitive.
- **Model-dependent**: All locbench runs used Claude Sonnet via `claude -p`. Results may differ on other models.
- **Task specificity**: "Marxism wins on fault localization" does not generalize to all engineering tasks. SimpleQA (factual recall) and SWE-Bench (code generation) show smaller or mixed effects.
- **Skill content matters more than label**: The improvements come from the specific investigation procedures embedded in each skill file, not from the ideology per se.

---

## Full Benchmark Results

See [`benchmark/reports/summary.md`](benchmark/reports/summary.md) for complete tables across all benchmarks.

---

*Benchmarks: [Loc-Bench V1](https://huggingface.co/datasets/czlll/Loc-Bench_V1) · [MathVista](https://huggingface.co/datasets/AI4Math/MathVista) · Agent: [Claude Code](https://claude.ai/claude-code)*
