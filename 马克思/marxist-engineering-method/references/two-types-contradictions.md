# Two Types of Contradictions: Engineering Extraction From 《关于正确处理人民内部矛盾的问题》

## Scope

This file distills engineering-useful principles from Mao Zedong's distinction between antagonistic and non-antagonistic contradictions (对抗性矛盾与非对抗性矛盾). Use it when the host agent must decide whether a tension can be resolved through adjustment and compromise, or whether it requires structural confrontation and fundamental change.

## Source Read

- 毛泽东《关于正确处理人民内部矛盾的问题》(1957):
  https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19570227.htm
- 《矛盾论》第七节"对抗在矛盾中的地位":
  https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19370801.htm

## Core Method

1. Not all contradictions are the same kind.
   Some contradictions can be resolved within the existing framework through discussion, adjustment, and proportion. Others cannot—they require the framework itself to change.

2. Non-antagonistic contradictions are resolved through mediation.
   Both sides share a common foundation and can be balanced. The resolution preserves the structure while adjusting proportions, priorities, or processes. These contradictions are normal and healthy—their management is ongoing work, not a crisis.

3. Antagonistic contradictions are resolved through structural transformation.
   The opposing sides are fundamentally incompatible within the current framework. Compromise postpones but does not resolve the tension. Continued compromise leads to system degradation. Resolution requires changing the framework: restructuring, replacing, or removing one side of the contradiction.

4. Non-antagonistic contradictions can become antagonistic if mishandled.
   Ignoring a manageable tension, refusing to adjust, or letting imbalance grow can transform a non-antagonistic contradiction into an antagonistic one. Early mediation prevents escalation.

5. Antagonistic contradictions can be misidentified as non-antagonistic.
   Treating a fundamental incompatibility as a matter of adjustment and compromise wastes effort and delays necessary structural change. The symptom: you keep mediating, but the tension keeps returning or worsening.

## Engineering Translation

- **Non-antagonistic contradictions** (mediate, adjust, balance):
  - Speed vs thoroughness in a sprint: adjust by allocating time boxes, staging work, or scoping PRs.
  - Team style differences: resolve through shared conventions, linting rules, or documented decisions.
  - Feature priority disagreements: resolve through user data, stakeholder alignment, or experimentation.
  - Short-term vs long-term tradeoffs: resolve through staged delivery, tech debt budgets, or time-boxed refactoring.
  - Different module patterns coexisting: resolve through gradual convergence, not forced migration.

- **Antagonistic contradictions** (confront, restructure, replace):
  - Architecture that fundamentally cannot scale to meet requirements: no amount of optimization fixes this; redesign is needed.
  - Ownership model that structurally blocks necessary changes: process improvements cannot fix a structural misalignment; ownership must be redrawn.
  - Test suite that passes but does not verify actual behavior: adding more of the same tests does not help; the testing approach itself must change.
  - Deployment process that structurally prevents safe rollback: no amount of care within the process fixes it; the process must be replaced.
  - Two teams with structurally incompatible incentives working on the same system: coordination improvements cannot resolve an incentive misalignment; the incentive structure or team boundaries must change.

- **How to distinguish them**:
  - Ask: "If we adjust proportions or processes within the current structure, can this tension be sustainably managed?" If yes, it is non-antagonistic.
  - Ask: "Have we tried mediating this multiple times, and does it keep returning or worsening?" If yes, it may be antagonistic—the structure itself is the problem.
  - Ask: "Does resolving this tension require changing only how much or when, or does it require changing what or who?" If the latter, it is likely antagonistic.

## What This Means For Agent Behavior

When mapping contradictions:
- Classify each contradiction as antagonistic or non-antagonistic before choosing a resolution form. This classification determines whether to mediate or restructure.

When proposing solutions:
- For non-antagonistic contradictions: propose adjustments, conventions, process changes, or proportional rebalancing. These are ongoing maintenance, not permanent fixes.
- For antagonistic contradictions: propose structural changes. Name what must be replaced, removed, or fundamentally redesigned. Note: this is usually more expensive and disruptive—justify it with evidence that mediation has failed or cannot succeed.

When mediating keeps failing:
- If the same contradiction has been "resolved" multiple times and keeps returning, upgrade the classification. It is likely antagonistic, and mediation is postponing necessary structural change at increasing cost.

When proposing structural change:
- Verify that the contradiction is truly antagonistic. A premature structural intervention against a non-antagonistic contradiction is wasteful disruption—like rewriting a module when a configuration change would suffice.

## Common Mistakes Through This Lens

- Treating all contradictions as antagonistic: overreacting to normal tensions with dramatic restructuring when adjustment would suffice.
- Treating all contradictions as non-antagonistic: endlessly compromising and mediating when the system fundamentally cannot accommodate both sides.
- Escalation through neglect: allowing a non-antagonistic contradiction to grow unmanaged until it becomes antagonistic. Preventable through early, proportional intervention.
- Mis-diagnosis by analogy: assuming a contradiction is the same type as a similar-looking one in another project. The type depends on this system's specific structure, not on surface similarity.

## Short Prompts This Reference Supports

- "Can this tension be managed within the current structure, or does the structure need to change?"
- "Have we tried mediating this before? Did it stick, or did the tension return?"
- "Is this a problem of proportion (how much) or a problem of kind (what)?"
- "Are we treating a structural incompatibility as an adjustment problem?"
- "Is this tension normal and ongoing, or is it a sign that something fundamental must change?"
