# Scenario Playbooks

Use the playbook that matches the dominant mode of work. When a task spans multiple modes, start with the playbook that covers the first phase and transition to the next as the work evolves.

Each playbook follows the same structure: goal, workflow, instruction-card pattern, standards, elementary operations, tool selection, exception-principle application, and verification strategy.

---

## 1. Research and information collection

**Goal**: Produce a reliable, decision-ready picture of a topic — not a pile of loosely related notes.

**Workflow**:
1. Define the research question and the output format.
2. Break the topic into subquestions (elementary operations of research).
3. For each subquestion, identify the best source type (code, docs, web, user clarification).
4. Collect source material systematically, recording claims with source linkage.
5. Separate facts, interpretations, and open questions — tag each.
6. Stop collecting when the next source yields diminishing returns (the 21-pound rule applied to information gathering).
7. Synthesize the result into a structured decision memo.

**Instruction-card pattern**:
```text
Task:        Research [bounded question]
Purpose:     Answer the question well enough to support a decision.
Inputs:      User question, existing files, trusted sources.
Constraints: Timebox, source quality, recency requirements.
Route:       Subquestion 1 → Subquestion 2 → ... → Synthesis.
Method:      Split into subquestions, gather evidence per subquestion,
             compare sources, tag claims (fact / inference / unknown), synthesize.
Output:      Structured findings with citations and unresolved questions.
Verification:Each key claim traces to a source or is labeled as inference.
Time limit:  [user-defined or self-imposed timebox]
```

**Elementary operations**: defining a subquestion; searching a source; reading a source; extracting a claim; tagging a claim; comparing two sources; synthesizing across claims.

**Tool selection**: use search tools for discovery, read tools for extraction, write tools for synthesis. Do not use one tool for all three (the shovel principle).

**Exception principle**: report what was found as expected briefly; describe gaps, contradictions, and surprises in detail.

**Verification**: each claim traces to a source. If a claim cannot be sourced, it is labeled as inference or hypothesis, never presented as fact.

---

## 2. Project advancement and task breakdown

**Goal**: Turn a broad initiative into a sequence of executable units with clear completion criteria.

**Workflow**:
1. Restate the desired outcome in concrete, verifiable terms.
2. Identify the current state by inspection (study before acting).
3. Identify blockers — record each as an explicit queue item, not a vague concern.
4. Split the work into milestones, each ending in a visible state change.
5. Split milestones into tasks small enough to complete and verify in one effort (the 21-pound rule).
6. Order tasks by dependency and risk (the route system).
7. Define what evidence closes each task.
8. Begin with the inspection system: ensure that verification works before pushing throughput.

**Instruction-card pattern**:
```text
Task:        Advance [project/initiative name]
Purpose:     Move the project to the next verified state.
Inputs:      Goal, current state, requirements, constraints.
Constraints: Time, dependencies, risk tolerance, scope.
Route:       [ordered list of milestones with dependencies]
Method:      Inspect current state, decompose into milestones and tasks,
             prioritize by dependency and risk, execute highest-leverage task,
             verify, iterate.
Output:      Updated plan plus finished artifacts for the active task.
Verification:Active task has objective evidence of completion;
             next step is clear and unblocked.
Time limit:  [per-task timebox]
```

**Elementary operations**: reading current state; identifying a blocker; defining a milestone; splitting a milestone into tasks; ordering tasks; writing a task specification; executing a task; verifying a task.

**Exception principle**: the plan update should note what proceeded as expected and then detail only the deviations.

**Verification**: each task has a defined closure condition. If a task cannot be verified, it is not yet well-specified — refine it before marking it done.

---

## 3. Coding, implementation, and testing

**Goal**: Produce working code with matching verification — not just plausible edits.

**Workflow**:
1. Inspect the relevant files and runtime expectations (study before acting).
2. State the bug, feature, or behavior change in one sentence.
3. Identify the elementary operations: which files to read, which functions to change, which tests to write or run.
4. Decide the smallest safe change that satisfies the requirement.
5. Implement one coherent slice at a time (one bottleneck at a time).
6. Run the closest relevant tests or checks immediately after each slice.
7. If a check fails, diagnose before broadening the change — do not add more code to mask the failure.
8. Summarize what changed, how it was validated, and remaining risk.

**Instruction-card pattern**:
```text
Task:        Implement [specific behavior change]
Purpose:     Change code to satisfy [requirement/fix].
Inputs:      Existing code at [paths], failing behavior or requirement, tests at [paths].
Constraints: Style conventions, architecture patterns, compatibility requirements.
Route:       Read context → Plan change → Edit → Test → Verify → Report.
Method:      Inspect first, patch smallest viable slice, validate, iterate.
Output:      Code change and verification result.
Verification:Tests pass; build succeeds; manual check confirms behavior;
             or inability to run checks is clearly stated with the gap and risk.
Time limit:  [per-slice timebox]
```

**Elementary operations**: reading a file; understanding a function; writing a test; editing a function; running a test; reading an error; diagnosing a failure; documenting a change.

**Tool selection**: read tools for inspection; edit tools for modification; dedicated test runners for verification; search tools for finding related code. Match the tool to the operation.

**Over-inspection**: for high-risk changes, apply layered verification:
- first check: tests pass;
- second check: verify the behavior by a different method (manual test, reading the diff for logic, checking edge cases);
- third check: review for unintended side effects in adjacent code.

---

## 4. Debugging and diagnosis

**Goal**: Identify the root cause of a defect through systematic study, not trial-and-error patching.

**Workflow**:
1. Reproduce the problem or confirm the symptoms by inspection.
2. State the observed behavior vs. expected behavior in one sentence.
3. Form hypotheses about possible causes (elementary operations of diagnosis).
4. Rank hypotheses by likelihood and testability.
5. Test the most likely hypothesis first with the least invasive observation.
6. If confirmed, trace the cause to its root — do not stop at the first correlating factor.
7. If refuted, move to the next hypothesis. Do not repeat the same test hoping for a different result.
8. Once root cause is identified, apply the coding playbook (scenario 3) for the fix.

**Instruction-card pattern**:
```text
Task:        Diagnose [symptom description]
Purpose:     Identify the root cause before attempting a fix.
Inputs:      Bug report, reproduction steps, relevant code paths, logs.
Constraints: Cannot modify production; timebox for diagnosis.
Route:       Reproduce → Hypothesize → Test hypothesis 1 → ... → Root cause → Fix.
Method:      Systematic elimination. Test one variable at a time.
             Change nothing until the cause is confirmed.
Output:      Root cause statement with evidence chain.
Verification:The explanation accounts for all observed symptoms;
             the fix eliminates the symptom without introducing new ones.
Time limit:  [diagnosis timebox before escalating or changing approach]
```

**Key Taylor parallel**: this is the equivalent of Taylor's metal-cutting experiments — 12 variables, each affecting the outcome, testable only by controlling all others and varying one at a time. The 20-minute trial methodology: run a controlled test, observe the result, adjust one variable, repeat.

---

## 5. Review, audit, and quality assessment

**Goal**: Assess the quality and correctness of existing work against defined standards.

**Workflow**:
1. Define the review criteria (standards) before starting the review.
2. Read the work systematically — do not skim (resist natural soldiering).
3. For each unit of work, check against each criterion independently.
4. Record findings tagged as: conforming, minor deviation, major deviation, or unknown.
5. Apply the exception principle: note conforming items briefly, describe deviations in detail.
6. For major deviations, trace to root cause — is it a content problem, a spec problem, or a process problem?
7. Summarize with actionable recommendations.

**Instruction-card pattern**:
```text
Task:        Review [scope]
Purpose:     Assess quality against [defined standards].
Inputs:      Work to review, standards/criteria, context.
Constraints: Review scope, time, depth of analysis.
Route:       Define criteria → Systematic reading → Per-unit assessment →
             Deviation analysis → Summary.
Method:      Check each unit against each criterion. Tag findings.
             Focus detail on deviations.
Output:      Review report with tagged findings and actionable recommendations.
Verification:Every major finding cites specific evidence.
             Recommendations are concrete, not vague.
Time limit:  [review timebox]
```

**Over-inspection**: for critical reviews, use two passes:
- first pass: systematic criterion-by-criterion check;
- second pass: holistic reading for issues that fall between criteria (design smell, implicit assumptions, missing edge cases).

**The inspector-first principle**: establish what "good" looks like before assessing what exists.

---

## 6. Migration, refactoring, and large-scale transformation

**Goal**: Move a system from state A to state B without breaking it in transit.

**Workflow**:
1. Document the current state thoroughly (study before changing).
2. Define the target state in concrete, verifiable terms.
3. Identify the transformation as a sequence of small, independently verifiable steps.
4. For each step, define: what changes, what must remain unchanged, and how to verify both.
5. Establish the verification system before starting the transformation (inspector first).
6. Execute one step at a time. Verify after each step. Do not batch multiple steps before checking.
7. If a step fails verification, stop and diagnose before continuing.

**Instruction-card pattern**:
```text
Task:        Migrate/refactor [specific scope]
Purpose:     Transform [current state] to [target state] without regression.
Inputs:      Current system, target spec, existing verification.
Constraints: No breakage in transit; incremental verifiability.
Route:       Step 1 → verify → Step 2 → verify → ... → final state.
Method:      Smallest safe step, verify both changed and unchanged,
             proceed only on green. Rollback plan for each step.
Output:      Transformed system passing all verification.
Verification:After each step: existing checks pass AND step-specific checks pass.
Time limit:  [per-step timebox; overall deadline]
```

**The shoveling parallel**: different materials in a transformation (renaming, restructuring, rewriting logic, updating dependencies) may require different tools. Do not use one approach for all transformation types.

---

## 7. Writing, editing, and content production

**Goal**: Produce clear, accurate, well-structured written output that serves a defined purpose — not vague prose that fills space.

**Workflow**:
1. Define the audience, purpose, and format of the output (clarify the deliverable).
2. Study the source material, context, and constraints before drafting (study before acting).
3. Decompose the writing task into elementary operations: outline, section drafts, evidence gathering, revision passes.
4. Draft in sections, each independently reviewable (one bottleneck at a time).
5. After each section, verify: does it serve the stated purpose? Is every claim supported? Is it the right length?
6. Revise with layered verification: first pass for accuracy, second pass for clarity and structure, third pass for tone and audience fit.
7. Apply the exception principle in review: note what works, detail what needs revision.

**Instruction-card pattern**:
```text
Task:        Write [document type: memo, report, analysis, email, proposal, etc.]
Purpose:     [what decision or action this document should enable]
Inputs:      Source material, context, prior decisions, audience profile.
Constraints: Length, format, tone, deadline, audience expertise level.
Route:       Define structure → Outline → Draft section 1 → verify →
             Draft section 2 → verify → ... → Revision passes → Final check.
Method:      Outline first. Draft per section. Verify each section against purpose.
             Revise in layers (accuracy → clarity → tone).
Output:      Finished document matching format and purpose specification.
Verification:Every factual claim is sourced or labeled as inference.
             Structure serves the stated purpose.
             Length and tone match the audience.
Time limit:  [per-section timebox; overall deadline]
```

**Elementary operations**: defining the audience; outlining structure; drafting a section; finding evidence for a claim; tagging a claim (fact/inference/opinion); revising for clarity; revising for tone; checking length.

**Waste diagnosis**:
- Effort waste: writing sections that don't serve the purpose; over-researching before drafting.
- Material waste: including more detail than the audience needs.
- Time waste: revising endlessly without clear criteria; not outlining first.
- Capability waste: using formal tone when informal is needed, or vice versa (wrong shovel).

**The bicycle-ball principle**: review each section individually, giving personal attention to sections that are weak rather than doing a single undifferentiated pass over the whole document.

---

## 8. Data analysis and reporting

**Goal**: Extract reliable conclusions from data and present them in a form that supports decisions — not just display numbers.

**Workflow**:
1. Define the question the analysis must answer and the decision it supports (clarify the output).
2. Inspect the data: source, quality, completeness, known limitations (study before acting).
3. Identify the elementary operations: data cleaning, transformation, calculation, visualization, interpretation.
4. Standardize the method: which calculations, which thresholds, which visualizations, which comparisons.
5. Execute each operation, verifying intermediate results (do not chain transformations without checking).
6. Separate findings (what the data shows) from interpretations (what the findings mean) from recommendations (what to do).
7. Report with the exception principle: summarize the expected pattern, detail the deviations.

**Instruction-card pattern**:
```text
Task:        Analyze [data source] to answer [specific question]
Purpose:     Support [specific decision] with evidence.
Inputs:      Data source, question, context, known limitations.
Constraints: Data quality, analysis method, output format, deadline.
Route:       Inspect data → Clean → Transform → Calculate → Visualize →
             Interpret → Report.
Method:      One operation at a time. Verify intermediate results.
             Separate facts from interpretations from recommendations.
Output:      Analysis report with findings, interpretations, limitations,
             and actionable recommendations.
Verification:Calculations are reproducible. Findings trace to data.
             Limitations are stated. Interpretations are labeled as such.
Time limit:  [per-operation timebox; overall deadline]
```

**Elementary operations**: inspecting a data source; cleaning a column/field; performing a calculation; checking an intermediate result; creating a visualization; interpreting a pattern; writing a finding; writing a recommendation.

**Key Taylor parallel**: this is the agent equivalent of "On the Art of Cutting Metals" — multiple variables affecting the outcome, each needing systematic isolation and measurement. The 20-minute trial methodology applies: test one analysis approach, check the result, refine, repeat.

**Over-inspection**: for high-stakes analyses, verify by two independent methods (e.g., calculate both manually and programmatically; compare results from different analytical approaches).

---

## 9. Decision making and evaluation

**Goal**: Make or support a decision through systematic comparison of options against defined criteria — not gut feeling or first impression.

**Workflow**:
1. State the decision to be made in one sentence.
2. Define the evaluation criteria and their relative importance (develop the science).
3. Identify the options (study before judging).
4. For each option, gather evidence against each criterion.
5. Separate facts from inferences from unknowns — tag each.
6. Compare options systematically, not holistically.
7. State the recommendation with the evidence chain, the key tradeoffs, and the uncertainties.

**Instruction-card pattern**:
```text
Task:        Evaluate [options] to decide [question]
Purpose:     Reach a well-grounded decision on [specific question].
Inputs:      Options list, criteria, context, constraints.
Constraints: Time, reversibility, risk tolerance, information availability.
Route:       Define criteria → Gather evidence per option per criterion →
             Compare → Recommend.
Method:      Systematic comparison. Each option evaluated against each criterion
             independently. No holistic "feeling" — evidence per dimension.
Output:      Decision recommendation with evidence, tradeoffs, and uncertainties.
Verification:Each claim about an option traces to evidence.
             Criteria weights are explicit.
             Key assumptions are named.
Time limit:  [evaluation timebox]
```

**Elementary operations**: defining a criterion; weighting criteria; gathering evidence for one option on one criterion; comparing two options on one criterion; identifying a tradeoff; stating an uncertainty; formulating a recommendation.

**Waste diagnosis**:
- Effort waste: evaluating options that are clearly dominated (eliminate early).
- Time waste: gathering evidence on low-importance criteria before high-importance ones.
- Capability waste: making a complex decision with a simple method, or vice versa.

**The route system**: evaluate high-importance criteria first. If an option is eliminated early on the most important criterion, do not spend time evaluating it on lesser criteria.

---

## 10. Communication and coordination

**Goal**: Produce communication (messages, updates, proposals, requests) that achieves a specific outcome with the minimum necessary effort from both sender and receiver.

**Workflow**:
1. Define the communication objective: what should the receiver know, decide, or do afterward?
2. Identify the audience: expertise level, context they already have, what they care about.
3. Select the right format and channel for the material (the shovel principle — different messages need different vehicles).
4. Draft with the exception principle: state the normal/expected briefly, detail only what is new, changed, or requires action.
5. Verify: does this message achieve the objective? Can the receiver act on it without asking follow-up questions?

**Instruction-card pattern**:
```text
Task:        Communicate [objective: inform, request, propose, align, escalate]
Purpose:     Enable the receiver to [specific action or understanding].
Inputs:      Context, audience profile, prior communication, urgency.
Constraints: Channel, length, tone, audience time budget.
Route:       Define objective → Identify audience → Select format →
             Draft → Verify against objective → Send.
Method:      Lead with the action or decision needed.
             Apply exception principle: what's normal is brief; what's new is detailed.
             Match format to channel and audience.
Output:      Message that achieves the communication objective.
Verification:A competent receiver can act on this without follow-up questions.
             The objective is achievable from the message alone.
Time limit:  [appropriate to urgency]
```

**Elementary operations**: defining the objective; profiling the audience; choosing the format; drafting the lead (action/decision); providing context; applying the exception principle; reviewing for completeness.

**The bicycle-ball principle**: give personal attention to the most critical message in a batch rather than treating all communications with equal effort.

**Waste diagnosis**:
- Effort waste: writing long messages when short ones suffice; restating known context.
- Time waste: multiple rounds of clarification caused by ambiguous initial message.
- Capability waste: using a formal report when a brief message would do, or vice versa.

---

## 11. Operations and process design

**Goal**: Design or improve a repeatable process that produces consistent, verifiable results — not a one-off procedure that works once by luck.

**Workflow**:
1. Study the current process by observation (study before changing). If no process exists, study the work that needs to be systematized.
2. Decompose the process into elementary operations.
3. For each operation, identify: inputs, method, output, verification, common failure modes.
4. Identify waste in the current process (effort, material, time, capability).
5. Design the improved process: standardize the method for each operation, establish the route, define checkpoints.
6. Build the instruction cards for each operation.
7. Establish the verification system (inspector first — before running the process at speed).
8. Run the process, collect feedback at each checkpoint, iterate.

**Instruction-card pattern**:
```text
Task:        Design/improve process for [repeatable work]
Purpose:     Create a reliable, verifiable, improvable process.
Inputs:      Current process (if any), requirements, constraints, known failure modes.
Constraints: Resources, tools, frequency, acceptable error rate.
Route:       Study current state → Decompose → Identify waste →
             Design improved process → Build instruction cards →
             Establish verification → Run → Iterate.
Method:      Elementary-operation analysis. Standardize each step.
             Route the sequence. Build checkpoints. Eliminate waste.
Output:      Documented process with instruction cards, verification criteria,
             and improvement mechanisms.
Verification:The process produces consistent results across multiple runs.
             Verification catches failures before they propagate.
             The process document is sufficient for a competent executor to follow
             without improvisation.
Time limit:  [design phase timebox; iteration cycles]
```

**Elementary operations**: observing current work; decomposing into steps; identifying waste in a step; designing an improved step; writing an instruction card; defining a checkpoint; testing the process; collecting feedback; revising the method.

**Key Taylor parallel**: this is the direct application of Taylor's planning-department methodology — the 17 functions of the planning department are essentially a process-design framework. The instruction card system, routing, standardization of tools, and exception principle are all process-design techniques.

**The prosperity principle**: a well-designed process benefits everyone — the executor works more efficiently, the requester gets more reliable results, future executors can follow the documented method without re-inventing it.

---

## 12. Learning, exploration, and technology evaluation

**Goal**: Build reliable understanding of an unfamiliar domain, system, or technology — enough to make informed decisions.

**Lighter-touch mode**: Taylor advised using a lighter process when the work is primarily creative exploration and premature structure would block discovery. However, even exploration benefits from:
- a bounded question (what am I trying to learn?);
- systematic coverage (not random wandering);
- recorded findings (not just impressions).

**Workflow**:
1. State the learning objective: what decision will this knowledge support?
2. Identify the key unknowns.
3. For each unknown, identify the best source.
4. Explore systematically, recording findings as you go.
5. Periodically synthesize: what do I now know, what remains unknown, has the original question changed?
6. Stop when the learning objective is met or when further exploration yields diminishing returns.

**Instruction-card pattern**:
```text
Task:        Learn/evaluate [topic or technology]
Purpose:     Build understanding sufficient for [specific decision].
Inputs:      Topic, existing context, available sources.
Constraints: Timebox, depth required, decision deadline.
Route:       Define unknowns → Source 1 → Source 2 → ... → Synthesis.
Method:      Bounded exploration. Record findings per unknown.
             Synthesize periodically. Stop at diminishing returns.
Output:      Structured understanding with: knowns, unknowns, and recommendation.
Verification:Each key claim is grounded in observation or labeled as inference.
             The output answers the original question.
Time limit:  [exploration timebox]
```

**When to escalate to a heavier playbook**: if exploration reveals that the task is more complex than expected, transition to the appropriate playbook with full Taylorist rigor.

---

## Cross-cutting techniques

These techniques apply across all scenarios:

### The 21-pound rule (optimal task sizing)
Both overloading and underloading produce less output than the right-sized load. Apply to any work:
- too large: unverifiable, stalls, accumulates hidden problems;
- too small: overhead exceeds value, no meaningful progress per unit;
- right-sized: completable and verifiable in a single focused effort.

### The route system (predetermined sequencing)
Before starting multi-step work, define the sequence and dependencies. Execute in order. Do not jump ahead before verifying earlier steps.

### The exception principle (focus on deviations)
In all reporting and review, note routine success briefly and describe deviations in detail.

### The feedback loop (white slip / yellow slip)
After each unit of work, generate immediate feedback: success or failure. Timely feedback enables course correction; delayed feedback enables compounding errors.

### The bicycle-ball principle (personal attention)
When a unit stalls or quality drops, give that specific unit focused individual attention. Diagnose what is wrong. Adjust the method. Do not apply general pressure — apply specific support.

### Over-inspection (layered verification)
For high-stakes work, verify by two independent methods. The existence of a second check improves the quality of the first.

### The inspector-first principle
Establish that verification works before pushing for speed. In every scenario, ensure you can detect failure before you optimize for output.

### The shovel principle (right tool for the material)
Different materials require different tools. Do not force one tool or method to serve all purposes. Match the tool to the operation.

### Waste diagnosis
Before and during any task, scan for the four types of waste (effort, material, time, capability) and the three root causes (output-kills-work fallacy, defective systems, rule-of-thumb methods).

### The prosperity principle
The goal is not merely to produce the deliverable, but to produce it in a way that improves capability for future work. The method should get better. The output should serve the requester AND raise the quality of the process.

### Method improvement
Every task is an opportunity to discover a better standard. When the work reveals a more reliable, faster, or clearer method, capture it. The current best method is always provisional.
