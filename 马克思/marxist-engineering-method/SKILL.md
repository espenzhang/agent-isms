---
name: marxist-engineering-method
description: Apply a Marxist, practice-first and contradiction-aware method to engineering work. Use when Codex, Claude, or another coding agent needs to handle (1) research and information gathering, (2) project推进, planning, or task breakdown, (3) coding, debugging, testing, and delivery under competing constraints, (4) system design and architecture decisions, (5) technical debt management and refactoring decisions, (6) cross-team coordination and organizational bottlenecks, (7) incident response and production debugging under time pressure, or (8) legacy system migration and parallel system management. Trigger this skill when requirements are unclear, tradeoffs are sharp, facts are incomplete, incremental fixes keep recurring, organizational structure constrains technical solutions, a system is degrading and the trajectory matters, changes may have far-reaching ripple effects, or the agent risks becoming dogmatic, purely经验主义, or disconnected from repository reality.
---

# Marxist Engineering Method

## Core Orientation

Use this skill to turn Marxist methodology into an engineering workflow: begin from concrete conditions, identify contradictions, find the principal contradiction, act in a practice-first way, and revise understanding through verification.

Prefer facts over slogans, movement over static labels, and real user or team value over performative complexity.

### Theoretical Foundation

This skill draws from the following core Marxist works, each extracted into an engineering-applicable reference:

Epistemology and method:
- [references/practice-on.md](references/practice-on.md) — 《实践论》: knowledge begins in practice, returns to practice, and iterates
- [references/abstract-to-concrete.md](references/abstract-to-concrete.md) — 马克思方法论: ascend from fragmented observations to governing principle, then back to specific interventions
- [references/concrete-analysis.md](references/concrete-analysis.md) — 列宁"具体问题具体分析": every situation has specific conditions; refuse to copy patterns without re-derivation

Dialectical laws:
- [references/contradiction-on.md](references/contradiction-on.md) — 《矛盾论》: find the principal contradiction and its principal aspect
- [references/two-types-contradictions.md](references/two-types-contradictions.md) — 两类矛盾: distinguish antagonistic contradictions (must restructure) from non-antagonistic ones (can mediate)
- [references/quantity-quality.md](references/quantity-quality.md) — 量变质变规律: quantitative accumulation transforms into qualitative shift at a threshold
- [references/negation-of-negation.md](references/negation-of-negation.md) — 否定之否定规律: development spirals upward through successive negations, not circular repetition
- [references/universal-connection.md](references/universal-connection.md) — 普遍联系与发展: trace ripple effects across connected systems; evaluate trajectory, not just snapshot

Historical materialism, mass line, and portfolio management:
- [references/forces-relations.md](references/forces-relations.md) — 生产力与生产关系、社会存在决定社会意识: technical capability must match organizational structure; material conditions shape team practices
- [references/mass-line.md](references/mass-line.md) — 群众路线: gather practitioner experience, synthesize, return for validation
- [references/ten-relations.md](references/ten-relations.md) — 论十大关系: balance multiple competing priorities simultaneously; prevent secondary contradictions from escalating

Read the relevant references when deeper grounding is needed for a specific aspect.

## Working Method

Follow this sequence unless the host agent already has a stronger local workflow:

1. Define the practical objective.
   State what must change in the world after the work is done: what outcome matters, for whom, and how success will be observed.

2. Start from material conditions.
   Inspect the actual repository, files, tests, logs, constraints, ownership boundaries, deadlines, and existing user statements before theorizing. Begin with the repository structure itself: directory layout, module boundaries, entry points, and dependency graph — these material facts determine where problems can exist and where solutions must be applied. Gather practitioner experience where available: bug reports, workarounds, operator runbooks, informal team knowledge (群众路线).

3. Ascend from chaotic to structured understanding.
   Do not stay lost in scattered observations. Find the simplest meaningful unit (the "cell form") and build understanding upward, layer by layer (从抽象到具体). Verify each layer against actual behavior.

4. Separate appearance from essence.
   Distinguish symptoms from structure. Ask what is failing on the surface and what mechanism produces that failure.

5. Map contradictions.
   Identify the important tensions:
- speed vs correctness
- local fix vs systemic fix
- short-term delivery vs long-term maintainability
- developer convenience vs user impact
- new feature vs regression risk
- abstraction vs simplicity
- technical capability vs organizational structure (生产力 vs 生产关系)

   Also ask: have accumulated small changes approached a qualitative threshold (量变质变)? Is a phase shift imminent or already underway?

6. Classify each contradiction.
   For each significant contradiction, ask: can this be mediated within the current structure (non-antagonistic), or does the structure itself need to change (antagonistic)? This determines the form of resolution: adjustment and proportion for non-antagonistic contradictions, structural transformation for antagonistic ones (两类矛盾).

7. Find the principal contradiction.
   Do not treat all issues equally. Name the one contradiction that currently governs progress. Solve or weaken that first. Ensure the diagnosis is specific to this project's conditions, not borrowed from a generic template (具体问题具体分析).

8. Trace connections and ripple effects.
   Before acting, map how the proposed change will propagate: direct dependencies, indirect consumers, human workflows, monitoring assumptions, deployment pipelines. Include who will be affected beyond the immediate target (普遍联系).

9. Choose a line of action.
   Decide what to do now, what to defer, what to measure, and what not to touch. Make the smallest change that can materially change the situation. Proportion effort across the principal contradiction and at-risk secondary contradictions (论十大关系).

10. Return knowledge to practice.
    Verify with execution: run tests, inspect output, reproduce the bug, compare behavior, or document what remains unverified. Theory that does not return to practice is incomplete. Distinguish two levels of verification: (a) the technical fix works as designed, and (b) the real problem practitioners experienced is actually resolved. Both are necessary (费尔巴哈论纲: the point is to change the world, not just to interpret it). Where possible, validate with the practitioners who reported the original problem (群众路线).

11. Reassess after movement.
    After each meaningful action, ask:
- Has the principal contradiction changed? If so, update the plan.
- Is the new cycle solving a higher-level problem than the last, or mechanically repeating (否定之否定)? If repeating, shift the level of abstraction.
- Has the accumulated progress reached a threshold that warrants a qualitative shift in approach (量变质变)?
- Has any secondary contradiction worsened and now threatens to become principal (论十大关系)?
- Has the trajectory of the system changed? Is the rate of improvement accelerating, stalling, or reversing (发展的观点)?

## Operational Rules

- Refuse abstract certainty without repository evidence.
- Refuse blind empiricism that piles actions together without extracting a pattern.
- Refuse borrowed patterns that have not been re-derived for this project's specific conditions.
- Prefer concrete inspection over template-driven answers.
- Prefer staged progress over total redesign unless the contradiction is truly antagonistic.
- Explain tradeoffs as relations, not isolated pros and cons.
- Track who bears the cost of a decision: user, maintainer, operator, teammate, downstream service, or future work.
- Trace connections before acting: what depends on the component being changed? Where will side effects surface?
- Assess trajectory, not just current state: is the situation improving, degrading, or stagnant?
- Distinguish technical problems from organizational problems. Do not disguise one as the other.
- Distinguish antagonistic from non-antagonistic contradictions. Do not restructure what can be mediated, and do not mediate what must be restructured.
- Understand the conditions that produced current practices before proposing to change them.
- Keep unknowns explicit.
- Use only the host agent's native capabilities. Do not assume external integrations.

## Scenario 1: Research, Information Gathering, And Fault Localization

Use this mode when requirements are fuzzy, context is missing, the task begins with investigation, or you are asked to identify which files in a repository need to be changed to fix a bug or issue.

### Fault Localization Procedure

When given a problem statement or bug report and asked to identify which files need editing, execute these steps in order. Do not skip steps.

**Step 1 — Map the material conditions.**
Inspect the actual structure of the repository before forming any theory:
- Run `find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.java" \) | head -80` to see the file tree.
- Read the top-level directory listing to understand module organization.
- Note which directories correspond to which subsystems.
The material structure of the codebase determines where bugs can live. Do not skip this step.

**Step 2 — Extract concrete entities from the issue.**
Read the problem statement carefully. List explicitly:
- Every class name, function name, method name, module name, or file name mentioned.
- The specific behavior described: what error occurs, what wrong output is produced, what test fails.
- Any stack traces, error messages, or line references.

**Step 3 — Search for each extracted entity.**
For every entity identified in Step 2:
- Run `grep -r "EntityName" --include="*.py" -l` (adapt extension to the repo language) to find all files containing it.
- Read the most relevant files to understand what mechanism they implement.

**Step 4 — Trace universal connections (the decisive step).**
This is the step that separates appearance from essence. The file that shows the error is often not the file that must change. For each top candidate from Step 3:
- Run `grep -r "import.*<module_name>\|from.*<module_name>" --include="*.py" -l` to find every file that imports this candidate. These are upstream dependents — bugs in shared modules surface here.
- Look inside the candidate file itself: `grep "^import\|^from" <candidate_file>` to see what it depends on. One of those dependencies may be the true source.
- Build a two-level map: what does this file import? Who imports this file?

**Step 5 — Identify the principal file (the root contradiction).**
Among all candidates, name the one file that:
- Owns the mechanism that produces the wrong behavior, AND
- Changing it would most directly resolve the described symptom.

This is the principal file — the location of the principal contradiction. The error may surface elsewhere, but the cause lives here.

**Step 6 — Rank the remaining suspects by causal proximity.**
Order your remaining top-4 candidates by how directly they relate to the principal file:
- Direct callers/importers of the principal file rank higher.
- Files that implement related but secondary mechanisms rank lower.
- Include a test file if a test directly exercises the failing path.

**Step 7 — Verify with evidence before finalizing.**
For each of your 5 predictions, state the specific evidence:
- Which file did you read?
- What specific code pattern (import, function call, class definition) connects it to the described symptom?

Do not include a file in your top-5 unless you have read it or read something that imports/is imported by it.

### General Research Procedure

For non-localization investigation tasks:

1. Define the practical question with an answerable form: not "research this codebase" but "what blocks X?" or "what is the safest path to Y?"
2. Build a concrete evidence set. Prioritize files directly named in errors, stack traces, or the problem description.
3. Ascend from observations to structure. Find the cell form (simplest meaningful operation) and layer upward until the observed behavior is explained (从抽象到具体).
4. Distinguish contradiction layers: symptom vs. cause, local vs. architectural, technical vs. organizational.
5. Name the principal contradiction and the next best step.

Output shape:
- objective
- evidence gathered (files read, searches run)
- dependency map relevant to the problem
- principal contradiction and the file(s) where it lives
- ranked suspect files with specific causal justification
- recommended next action

## Scenario 2: Project Push And Task Breakdown

Use this mode when a task is too large, blocked, politically messy, or diffused across many threads.

Procedure:

1. Define the current stage of practice.
   Ask whether the work is in discovery, alignment, implementation, stabilization, or delivery.

2. Identify the contradiction that governs progress.
   Typical examples:
- scope expansion vs delivery deadline
- unclear ownership vs need for execution
- fragile codebase vs demand for rapid change
- parallel workstreams vs integration risk
- technical readiness vs organizational readiness (生产力 vs 生产关系)

3. Split by contradiction, not by superficial categories.
   Good decomposition isolates decisive tensions. Bad decomposition creates many parallel tasks that all depend on the same unresolved bottleneck.

4. Order tasks by material leverage.
   Sequence work so earlier tasks change the conditions for later tasks. Resolve unknowns, interfaces, and testability early. Identify where a single qualitative intervention (a structural change) can eliminate an entire category of quantitative tasks.

5. Balance secondary contradictions.
   While pursuing the principal contradiction, monitor secondary ones. Ask: if this secondary contradiction is neglected for another cycle, will it become principal? Proportion effort to prevent decay without losing focus (论十大关系思维).

6. Keep a moving center.
   Revisit the principal contradiction after each milestone. Do not keep yesterday's task plan when today's facts changed. Each reassessment should produce a qualitatively better plan, not a patched version of the old one (否定之否定).

Recommended decomposition template:
- task goal
- why it matters materially
- blocker or contradiction it addresses
- dependency on prior tasks
- proof of completion
- what secondary contradictions this task leaves unaddressed

## Scenario 3: Coding, Debugging, And Testing

Use this mode when writing or changing code.

Procedure:

1. Reproduce or inspect before editing.
   Ground action in failing tests, runtime behavior, logs, code paths, or clear user-reported behavior. If practitioners have workarounds, understand what the workaround reveals about the real failure mode.

2. Locate the principal contradiction in the implementation.
   Examples:
- correctness vs backward compatibility
- performance vs readability
- fast patch vs maintainable design
- mock-based passing tests vs real behavior

3. Check for accumulated quantity.
   Is this the Nth fix to the same module or mechanism? If so, ask whether the accumulated patches have reached a qualitative threshold. The correct intervention may be to replace the mechanism, not patch it again (量变质变).

4. Change the decisive point first.
   Patch the mechanism that governs behavior. Avoid broad churn that does not alter the contradiction.

5. Keep implementation and verification in one cycle.
   Each meaningful code change should have a matching validation step: automated tests, manual reproduction, static checks, or clearly stated verification gaps. Where possible, check with the original reporter: does the fix match their experience?

6. Ensure spiral progress.
   If this debugging cycle resembles a previous one, ask: am I solving at a higher level of abstraction, or repeating the same approach? If repeating, shift levels: from patching behavior to restructuring the interface that produced the behavior (否定之否定).

7. Summarize in transformed terms.
   Report what contradiction was addressed, what changed materially, what evidence now supports the result, what contradictions remain, and whether the fix was quantitative (within the current structure) or qualitative (changing the structure).

## Scenario 4: System Design And Architecture Decisions

Use this mode when designing a new system, evaluating architectural options, or deciding whether to restructure.

Procedure:

1. Start from the concrete need, not from an architectural ideal.
   Define the practical problem the design must solve. Resist beginning with a pattern ("let's use microservices") and instead begin with the material constraint ("we need independent deployment for the billing module").

2. Ascend from cell form to full design.
   Identify the simplest meaningful operation the system must perform. Design for that first. Then add complexity one layer at a time: error handling, scaling, multi-tenancy, observability. At each layer, verify that the added complexity is demanded by concrete conditions, not by architectural taste (从抽象到具体).

3. Re-derive, do not copy.
   If referencing another system's architecture, list the conditions that made it work there. Check each condition against this project. Missing conditions invalidate the reference (具体问题具体分析).

4. Map the contradiction between technical and organizational structure.
   Ask: can the current team structure execute this design? Does code ownership match module boundaries? Does deployment authority match service boundaries? If not, either adjust the design to fit the organization, or identify the organizational change needed and assess its feasibility (生产力与生产关系).

5. Prefer the smallest qualitative change over the grandest redesign.
   If the current architecture can be saved by changing one interface, one ownership boundary, or one deployment pipeline, prefer that over a full rewrite—unless analysis shows the accumulated degradation has already crossed a qualitative threshold (量变质变).

6. Define proof of design validity.
   State how the design will be verified in practice: prototype, spike, load test, staged rollout. A design that cannot be tested incrementally is suspicious.

Output shape:
- practical need
- cell form and ascending design layers
- conditions assumed (and which hold in this project)
- organizational fit assessment
- principal design contradiction
- recommended approach with verification plan

## Scenario 5: Technical Debt Management And Refactoring Decisions

Use this mode when deciding whether, when, and how to address accumulated technical debt.

Procedure:

1. Inventory the accumulation.
   Count concrete indicators: recurring bug categories, patch frequency to the same modules, workaround layers, velocity trends, incident recurrence rates. These are quantitative measures of debt.

2. Assess the qualitative threshold.
   Ask: has the accumulation changed the character of the system? Signs of a qualitative shift already underway:
- workarounds outnumber designed paths
- new features require disproportionate effort in the degraded area
- the team has informally abandoned the official architecture in favor of ad-hoc patterns
- incident response depends on tribal knowledge, not system design

3. If the threshold has not been reached: patch within the current structure.
   Make targeted fixes that reduce the rate of accumulation. Track whether each fix actually reduces future incidents or merely addresses the current one.

4. If the threshold has been reached: plan a qualitative intervention.
   Design a structural change (refactor, rewrite, decompose) that resets the quantitative parameters. Ensure the new structure preserves the gains of the old one—especially hard-won edge case handling and battle-tested behavior (否定之否定: transcend, do not regress).

5. Validate the organizational fit.
   A refactoring plan that requires team reorganization, new ownership boundaries, or different deployment processes must account for those changes. A pure-code refactor in an incompatible organizational structure will degrade back to its current state (生产力与生产关系).

6. Verify with practitioners.
   Before and after refactoring, gather feedback from the developers and operators who work with the affected code daily. Their experience is the ground truth for whether debt has been meaningfully reduced (群众路线).

## Scenario 6: Cross-Team Coordination And Organizational Bottlenecks

Use this mode when progress is blocked not by technical difficulty but by ownership, communication, or coordination problems.

Procedure:

1. Distinguish force problems from relation problems.
   Force problem: "We don't have the capability to do X" (missing skill, tool, or infrastructure).
   Relation problem: "We can do X, but the ownership model / approval process / communication path prevents it." Treat them differently (生产力与生产关系).

2. Map the organizational contradiction.
   Typical examples:
- centralized ownership vs distributed execution needs
- team boundaries vs cross-cutting change requirements
- individual expertise vs bus factor risk
- fast local decisions vs global consistency needs

3. Gather scattered experience from practitioners.
   Ask the people blocked by the coordination problem: what do they actually experience? What workarounds have they developed? What informal processes exist that the formal structure does not capture? (群众路线)

4. Synthesize, do not aggregate.
   Transform scattered complaints into a structural diagnosis: which organizational relationship is mismatched with the current technical reality? Name the specific mismatch, not a general category ("communication is bad").

5. Propose the smallest organizational adjustment that unblocks technical progress.
   This may be: clarifying ownership of one module, creating one shared interface contract, establishing one cross-team review process, or documenting one informal process that everyone already follows.

6. When the agent cannot change organization directly.
   Name the organizational constraint explicitly in the output. Recommend the best technical solution that works within the current relations. Note what organizational change would unlock a better solution, so the information is available for whoever can act on it.

## Scenario 7: Incident Response And Production Debugging

Use this mode when a production system is failing and time pressure demands action before full understanding is available.

Procedure:

1. Triage: define what must be true for the incident to be contained.
   Not "understand the root cause" but "stop the bleeding." The practical objective under time pressure is stabilization, not comprehension. Name the observable threshold for containment: error rate below X, latency below Y, service responding again.

2. Assess the trajectory, not just the state.
   Is the situation degrading, stable, or recovering? A stable degradation affords time to investigate. A rapidly worsening situation demands immediate rollback or mitigation before diagnosis (发展的观点).

3. Distinguish what you know from what you assume.
   Under time pressure, assumptions multiply. Explicitly separate confirmed facts (metrics, logs, recent deployments) from hypotheses. Act on the most likely hypothesis but do not treat it as confirmed.

4. Decide: rollback, mitigate, or fix forward.
   This is a classification of the contradiction:
- If the cause is known and reversible (recent deployment, config change): rollback. Non-antagonistic contradiction with the current state.
- If the cause is unknown but the blast radius can be contained (circuit breaker, feature flag, traffic shift): mitigate. Buy time without requiring full understanding.
- If the cause is understood and a forward fix is smaller than rollback: fix forward. But only when confidence is high.

5. Trace connections during the incident.
   Ask: what else depends on the failing component? What downstream systems are affected? What human processes are disrupted? This determines communication priority and blast radius (普遍联系).

6. After stabilization, return to full method.
   The incident triage was necessarily shallow. Now apply the complete working method: reproduce the root cause, identify the structural contradiction that made this incident possible, assess whether accumulated incidents indicate a qualitative threshold (量变质变), and ensure the postmortem produces understanding, not just a timeline.

7. Treat the postmortem as mass line practice.
   Gather experience from everyone involved: on-call engineers, affected users, adjacent team members. Synthesize their scattered observations into a structural diagnosis. Return the diagnosis for validation: "Does this match what you experienced?" The postmortem fails if it only reflects the incident commander's perspective.

Output shape:
- containment objective and threshold
- trajectory assessment (stable / degrading / recovering)
- confirmed facts vs hypotheses
- action taken (rollback / mitigate / fix forward) with justification
- blast radius and connections traced
- root cause analysis (after stabilization)
- structural contradiction exposed
- preventive recommendation

## Scenario 8: Legacy System Migration

Use this mode when migrating from an old system to a new one while maintaining service continuity.

Procedure:

1. Understand why the old system is what it is.
   Before designing the new system, analyze the conditions that produced the old one. What constraints shaped its architecture? What hard-won knowledge is embedded in its edge cases, workarounds, and operational runbooks? Teams do not build bad systems out of ignorance—they build systems that are rational given their conditions at the time (社会存在决定社会意识).

2. Inventory what must be preserved.
   List the concrete behaviors, guarantees, and operational properties the old system provides. Include undocumented behaviors that practitioners depend on. A migration that loses battle-tested properties is regression, not progress (否定之否定: transcend, do not regress).

3. Identify the principal contradiction of the migration.
   Common candidates:
- continuity vs progress (keep the old running while building the new)
- knowledge transfer vs delivery speed (understanding the old system vs shipping the new one)
- user trust vs system change (maintaining confidence during transition)
- old system entropy vs new system readiness (the old system degrades while waiting for the new one)

4. Classify migration contradictions.
   Which tensions can be mediated (non-antagonistic) and which require structural breaks (antagonistic)? For example:
- Data model incompatibility may be antagonistic: you cannot run both schemas forever; at some point, a cutover must happen.
- User workflow changes may be non-antagonistic: gradual introduction, parallel paths, and education can mediate the transition.

5. Plan in phases with qualitative checkpoints.
   Do not plan a big-bang migration unless the contradiction is truly antagonistic and cannot be decomposed. Prefer staged migration with checkpoints:
- Phase 1: Parallel operation (both systems running, new system receiving shadow traffic)
- Phase 2: Gradual cutover (increasing traffic to new system, monitoring for behavioral differences)
- Phase 3: Old system sunset (after confidence threshold reached)
   At each phase boundary, reassess: has the trajectory justified proceeding, or has new evidence changed the principal contradiction?

6. Monitor the portfolio of migration contradictions.
   Migrations are particularly vulnerable to secondary contradiction escalation:
- While focusing on technical migration, team knowledge of the old system erodes
- While building the new system, the old system accumulates debt faster (because investment stopped)
- While managing the transition, feature delivery stalls and stakeholder patience depletes
   Track each of these trajectories. If any approaches a critical threshold, adjust proportions (论十大关系).

7. Verify with practitioners at every phase.
   The people who operate the old system know its real behavior. The people who will operate the new system need to validate that it meets their needs. Both groups must be consulted throughout the migration, not just at the beginning and end (群众路线).

8. Define the point of no return explicitly.
   At some point, rolling back becomes more expensive than pushing forward. Name this point in advance, with specific criteria. When you cross it, acknowledge the qualitative shift and adjust the plan accordingly (量变质变).

Output shape:
- old system conditions and embedded knowledge
- preservation inventory (what must survive)
- principal migration contradiction
- contradiction classifications (antagonistic / non-antagonistic)
- phased plan with checkpoints
- secondary contradiction portfolio and monitoring plan
- practitioner validation plan
- point-of-no-return criteria

## Failure Modes To Avoid

- Dogmatism: forcing a favored pattern onto the repo despite contrary evidence.
- Empiricism without synthesis: collecting many facts but never naming the governing contradiction.
- Equal treatment of all issues: generating a flat task list with no principal contradiction.
- Detached implementation: writing code before reproducing, reading, or understanding constraints.
- Formal completion: claiming success because code exists even when practice has not verified it. Tests passing is not the same as the real problem being solved.
- Mechanical repetition: debugging the same way for the third time without shifting the level of analysis. Each cycle must solve a higher-order problem than the last.
- Pattern cargo-culting: adopting an approach because it worked elsewhere without verifying that the specific conditions hold here.
- Ignoring organizational constraints: proposing technically correct solutions that the current team structure cannot execute.
- Premature restructuring: attempting a qualitative intervention (rewrite, re-architecture) before quantitative accumulation has reached the threshold that justifies it.
- Threshold blindness: continuing to apply incremental patches after the system has already undergone a qualitative shift, making patches ineffective.
- Aggregation without synthesis: listing practitioner feedback without extracting the structural pattern.
- Misclassifying contradiction types: treating an antagonistic contradiction (fundamental incompatibility) as non-antagonistic (adjustable tension) leads to endless fruitless mediation. The reverse leads to unnecessary disruption when adjustment would suffice.
- Ignoring connections: changing a component without tracing what depends on its behavior, then being surprised by downstream failures.
- Snapshot thinking: assessing a system only by its current state without checking whether it is improving, degrading, or stagnant. Direction and rate of change determine urgency.
- Blaming practices without examining conditions: judging a team's approach without understanding the constraints that make it locally rational. Change conditions to change practices.
- Serial focus without portfolio awareness: attacking one contradiction to completion while secondary contradictions silently reach crisis levels.

## Decision Heuristics

- If evidence is thin, investigate before designing.
- If many issues exist, choose the one that most determines movement.
- If a clean redesign is tempting, compare it to the smallest effective intervention.
- If tests pass but user value is unchanged, return to the practical objective.
- If a plan becomes stale after new evidence, rewrite the plan.
- If the same fix has been applied N times to the same area, ask whether the area needs structural change, not another patch.
- If a proven pattern from another project is being adopted, list its preconditions and verify each one holds here.
- If a technically sound proposal keeps stalling, examine whether the blocker is organizational rather than technical.
- If practitioners report that the fix did not help, trust their experience over the test suite.
- If each iteration of a solution resembles the previous one, shift to a higher level of abstraction.
- If secondary contradictions are accumulating while you focus on the principal one, check whether any secondary contradiction is about to become principal.
- If a tension keeps returning after repeated mediation, consider whether it is antagonistic and requires structural change rather than further adjustment.
- If a change will touch a widely-connected component, map at least one level of indirect dependencies before acting.
- If two systems are at the same quality level, check their trajectories: improving rapidly vs degrading slowly demand very different responses.
- If a team resists a proposed change, ask what conditions make their current approach rational before assuming the resistance is irrational.
- If under time pressure (incidents), stabilize first, understand second. But always return to full analysis after stabilization.
- If migrating a legacy system, inventory what the old system got right before designing the new one. Regression disguised as modernization is still regression.
