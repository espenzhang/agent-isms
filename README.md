# Ideology-Driven AI Agents

We gave AI agents five ideological frameworks — Marxism, Pragmatism, Keynesian Economics, Evolutionary Darwinism, and Taylorism — and measured their performance on real engineering benchmarks.

**One ideology consistently improved performance. The rest made things worse.**

---

## Results

### Fault Localization (Loc-Bench, n=30)

Given a GitHub issue, identify which files need to be edited. Scored by recall@5 (fraction of correct files found in top-5 predictions).

| Rank | Ideology | Recall@5 | vs Baseline |
|------|----------|----------|-------------|
| 🥇 1 | **Marxist Engineering** | **0.989** | **+0.6%** |
| 2 | Baseline (no skill) | 0.983 | — |
| 3 | Pragmatist Engineering | 0.967 | -1.7% |
| 4 | All Skills Combined | 0.922 | -6.1% |
| 5 | Evolutionary Execution | 0.906 | -7.8% |
| 6 | Keynesian Engineer | 0.900 | -8.3% |
| 7 | Taylorist Execution | 0.856 | -12.8% |

### Math & Visual Reasoning (MathVista, n=50)

Multimodal math reasoning benchmark.

| Rank | Ideology | Pass Rate | vs Baseline |
|------|----------|-----------|-------------|
| 🥇 1 | **Marxist Engineering** | **84.0%** | **+2.0%** |
| 2 | Baseline (no skill) | 82.0% | — |
| 2 | Keynesian Engineer | 82.0% | ±0.0% |
| 2 | Pragmatist Engineering | 82.0% | ±0.0% |
| 5 | Evolutionary Execution | 80.0% | -2.0% |
| 5 | Taylorist Execution | 80.0% | -2.0% |

### Summary

**Marxist methodology is the only ideology that improves performance across every benchmark we tested.** All other frameworks either have no effect or actively degrade performance.

This pattern holds across two fundamentally different task types: fault localization (investigation-heavy) and mathematical reasoning (deductive).

---

## Why Marxism Works

The Marxist engineering method translates dialectical materialism into a concrete investigation procedure:

1. **Start from material conditions** — inspect the actual repository structure before theorizing
2. **Trace universal connections (普遍联系)** — follow import chains in *both directions*; the root cause is often one step upstream from the obvious symptom
3. **Find the principal contradiction (主要矛盾)** — among all candidate files, identify the one that *owns* the failing mechanism
4. **Verify with evidence** — never claim a file is responsible unless you have read it or traced a dependency to it

Step 2 is the key differentiator. Other frameworks stop at finding the obvious file. Marxist methodology goes deeper into the dependency graph.

---

## Why Other Ideologies Hurt

**Taylorism** (-12.8% recall): The instruction-card format and step-by-step decomposition introduce overhead. Ironically, the ideology of scientific efficiency is the least efficient at investigation tasks.

**Keynesian** (-8.3%): The "multiplier heuristic" (rank files by import count) leads the agent toward widely-used utilities rather than the specific defect location.

**Evolutionary** (-7.8%): Generating multiple competing theories before searching creates cognitive overhead; the agent hedges rather than commits to the most likely root cause.

**Pragmatism** (-1.7%): Close to baseline. "Stop when you have 5 candidates" avoids over-investigation but occasionally stops before tracing necessary dependency chains.

---

## The Skills

Each ideology is packaged as a standalone `SKILL.md` — installable in Claude Code, Codex, or any agent that accepts a system prompt.

| Skill | Philosophy |
|-------|------------|
| [Marxist Engineering Method](马克思/marxist-engineering-method/SKILL.md) | Dialectical materialism: material conditions → contradiction mapping → connection tracing |
| [Pragmatist Engineering](实用主义/pragmatist-engineering/SKILL.md) | William James: translate claims into consequences, prefer the cheapest next step |
| [Keynesian Engineer](凯恩斯主义/keynesian-engineer/SKILL.md) | Effective demand, multiplier effects, active intervention under uncertainty |
| [Taylorist Execution](泰勒主义/SKILL.md) | Scientific management: study before acting, explicit standards, instruction cards |
| [Evolutionary Execution](社会达尔文主义-演化/evolutionary-execution/SKILL.md) | Variation-selection-retention: generate options, select by evidence, retain gains |
| [求是 / Qiushi](求是/AGENTS.md) | Seek truth from facts: investigate first, identify the primary contradiction |

---

## Install a Skill

### Claude Code

Add to your project's `CLAUDE.md` (or use as a standalone system prompt):

```bash
# Option 1: Copy the skill file
cp 马克思/marxist-engineering-method/SKILL.md ./CLAUDE.md

# Option 2: Reference it from an existing CLAUDE.md
echo "\n@./marxist-engineering-method/SKILL.md" >> CLAUDE.md
```

### Codex / OpenAI Agents

Prepend the `SKILL.md` content to your system prompt, or reference via `agents/openai.yaml`.

---

## Reproduce the Benchmarks

```bash
cd benchmark
uv sync

# Fault localization (uses Claude Haiku via claude -p)
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant baseline
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant marxist_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant taylorism_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant keynesian_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant pragmatist_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant evolutionary_only
uv run skill-bench run --config benchmark.locbench.toml --benchmark locbench --variant all_skills

# Math reasoning (uses Codex)
uv run skill-bench run --config benchmark.toml --benchmark mathvista --variant marxist_only

# Generate combined report
uv run skill-bench report --config benchmark.toml
```

Results appear in `benchmark/reports/summary.md` and `benchmark/reports/dashboard.html`.

---

## Caveats

- **Small sample sizes** (n=30 locbench, n=50 mathvista). Treat results as preliminary signal, not statistically definitive proof.
- **Model-dependent**: Locbench runs used Claude Haiku; MathVista used Codex. Results will vary on other models.
- **Ceiling effects**: Claude Haiku achieves 96.7% Acc@5 on locbench *without any skill*. The recall@5 metric reveals finer differentiation.
- **Not a universal claim**: "Marxism wins" applies to structured investigation tasks. Different task types may favor different methodologies.

---

## Contributing

PRs welcome for:
- New ideology-based skills (Austrian economics? Confucianism? Stoicism?)
- Additional benchmark families
- Larger sample runs or statistical significance tests
- Runs on different base models

The benchmark harness (`benchmark/`) supports adding new skills and variants in a single `benchmark.toml` edit.

---

*Benchmarks: [Loc-Bench V1](https://huggingface.co/datasets/czlll/Loc-Bench_V1) · [MathVista](https://huggingface.co/datasets/AI4Math/MathVista) · Agent: [Claude Code](https://claude.ai/claude-code)*
