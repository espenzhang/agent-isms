# Ten Relations: Engineering Extraction From 《论十大关系》

## Scope

This file distills engineering-useful principles from Mao Zedong's *On the Ten Major Relationships* (《论十大关系》), which addresses how to balance multiple competing priorities simultaneously rather than focusing on one at the expense of all others. Use it when the host agent faces a portfolio of contradictions that must be managed concurrently—when solving the principal contradiction risks neglecting secondary ones that may escalate.

## Source Read

- 毛泽东《论十大关系》(1956):
  https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19560425.htm

## Core Method

1. Multiple contradictions coexist and interact.
   In any real project, there is never just one tension. Feature delivery, code quality, operational stability, team health, user experience, security posture, and infrastructure investment all compete for attention simultaneously.

2. The principal contradiction gets primary attention, not exclusive attention.
   Finding the principal contradiction means allocating disproportionate effort to it—not ignoring everything else. Secondary contradictions managed at low cost prevent them from escalating into principal ones.

3. Each relation has its own correct proportion.
   Balance is not equal allocation. The correct proportion for each competing priority depends on the current stage of the project, the trajectory of each dimension, and the cost of neglect.

4. Neglect of secondary contradictions creates cascading crises.
   Ignoring team health while shipping features works until the team burns out. Ignoring tech debt while adding features works until velocity collapses. The crisis appears sudden but was produced by sustained neglect.

5. Proportions must be reassessed periodically.
   The correct balance last quarter may be wrong this quarter. As the principal contradiction shifts, the portfolio of secondary contradictions also shifts. Rebalancing is a regular activity, not an exception.

## Engineering Relations To Balance

The following are common engineering relations that must be managed simultaneously. The specific set and proportions depend on the concrete conditions of each project.

1. **Feature delivery vs code quality**: Ship features to create value; maintain quality to sustain velocity. Neither extreme is viable.

2. **Speed vs stability**: Move fast to capture opportunities; ensure reliability to retain trust. The correct proportion depends on the product's maturity and user tolerance.

3. **New development vs debt reduction**: Build new things to grow; reduce debt to maintain capability. Allocating zero effort to either is unsustainable.

4. **Individual team autonomy vs system-wide consistency**: Allow teams to move independently; maintain enough consistency for integration. The balance depends on coupling between teams' domains.

5. **Infrastructure investment vs immediate feature work**: Build infrastructure to enable future work; deliver features to demonstrate present value. Infrastructure without users is waste; features without infrastructure create fragility.

6. **Depth vs breadth of testing**: Test critical paths deeply; cover broad surface area thinly. Complete coverage of everything is infeasible; testing nothing is reckless.

7. **Documentation vs doing**: Document to share knowledge; do to create value. Over-documentation slows progress; under-documentation creates bus factor risk.

8. **Centralized control vs distributed decision-making**: Centralize for consistency; distribute for speed. The balance depends on how much coordination cost the organization can absorb.

9. **User-facing work vs operator-facing work**: Build features users see; improve tools operators need. Neglecting operators makes features unreliable; neglecting features makes operations pointless.

10. **Current architecture vs future architecture**: Optimize for today's constraints; prepare for tomorrow's growth. Over-preparation is premature; zero preparation is shortsighted.

## Engineering Translation

- At the beginning of each planning cycle, list the active relations (not just tasks or stories). For each relation, assess: what is the current proportion? What is the trajectory? Is neglect of either side approaching a critical threshold?
- Set explicit minimums for secondary priorities. Example: "We will allocate at least 15% of sprint capacity to debt reduction, regardless of feature pressure." This prevents cascading neglect.
- Monitor for early warning signs of secondary contradictions escalating:
  - Rising incident count → stability neglected
  - Declining velocity → debt or quality neglected
  - Increasing on-call burden → operator tooling neglected
  - Team attrition → team health neglected
  - Increasing bug reports → testing neglected
- When a secondary contradiction shows accelerating degradation, elevate it proactively rather than waiting for crisis.
- Accept that perfect balance is impossible. The goal is sustainable imbalance: consciously favoring one side while keeping the other side above its minimum viable level.

## What This Means For Agent Behavior

When planning work:
- Do not produce a task list organized only by the principal contradiction. Include at least one task addressing the most at-risk secondary contradiction. Justify the proportion.

When assessing project health:
- Report on multiple dimensions, not just the current focus area. "Feature delivery is on track, but incident frequency has risen 40% over three sprints and debt reduction has received no allocation for two cycles."

When the principal contradiction is resolved or weakened:
- Immediately reassess the portfolio. The next principal contradiction is likely one of the secondary ones that was accumulating during the previous focus period.

When recommending priorities:
- State what you are recommending to deprioritize and what the cost of that deprioritization is. "Recommend focusing on stability this sprint. Cost: feature X slips one sprint. Risk of not acting: incident trend suggests a major outage within two sprints."

## Common Mistakes Through This Lens

- Serial focus: attacking one contradiction completely before touching any other, allowing secondary contradictions to reach crisis.
- Equal allocation: dividing effort equally across all priorities regardless of urgency, trajectory, or impact—this is not balance, it is diffusion.
- Invisible neglect: not tracking secondary contradictions at all, so their degradation is only noticed when it becomes a crisis.
- Reactive rebalancing: only adjusting proportions after a crisis forces it, rather than monitoring trajectories and adjusting proactively.
- Confusing proportion with priority: "Feature work is our priority" does not mean "zero effort on anything else." Priority sets the dominant allocation; proportion sets the minimum for everything else.

## Short Prompts This Reference Supports

- "What secondary contradictions are we neglecting while focusing on the principal one?"
- "What is the minimum viable allocation for each competing priority this cycle?"
- "Which secondary contradiction is closest to becoming principal?"
- "What are we consciously deprioritizing, and what is the cost of that choice?"
- "Has our balance of priorities shifted since last cycle? Should it?"
