# Contradiction On: Engineering Extraction From 《矛盾论》

## Scope

This file distills engineering-useful principles from Mao Zedong's 《矛盾论》 for agent work. Use it when the host agent must understand tradeoffs, identify the governing bottleneck, or choose the right form of resolution.

## Source Read

- 《矛盾论》, 求是网《毛泽东选集第一卷》分页全文:
  - https://www.qstheory.cn/books/2019-07/31/c_1119448591_22.htm
  - https://www.qstheory.cn/books/2019-07/31/c_1119448591_23.htm
  - https://www.qstheory.cn/books/2019-07/31/c_1119448591_25.htm
  - https://www.qstheory.cn/books/2019-07/31/c_1119448591_27.htm

## Core Method

1. Contradictions are everywhere.
   Every engineering task contains tensions: speed and quality, coupling and reuse, delivery and stability, simplicity and coverage.

2. Each contradiction is specific.
   Do not solve "performance" or "architecture" in the abstract. Solve the concrete contradiction in this repository, service, team, and release context.

3. Internal causes govern development; external causes condition it.
   External pressure matters, but outcomes are determined mainly by the system's internal structure: data model, ownership, interfaces, tests, and architecture.

4. Find the principal contradiction.
   In a complex situation, one contradiction usually governs the motion of the others. Name it and act on it first.

5. Distinguish the principal aspect.
   Inside one contradiction, one side is dominant at a given moment. This determines the current character of the problem.

6. Expect transformation.
   A secondary issue can become primary after a release, refactor, incident, or requirement change. Re-evaluate after movement.

7. Match the form of resolution to the contradiction.
   Not every contradiction requires confrontation or total replacement. Some need sequencing, mediation, abstraction, interface cleanup, or temporary compromise.

## Engineering Translation

- Do not flatten a problem into a list of equal TODOs.
- Ask what actually determines progress right now.
- Prefer solving the mechanism that shapes many symptoms.
- Re-check whether the dominant side changed after each meaningful step.

## Contradiction Mapping Template

- objective
- opposing forces
- internal structural cause
- external pressures
- principal contradiction
- principal aspect
- possible resolution forms
- smallest decisive next action

## Common Mistakes Through This Lens

- Treating all bugs as equally important.
- Solving visible symptoms while the governing mechanism remains untouched.
- Copying a successful pattern from another codebase without checking this codebase's specific contradictions.
- Choosing the most dramatic intervention instead of the correctly matched one.

## Short Prompts This Reference Supports

- "What is the principal contradiction in this task?"
- "Which side of the contradiction is dominant right now?"
- "What smallest action would materially alter the balance?"
- "Is this a contradiction to resolve by redesign, sequencing, isolation, or compromise?"
