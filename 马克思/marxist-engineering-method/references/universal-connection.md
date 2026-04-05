# Universal Connection and Development: Engineering Extraction From 唯物辩证法基本特征

## Scope

This file distills engineering-useful principles from two foundational features of materialist dialectics: universal connection (普遍联系) and perpetual development (永恒发展). Use it when the host agent must trace how changes propagate through interconnected systems, predict unintended consequences, or evaluate a system by its trajectory rather than a single snapshot.

## Source Read

- 恩格斯《反杜林论》第一编"世界模式论" 关于普遍联系:
  https://www.marxists.org/chinese/engels/erta/index.htm
- 恩格斯《自然辩证法》"辩证法" 关于联系与发展:
  https://www.marxists.org/chinese/engels/dialectics-of-nature/index.htm
- 列宁《谈谈辩证法问题》:
  https://www.marxists.org/chinese/lenin/erta/index.htm

## Core Method

### Universal Connection (普遍联系)

1. Nothing exists in isolation.
   Every component in a system is connected to others through dependencies, data flows, shared resources, human processes, and organizational structures. A change to one component is a change to the system.

2. Connections are objective and discoverable.
   Dependencies are not opinions—they are structural facts. Trace them through imports, API calls, shared databases, deployment pipelines, team communication paths, and user workflows.

3. Direct and indirect connections both matter.
   A module's direct dependencies are obvious. Its indirect effects—on downstream consumers, on operator workflows, on team cognitive load, on deployment cadence—are less visible but often more consequential.

4. The form of connection matters, not just its existence.
   Two modules may both depend on a database, but one reads while the other writes. One module's failure may cascade; another's may be safely isolated. Understand the type and strength of each connection.

### Perpetual Development (永恒发展)

5. Every system is in motion.
   No codebase, team, or service is static. It is either improving, degrading, or shifting character. A point-in-time assessment misses the direction and rate of change.

6. Evaluate trajectory, not just state.
   A system at 60% test coverage and rising is in a different situation than one at 60% and falling. The number is the same; the condition is not. Decision-making must account for direction.

7. Rate of change matters as much as direction.
   A slowly degrading system may tolerate delay. A rapidly degrading system demands immediate intervention. A rapidly improving system may not need the intervention you planned last week.

8. Transformation is inevitable.
   The current state of any system is temporary. Design decisions, team structures, and processes will need to change. Build with awareness that what you create will be superseded—this is not failure, it is the nature of development.

## Engineering Translation

### Connection Mapping

- Before making a change, trace its connections: What calls this code? What reads from this data store? What team processes depend on this behavior? What user workflows pass through here? What monitoring or alerting depends on the current behavior?
- Categorize connections by propagation risk: Which connections will propagate a failure? Which will propagate a behavior change? Which will propagate a latency increase? Not all connections carry the same risk.
- Identify hidden connections: Shared configuration files, implicit ordering assumptions, runtime feature flags, cron job schedules, and cache invalidation patterns are connections that may not appear in import graphs.
- When estimating blast radius, include human connections: Will this change affect who gets paged? Will it change what operators must know? Will it change which runbook is relevant?

### Trajectory Assessment

- When assessing a system, always ask: "Is this getting better, worse, or staying the same? How fast?" Before intervening, know the trend.
- Use historical data to establish trajectory: incident frequency over time, patch frequency to a module, code churn rates, test coverage trends, deployment frequency trends, on-call burden trends.
- Interventions should be proportional to trajectory: a system degrading slowly needs different urgency than one degrading rapidly, even if they are currently at the same state.
- After intervention, track whether the trajectory changed. If the trajectory did not change, the intervention addressed a symptom, not a cause.

## What This Means For Agent Behavior

When planning a change:
- Map at least one level of indirect connections before acting. Not just "what does this module call?" but "what calls the modules that call this one?" and "what human processes depend on this behavior?"
- Ask: "If this change introduces a subtle behavior difference, where would it surface first? Who would notice?" That is where verification should focus.

When investigating a failure:
- Do not assume the failing component is the cause. Trace connections upstream: what changed recently in components that feed into this one? What shared resources may have shifted?

When evaluating system health:
- Present assessment as trajectory, not snapshot. "Module X has had 3, 5, and 8 patches in the last three sprints—the trend is accelerating" is more useful than "Module X has 8 patches this sprint."
- Use trajectory to set urgency: accelerating degradation is more urgent than stable degradation, even if absolute levels are similar.

When recommending whether to act now or later:
- Check the trajectory. If the situation is stable or improving, waiting for more evidence may be wise. If it is degrading and accelerating, delay increases cost. Trajectory determines the option value of waiting.

## Common Mistakes Through This Lens

- Treating components as isolated: changing a module without tracing what depends on its behavior.
- Snapshot assessment: evaluating a system's health at one point in time without asking about direction and rate of change.
- Ignoring indirect connections: accounting for direct callers but missing shared databases, configuration, or human workflows.
- Assuming stability: treating the current state as permanent rather than as a phase in ongoing development.
- Confusing activity with progress: making changes without verifying that the trajectory actually improved.
- Optimizing locally while degrading globally: improving one module's performance while increasing latency for its downstream consumers.

## Short Prompts This Reference Supports

- "What is connected to this component that we haven't accounted for?"
- "If this change has a subtle side effect, where would it surface first?"
- "Is this system improving, degrading, or stable? How fast?"
- "Does the trajectory justify acting now, or can we wait for more evidence?"
- "Did our intervention change the trend, or just the current number?"
- "What human processes depend on the behavior we're about to change?"
