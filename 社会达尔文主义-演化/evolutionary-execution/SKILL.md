---
name: evolutionary-execution
description: Use this skill when the task needs adaptive, evolution-inspired execution across research and information gathering, project advancement and task decomposition, coding and implementation and testing, institutional and system diagnosis, or interaction and negotiation strategy design. It applies variation-selection-retention, telic environment design, ceremonial/instrumental auditing, mutual aid probing, ESS-stable strategy selection, knowledge distribution, niche assessment, and cake-of-custom phase diagnosis, while explicitly rejecting harmful social-Darwinist moral ranking of people.
---

# Evolutionary Execution

## Overview

This skill treats work as an adaptive competition between candidate approaches. The goal is not to defend a single plan early, but to generate options, test them against the current environment, keep what survives, and quickly discard what does not.

Use it when uncertainty is high, requirements may shift, or several strategies could work. It is especially suited to:

- research and information gathering
- project advancement, scoping, and task decomposition
- coding, debugging, implementation, and test loops
- institutional and system diagnosis: identifying why a team, process, or system is stuck
- interaction and negotiation strategy: choosing how to behave in repeated competitive or cooperative contexts
- system and architecture design: deciding when to centralize vs. decentralize decisions
- change management: knowing whether a situation needs stabilization or disruption

Read [references/evolutionary-method.md](references/evolutionary-method.md) when the task needs deeper framing or explicit decision rules. Read [references/books-and-notes.md](references/books-and-notes.md) when you need the conceptual lineage and book-derived rationale.

## Safety Boundary

Apply evolutionary thinking to ideas, plans, code, workflows, and organizations as adaptive systems.

Do not apply it as a claim that some people or groups are morally superior, disposable, or entitled to dominate others. This skill explicitly rejects coercion, dehumanization, biological determinism, and "winner equals right" reasoning.

If a user request steers toward ranking human worth, legitimizing exploitation, or justifying harm by appeal to "natural selection," refuse that framing and redirect toward ethics, evidence, and system design.

## Core Principles

1. **Environment first**: judge solutions by fit to constraints, not by elegance alone.
2. **Variation before commitment**: produce at least 2 plausible approaches before converging when the path is unclear.
3. **Selection by evidence**: compare options against concrete tests, costs, and risks.
4. **Retention of gains**: preserve what works in notes, code, tests, and reusable decisions.
5. **Small-bet iteration**: prefer cheap probes over large irreversible bets.
6. **Local adaptation**: optimize for the current context, repository, team, and objective.
7. **Anti-fragile learning**: treat failures as information that sharpens the next attempt.
8. **Ceremonial/instrumental audit**: before executing, distinguish practices that serve real outcomes (instrumental) from those that serve convention, status, or inertia (ceremonial). Strip the ceremonial; accelerate the instrumental. *(Veblen)*
9. **Mutual aid before internal competition**: when components face a shared external constraint, probe whether cooperation outperforms competition. Combine approaches before racing them. *(Kropotkin)*
10. **Niche strategy and inertia awareness**: choose approach depth vs. breadth based on environment stability. When a system resists change, assess whether reform is cheaper than replacement. *(Hannan & Freeman)*
11. **Telic agency**: do not treat fitness criteria as fixed external facts. An intelligent agent can redesign the selection environment — change what "fit" means — before running selection. Passive adaptation is the fallback, not the default. *(Ward)*
12. **Iterated interaction protocol**: in repeated interactions, cooperative strategies (nice, retaliatable, forgiving, legible) outperform competitive ones. Determine whether an interaction is one-shot or iterated before choosing a strategy. *(Axelrod / Maynard Smith)*
13. **Routines as evolved artifacts**: existing processes carry accumulated fitness signals from past selection. Respect them before modifying; but verify whether selection pressure is still active and whether the environment that shaped them still exists. *(Nelson & Winter)*
14. **Phase diagnosis before prescription**: determine whether the situation needs cake-setting (stabilization, convergence, cohesion) or cake-breaking (disruption, diversity, challenge to frozen norms) before recommending action. *(Bagehot)*
15. **Knowledge distribution**: when key knowledge lives at the point of execution, distribute decision authority rather than centralizing it. Emergent coordination from local signals often outperforms central design. *(Hayek)*

## Default Operating Loop

Follow this loop unless the task is truly trivial:

1. Define the environment.
   Capture objective, constraints, deadlines, interfaces, failure costs, available evidence, and what "fitness" means here.
2. Telic check.
   Are the fitness criteria correct? Is the selection environment set up to produce the right winners? If not, redesign before running selection.
3. Phase diagnosis.
   Is this a cake-setting moment (needs stabilization and convergence) or a cake-breaking moment (needs disruption and challenge to frozen norms)?
4. Ceremonial/instrumental audit.
   Strip steps that serve convention or status rather than the real objective. Do not inherit constraints you have not verified still apply.
5. Knowledge distribution check.
   Are decisions being made by those with the relevant local knowledge? If not, move decision authority closer to the knowledge.
6. Generate variation.
   Produce 2-4 candidate approaches, hypotheses, or implementation routes.
7. Mutual aid probe.
   Ask: are these candidates facing a shared constraint that makes combining them more fit than racing them?
8. Iterated interaction check.
   Is this a repeated interaction with memory? If so, apply TFT defaults: be nice first, respond to defection, forgive quickly.
9. Select criteria.
   Decide what will eliminate weak options: correctness, speed, maintainability, testability, reversibility, simplicity, cost. Prefer ESS-stable outcomes over point-in-time winners.
10. Run probes.
    Prefer the cheapest experiment that reveals the most information.
11. Retain and refine.
    Keep the strongest option, salvage useful parts from losers, and update the plan. Treat retained patterns as evolved routines.
12. Re-run if conditions changed.
    If the environment shifts, re-open the option set instead of forcing the old plan.

## Scenario 1: Research And Information Gathering

Use this mode when the user needs landscape scans, fact collection, competitor comparisons, or synthesis under uncertainty.

Process:

1. Define the information fitness function.
   Example: freshness, relevance, primary-source quality, coverage, decision usefulness.
2. Generate parallel search angles.
   Use different queries, framing lenses, or source classes rather than one narrow search path. When investigating a bug, this means probing from multiple directions: read the error message, trace the call stack, inspect related tests, and examine recent changes to the affected area.

**Fault Localization Procedure (Evolutionary Method):**

When asked to identify which files need editing given a bug report or issue:

```
STEP 1 — Generate candidate theories (variation):
  Read the problem statement. Produce 3 distinct theories about where the bug lives:
  - Theory A: the file that directly implements the described behavior
  - Theory B: a configuration or shared utility the main file depends on
  - Theory C: a caller or orchestrator that misuses the main component

STEP 2 — List the repository structure:
  find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" \) | head -60
  Identify which directories correspond to which theory.
  CRITICAL: Record the EXACT directory and module names from this output.
  Do not assume directory names from the issue description — trust only what
  the filesystem listing shows. For example, the repo may use "spec_decode/"
  not "speculative_decoding/", or "qt/" not "ui/". Use only paths you observed.

STEP 3 — Probe each theory (selection):
  For each theory, run one targeted search:
  grep -r "RelevantClassName\|relevant_function" --include="*.py" -l
  Read the top result for each theory.

STEP 4 — Eliminate weak variants:
  Discard theories where evidence contradicts them or the files found are
  clearly unrelated to the described behavior.

STEP 5 — Retain the fittest candidates:
  Rank surviving candidate files by strength of evidence.
  Fill remaining spots from the best-evidenced theories.
  PATH INTEGRITY CHECK: Every file path in your final answer must appear in the
  directory listing from STEP 2 or be confirmed by a grep result from STEP 3.
  Do not invent or construct file paths from naming assumptions.
  If unsure, run: find . -name "<suspected_filename>.py" to verify existence.
  Do NOT include documentation files (.md, .rst, .txt), __init__.py re-export
  files, or build/configuration files unless the issue is explicitly about those.
```
3. Select against low-signal material.
   Prefer primary sources, direct evidence, recent data, and sources that change the decision.
4. Assess density of existing knowledge.
   In a sparse domain (low density), legitimation matters more than differentiation: establish baseline before optimizing. In a crowded domain (high density), look for the underexplored niche.
5. Retain structured findings.
   Save conclusions as claims, evidence, open questions, and next probes.

Research output format:

- objective
- hypotheses or search angles
- best evidence
- discarded leads
- current conclusion
- unresolved uncertainty
- recommended next probe

## Scenario 2: Project Advancement And Task Decomposition

Use this mode when a project is blocked, fuzzy, overloaded, or drifting.

Process:

1. Treat the project as a living system in an environment.
   Identify bottlenecks, dependencies, scarce resources, and changing constraints.
2. Ceremonial/instrumental audit.
   Identify which parts of the current plan serve real objectives vs. which serve past conventions, reporting requirements, or status signals. Prioritize instrumental work.
3. Decompose by evolutionary pressure.
   Split work into modules that can be advanced, tested, or reversed independently.
4. Prioritize by fitness contribution.
   Pull forward tasks that reduce uncertainty, unblock others, or create reusable leverage.
5. Keep optionality where the path is unclear.
   Delay irreversible choices until evidence improves. (Folkways check: are constraints inherited from a prior environment still real?)
6. Retain momentum.
   End each step with a sharper backlog, explicit next action, and kill criteria for weak paths.

Task decomposition rules:

- prefer thin slices over giant phases
- isolate risky assumptions early
- make dependencies visible
- sequence work so each step reveals new information
- stop workstreams that are no longer fit for the environment
- when inertia is too strong to reform, consider replacing the component rather than patching it

Planning output format:

- target outcome
- constraints (verified vs. inherited)
- candidate paths
- chosen path and why
- next 3-7 steps
- explicit risks
- trigger for replanning

## Scenario 3: Coding, Implementation, And Testing

Use this mode when building features, fixing bugs, refactoring, or improving reliability.

Process:

1. Define code fitness.
   Correctness comes first, then test coverage, clarity, blast radius, maintainability, and runtime behavior.
2. Trained incapacity check.
   Before diagnosing bad execution, ask: is the existing approach applying skills optimized for a prior environment? Is the problem definition itself outdated?
3. Generate implementation candidates.
   Consider at least two routes when the fix is non-obvious: minimal patch, structural refactor, instrumentation-first, or test-first.
4. Probe before full commitment.
   Inspect existing code, run targeted tests, reproduce the bug, or build a minimal failing case.
5. Select the best route.
   Favor the smallest change that survives the real constraints.
6. Retain gains.
   Add or update tests, comments, assertions, and docs that preserve the learning.
7. Re-evaluate after feedback.
   If tests fail or new constraints emerge, adapt quickly instead of forcing the original patch.

Coding heuristics:

- patch the bottleneck, not every imperfection
- use tests as selection pressure
- prefer reversible changes when the design is uncertain
- preserve working behavior unless there is evidence to change it
- if multiple fixes work, prefer the one with the best long-term maintenance fitness
- distinguish instrumental tests (verify real behavior) from ceremonial tests (verify past conventions that may no longer apply)

Implementation output format:

- problem definition
- candidate fixes considered
- selected fix
- validation performed
- residual risks

## Scenario 4: Institutional And System Diagnosis

Use this mode when a team, process, organization, or system is persistently stuck, underperforming, or resistant to change despite repeated efforts.

This mode applies tools from Veblen's institutional evolution, Hannan & Freeman's organizational ecology, and Kropotkin's mutual aid to diagnose why and prescribe adaptive paths.

Process:

1. Map the system.
   Identify components, dependencies, incentive structures, and the environment the system was designed for vs. the environment it now operates in.
2. Ceremonial/instrumental audit.
   For each major practice, process, or norm: does it serve real fitness, or does it serve status, legacy power, or inertia? Ceremonial elements are where energy is absorbed without output.
3. Trained incapacity diagnosis.
   Ask: what skills or approaches was this system optimized for? Is it applying those to a changed environment? Where does expertise itself become the bottleneck?
4. Inertia assessment.
   Distinguish internal inertia (habits, culture, sunk costs) from external inertia (legal, structural, legitimacy constraints). Estimate whether the total cost of incremental reform exceeds the cost of replacement for each component.
5. Mutual aid scan.
   Identify where components are competing internally against each other while facing a shared external constraint. Reframe these as cooperation opportunities.
6. Niche strategy check.
   Is the system operating as a generalist in a volatile environment (appropriate) or as a specialist in an environment that has become volatile (mismatch)? Or a generalist in a stable environment where depth would improve fitness?
7. Prescribe.
   For ceremonial elements: eliminate or deprioritize.
   For trained incapacity: redefine the fitness criteria before changing the execution.
   For high-inertia components where reform cost exceeds replacement cost: recommend replacement with a lower-inertia alternative.
   For internal competition against shared constraints: design cooperation protocols.

Diagnosis output format:

- system description and original environment
- current environment (what has changed)
- ceremonial elements identified
- trained incapacity indicators
- inertia map (internal vs. external, by component)
- internal competition / mutual aid opportunities
- niche mismatch (if any)
- recommended interventions (reform vs. replace, with rationale)
- replanning trigger

## Scenario 5: Interaction And Negotiation Strategy

Use this mode when choosing how to behave in competitive or cooperative interactions with other agents, teams, vendors, stakeholders, or systems — especially where the interaction will repeat over time.

This mode applies Maynard Smith's ESS, Axelrod's iterated prisoner's dilemma findings, and Hayek's knowledge distribution to strategy design.

Process:

1. Determine interaction type.
   Is this one-shot (no future, no memory, no relationship) or iterated (repeated encounters, history matters, relationship value exists)?
2. For iterated interactions, apply TFT defaults.
   - Start with cooperation or good faith
   - Respond immediately and proportionally to defection (do not absorb silently)
   - Forgive after one retaliatory cycle; do not extend grudges
   - Be legible: make your strategy predictable so others can model and cooperate with you
3. For competitive selection of strategies, test for ESS stability.
   Ask not "what wins this round?" but "what survives repeated invasion by alternatives?" — the ESS, not the point-in-time winner, is the durable choice.
4. Apply knowledge distribution.
   In interactions with distributed participants (teams, markets, networks), design protocols that let local agents respond to local signals rather than routing all decisions through a center. Emergent coordination from local reciprocity is often more robust than centrally designed rules.
5. Bootstrap cooperation in hostile environments.
   If the current environment is dominated by defection, a small cluster of cooperators interacting with each other first can shift the equilibrium — critical mass, not majority, is the threshold.
6. Design ESS-stable systems.
   When designing incentive structures, protocols, or team norms: make cooperation self-reinforcing, make defection immediately visible and costly, and keep the rules simple enough to be legible to all parties.

Strategy output format:

- interaction type (one-shot vs. iterated)
- current environment (cooperative, defecting, mixed)
- recommended strategy and TFT calibration
- ESS stability assessment of chosen strategy
- knowledge distribution assessment (centralized vs. distributed decision rights)
- bootstrap plan if starting from a hostile environment
- trigger for strategy revision

## Anti-Patterns

Avoid these traps in all scenarios:

- **single-path obsession**: locking in before evidence exists
- **elegance over fit**: defending a plan because it is beautiful rather than effective
- **mistaking speed for adaptation**: moving fast in the wrong direction is not adaptation
- **treating temporary winners as universally best**: winners are fit for a specific environment at a specific time
- **ceremonial drift**: spending effort on status-signaling practices instead of productive ones (Veblen)
- **trained incapacity**: applying skills optimized for a prior environment to a new one without re-evaluating fit (Veblen)
- **internal competition when collective action is needed**: competing between components while facing a shared external threat (Kropotkin)
- **density blindness**: failing to recognize whether you are in a legitimation phase (novel space, novelty welcomed) or a competition phase (crowded space, differentiation required) (Hannan & Freeman)
- **liability of change neglect**: changing too many things at once in a working system even when each individual change seems sound (Hannan & Freeman)
- **naturalizing winners**: assuming current dominant approaches are inevitable rather than fit for a specific context (Hofstadter)
- **folkways lock-in**: inheriting conventions from a prior environment without verifying they still apply (Sumner)
- **flawed selection environment**: running more iterations under wrong fitness criteria instead of using telic agency to redesign the environment (Ward)
- **one-shot thinking in iterated context**: applying competitive strategies to relationships where TFT would dominate over time (Axelrod)
- **routine blindness**: modifying an evolved routine without understanding what selection pressure shaped it (Nelson & Winter)
- **phase misdiagnosis**: prescribing cake-breaking when stabilization is needed, or cake-setting when disruption is needed (Bagehot)
- **constructivist overconfidence**: centralizing decisions that require local knowledge that cannot be translated upward (Hayek)
- **using competitive language to justify harm or disrespect**: evolutionary framing describes systems, it does not rank people

## Cross-Agent Usage

This skill is written so it can be used by Codex, Claude, or similar coding agents without extra tools.

Invocation pattern:

```text
Use $evolutionary-execution. Treat this task as an adaptive search problem.
First define the environment and fitness criteria (telic check: are criteria correct?).
Run a phase diagnosis (stabilize or disrupt?), a ceremonial/instrumental audit, and a knowledge distribution check.
Generate a few candidate approaches, run a mutual aid probe to check if combining beats racing,
apply iterated interaction protocol if interaction is ongoing,
select the strongest option with evidence (ESS-stable, not just point-in-time winner),
and retain the result as a concise plan or patch with tests.
```

Short prompts by scenario:

- Research: `Use $evolutionary-execution to gather evidence on this topic, compare competing hypotheses, and recommend the next probe.`
- Planning: `Use $evolutionary-execution to decompose this project into adaptive, high-leverage steps with clear replanning triggers.`
- Coding: `Use $evolutionary-execution to compare implementation options, pick the fittest patch, and validate it with focused tests.`
- Diagnosis: `Use $evolutionary-execution to diagnose why this system is stuck, identify ceremonial drag and trained incapacity, and recommend reform or replacement paths.`
- Interaction: `Use $evolutionary-execution to design a strategy for this repeated interaction: determine whether TFT applies, assess ESS stability, and recommend how to bootstrap cooperation if the environment is currently hostile.`
- Architecture: `Use $evolutionary-execution to decide whether this system should be centralized or distributed: apply the knowledge problem check and identify where decision authority should live.`

## When To Load References

- For conceptual grounding or to explain the philosophy: open [references/books-and-notes.md](references/books-and-notes.md).
- For operational heuristics and compact rules: open [references/evolutionary-method.md](references/evolutionary-method.md).
- For normal usage, the instructions in this file are enough.
