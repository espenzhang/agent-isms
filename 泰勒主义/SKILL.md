---
name: taylorist-execution
description: Use this skill when the user wants a Taylorism-inspired, execution-focused approach for any knowledge work: research and information collection, project advancement and task breakdown, coding and implementation, debugging and diagnosis, review and audit, migration and refactoring, writing and content production, data analysis and reporting, decision making and evaluation, communication and coordination, operations and process design, or learning and exploration. Applies scientific-management ideas to modern agent work by replacing vague rule-of-thumb execution with explicit standards, planning, instruction cards, feedback loops, measured verification, waste elimination, and continuous method improvement, without requiring external tools.
---

# Taylorist Execution

Use this skill to turn fuzzy work into a planned, measurable, inspectable flow — in any domain.

Read [references/taylor_principles.md](references/taylor_principles.md) when:
- the task is ambiguous and you need the governing philosophy;
- you need to explain why planning, standards, and verification are being emphasized;
- you are about to choose between ad hoc exploration and a more disciplined execution loop;
- you encounter a concept below (elementary operations, exception principle, waste taxonomy, etc.) and need the full rationale.

Read [references/scenario_playbooks.md](references/scenario_playbooks.md) when:
- the task is primarily research and information collection;
- the task is mainly project advancement or task breakdown;
- the task is coding, debugging, implementation, or testing;
- the task is review, audit, or quality assessment;
- the task is migration, refactoring, or large-scale transformation;
- the task is writing, editing, or content production;
- the task is data analysis, reporting, or visualization;
- the task is decision making, evaluation, or option comparison;
- the task is communication, coordination, or stakeholder alignment;
- the task is operations design, process improvement, or workflow creation;
- the task is learning, exploration, or technology evaluation.

---

## The mental revolution

Taylor's congressional testimony (1912) distilled his life's work into one idea: scientific management is NOT any efficiency device, not time study, not motion study, not instruction cards. It IS "a complete mental revolution" on both sides — planner and executor.

The content of this revolution: **both sides stop fighting over dividing the surplus and together turn their attention toward increasing the size of the surplus.** Without this shift in orientation, no amount of mechanism constitutes scientific management.

For agent work, the mental revolution means:
- Studying a task before doing it is not wasted time — it is the foundation.
- Writing down the method is not bureaucracy — it is the coordination mechanism.
- Verifying the result is not doubt — it is professionalism.
- Improving the method is not restlessness — it is the system working as designed.
- The goal is prosperity for all parties: better output, better quality, less wasted effort.

---

## Operating stance

Do not imitate historical factory management literally. Apply the useful parts of Taylor's method to knowledge work:

- Replace rule-of-thumb with explicit working standards.
- Separate planning from execution, but keep a tight feedback loop.
- Define one best current method, then revise it when evidence improves it.
- Make work observable through artifacts, not vague status claims.
- Optimize for throughput, quality, and repeatability, not performative busyness.
- Match the right tool and method to the material at hand (the shovel principle).
- Manage by exception: focus attention on deviations, not routine confirmations.
- Treat the method itself as improvable: when work reveals a better standard, adopt it.
- Eliminate waste systematically: wasted effort, wasted material, wasted time, wasted capability.
- Provide personal attention at the unit level: the bicycle-ball principle.

Remember the mechanism-philosophy distinction: task cards, checklists, and verification loops are mechanisms. The philosophy is disciplined method, explicit standards, cooperative execution, and equal division of responsibility between planning and doing. Never confuse adopting a mechanism with practicing the philosophy.

---

## Core principles (from Taylor's four duties of management)

1. **Develop a science for each element of work.** Study the task before acting. Replace intuition with observation, measurement, and tested method.
2. **Select and prepare for the work.** Match capability to task. A first-class approach to one kind of work may be wrong for another. Measure the "personal coefficient" — what approach fits this specific situation.
3. **Cooperate to ensure the work follows the developed method.** Surface assumptions early, expose tradeoffs, verify against the real goal. Cooperation is the essence, not a nicety.
4. **Divide responsibility between planning and execution.** The planner should not also be the executor improvising the whole system. Separate the two, then connect them through instruction cards and feedback.

---

## Default workflow

### 1. Clarify the output (the prosperity target)
Define the deliverable, acceptance checks, stopping condition, and what counts as "done." Define who benefits and how — maximum prosperity means the output serves both the requester and the quality of the work itself. If the request is vague, restate the desired outcome in concrete terms before proceeding.

### 2. Study before acting
Inspect the existing state before proposing a path. Do not jump to execution from intuition alone. As Taylor observed: the science of any non-trivial work is typically beyond the executor who is best suited to doing it — study must precede action.

When investigating a problem or bug, study means: read the repository structure, trace the relevant code paths, inspect test coverage, and examine error messages or failing outputs. Map the system's components and their relationships before proposing a cause.

#### Fault Localization Procedure (Study Applied to Bug Reports)

When given a bug report or issue and asked to identify which files need editing, apply the following instruction card:

```
Task:        Identify the top 5 files most likely to need editing
Inputs:      Problem statement, read-only repository access
Method:
  STEP 1 — List the repository structure:
    find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" \) | head -80
    Read the directory layout to understand which module owns which behavior.

  STEP 2 — Decompose the issue into elementary operations:
    What specific operation is described as failing?
    What should it do vs. what does it actually do?
    List each described operation as a separate unit.

  STEP 3 — Locate the file responsible for each operation:
    grep -r "FailingFunctionName\|FailingClassName" --include="*.py" -l
    Read the matching files. Confirm they handle the described operation.

  STEP 4 — Check the direct call chain:
    For the primary candidate, look at who calls it (search for its name in other files).
    Include the calling file if the bug could live in how the call is made.

  STEP 5 — Rank by ownership:
    Files that own the most failing operations rank first.
    Files one level up in the call chain rank second.
    Include a test file if there is a directly relevant failing test.

Output:      5 file paths ordered by likelihood, with one-line justification each
Verification: Each file must have been found via grep or explicitly read
```

### 3. Diagnose waste
Before planning the work, identify what is being wasted or could be wasted:
- **Effort waste**: doing things that do not contribute to the output; repeating work; using inefficient methods.
- **Material waste**: consuming resources (tokens, compute, source material) without proportional value.
- **Time waste**: waiting, context-switching, unplanned detours, working without a clear target.
- **Capability waste**: using a powerful approach on trivial work, or a weak approach on critical work; not leveraging available tools.

Eliminating waste is not a side benefit — it is a primary objective.

### 4. Decompose into elementary operations
Break the work into its smallest recombinable units. Each elementary operation should be:
- independently completable and verifiable;
- reusable across similar future tasks (unit patterns);
- small enough that failure in one does not corrupt the rest.

This is the equivalent of Taylor's "elementary rate-fixing" — once you have reliable unit operations, you can assemble them into new task sequences without re-studying from scratch.

### 5. Standardize the job
Convert the work into a small set of explicit steps, decision rules, and checkpoints. Name assumptions. Select the right tools for the material:
- different tasks demand different tools, just as different materials demand different shovels;
- use the tool calibrated for the job, not the one that happens to be at hand.

### 6. Separate planning from execution
Do the planning work first: scope, task order, dependencies, risks, verification strategy, and required artifacts. Then execute against that plan. The plan is not bureaucracy — it is preparation that enables the executor to work better and faster.

"Almost every act of the executor should be preceded by one or more preparatory acts of planning which enable the work to be done better and quicker."

### 7. Issue an instruction card
For each unit of work, state clearly:

```text
Task:        [what to do]
Purpose:     [why this unit matters]
Inputs:      [what is needed before starting]
Constraints: [boundaries, style, compatibility, time]
Route:       [sequence of operations, dependencies on other units]
Method:      [exact actions, tools, parameters]
Output:      [expected deliverable]
Verification:[how to confirm the output is correct]
Time limit:  [stopping condition or timebox]
```

The instruction card is the single most important coordination artifact. It replaces verbal hand-waving with written specification. Every detail that appears self-evident should still be recorded — nothing should be left to memory or assumption.

### 8. Execute one bottleneck at a time
Work on exactly one critical-path unit at a time. Do not scatter effort across multiple fronts. Complete, verify, and close each unit before starting the next.

### 9. Provide feedback at the unit level
After each unit completes, generate immediate feedback:
- **Success signal** (white slip equivalent): unit verified, output confirmed, proceed.
- **Failure signal** (yellow slip equivalent): unit failed verification, deviation noted, correction needed before proceeding.

Do not accumulate multiple units before checking. The feedback must be timely — "a reward, if it is to be effective, must come soon after the work has been done."

### 10. Apply the exception principle
When reporting or reviewing, note what was completed satisfactorily and then enumerate only the deviations, failures, or surprises. Do not repeat routine confirmations at length. Attention should focus on significant departures from the standard.

### 11. Provide personal attention
When a unit stalls or quality drops, give that specific unit focused individual attention — diagnose what is wrong, adjust the method, provide support. This is the bicycle-ball principle: measuring and attending to each unit "as often as once every hour" was a key factor in achieving both quality and efficiency gains. Personal attention is not overhead — it is the mechanism that catches problems before they compound.

### 12. Verify with over-inspection
For work where quality failures are costly, apply layered verification:
- primary check by the executor immediately after completing each unit;
- secondary check by a different method or perspective (different test, different angle of reading, re-derivation);
- the knowledge that work may be re-inspected maintains diligence throughout.

### 13. Inspect and improve the method
If the work stalls, quality drops, or a better approach becomes apparent, revise the process itself: split tasks further, tighten standards, change the tool, or improve the verification loop. Capture any improved method discovered during the work so similar work becomes faster next time.

---

## The law of sustainable pace

Taylor's fatigue studies showed that sustainable output requires deliberate rest intervals proportional to the intensity of the work:
- At 92-pound loads: only 43% of the day under load; 57% rest.
- For concentrated inspection work: mandatory 10-minute breaks every 1.25 hours, plus full rest days.
- Shorter working hours with planned rest periods produced MORE output than longer hours.

For knowledge work:
- Heavy cognitive load (complex debugging, architecture decisions, dense writing) cannot be sustained continuously — build in explicit pauses to review and consolidate.
- For extended tasks, set intermediate checkpoints where progress is assessed and direction is confirmed before continuing.
- A task calibrated correctly can be sustained over time without degradation. If quality drops noticeably as work continues, the task is either too large, too intense, or the method needs revision — not more effort.

---

## Waste taxonomy (diagnostic tool)

Use this framework to identify what is being wasted before and during any task:

| Waste type | What it looks like | Taylor's solution |
|---|---|---|
| **Effort** | Doing things that don't contribute; repeating work; inefficient methods | Time study → find the one best current method |
| **Material** | Consuming resources disproportionate to value | Stores management → standardize inputs, track consumption |
| **Time** | Waiting; context-switching; working without a target | Routing and scheduling → plan the path, eliminate idle gaps |
| **Capability** | Using the wrong tool/method for the task; not leveraging available strengths | Scientific selection → match capability to task; the shovel principle |

The three root causes of waste (per Taylor):
1. The fallacy that more output eliminates work — leading to conservative, under-ambitious execution.
2. Defective systems that punish good performance — leading to concealed capability.
3. Rule-of-thumb methods — inherited habits applied without examination.

---

## Anti-patterns (soldiering equivalents)

**Natural soldiering** (drifting):
- skimming instead of reading;
- starting execution before understanding the context;
- deferring verification to "later";
- producing vague summaries instead of concrete artifacts;
- answering with plausible generalities instead of verified specifics.

**Systematic soldiering** (entrenched bad practice):
- always using the same approach regardless of the material;
- treating all tasks as equally complex or equally trivial;
- skipping planning because "it's faster to just do it";
- hiding uncertainty behind confident language instead of stating assumptions;
- doing the minimum to appear productive without verifying that the output serves the goal.

**Initiative-and-incentive trap**:
- jumping straight into execution with enthusiasm but no method;
- relying entirely on the executor's judgment without developing explicit standards;
- energy without science produces activity, not results.

When you notice any of these patterns, name it and correct course.

---

## Implementation order

When introducing this method to a new domain, project, or unfamiliar environment, follow Taylor's advice — begin with changes that are least disruptive and build outward:

1. **Standards first.** Understand and document the existing conventions, patterns, and expectations.
2. **Study the units.** Read the material, inspect the state, measure what exists before proposing changes.
3. **Establish the inspection system.** Make sure verification works reliably before pushing for higher output. The inspector is trained first.
4. **Then increase throughput.** Only after standards, study, and inspection are in place should you optimize for speed.

Starting with speed before establishing standards produces unreliable results.

---

## Behavioral rules

- Prefer explicit criteria over implicit expectations.
- Prefer smaller tasks with visible completion over large blended efforts.
- Prefer one active bottleneck at a time over scattered parallelism.
- Prefer written instructions and checklists for repeated work.
- Prefer verification during execution, not only at the end.
- Prefer the right tool for the material over the familiar tool for every job.
- Prefer timely feedback at the unit level over delayed batch review.
- Treat unexpected findings as process input: update the plan, do not hide the deviation.
- Record everything that might matter: nothing left to memory.
- When a unit of work cannot be verified, it is not yet well-specified — refine it before executing.
- When the next source, file, or experiment yields diminishing returns, stop collecting and synthesize.
- When quality drops, give personal attention to the failing unit — diagnose, don't push harder.

---

## Quality bar

Before finishing, confirm:
- the deliverable matches the requested scope;
- the path taken is documented enough to repeat;
- verification steps match the risk level of the work;
- open risks and assumptions are stated plainly;
- deviations from the original plan are noted with rationale;
- waste was identified and addressed (or consciously accepted with justification);
- any improved method discovered during the work is captured for reuse;
- the report applies the exception principle: what succeeded is noted briefly, what deviated is described in detail.

---

## Cross-agent use

This skill is written to work in Codex-style and Claude-style environments.
- In systems with native skill loading, invoke `$taylorist-execution`.
- In systems without native skill loading, load this `SKILL.md` first and then open the referenced files only as needed.
