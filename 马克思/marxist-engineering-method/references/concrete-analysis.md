# Concrete Analysis: Engineering Extraction From 列宁"具体问题具体分析"

## Scope

This file distills engineering-useful principles from Lenin's insistence on concrete analysis of concrete conditions (具体问题具体分析), which he described as the living soul of Marxism. Use it when the host agent faces pressure to apply generic patterns, "best practices," or borrowed solutions without verifying that the specific conditions of the current project justify them.

## Source Read

- 列宁《共产主义》(1920), 关于"对具体情况的具体分析是马克思主义的活的灵魂":
  https://www.marxists.org/chinese/lenin/erta/index.htm
- 列宁《论策略书》(1917), 关于具体分析的方法:
  https://www.marxists.org/chinese/lenin/erta/index.htm
- 毛泽东《矛盾论》第五节"矛盾的特殊性":
  https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19370801.htm

## Core Method

1. Every situation has its own specific conditions.
   No two codebases, teams, deployment environments, or user populations are identical. Solutions that worked elsewhere worked because of their specific conditions, not because they are universally correct.

2. General principles require concrete application.
   "Use caching to reduce latency" is a general principle. Whether to cache, what to cache, where to cache, and how to invalidate depends entirely on this system's access patterns, consistency requirements, data staleness tolerance, and operational capacity.

3. Borrowing requires re-derivation, not copying.
   When adopting a pattern from another project, re-derive it: What problem did it solve there? What conditions made it work? Do those conditions hold here? If not, what would need to change?

4. "Best practice" is a hypothesis, not a conclusion.
   Industry standards, framework recommendations, and team conventions are accumulated experience condensed into general rules. They are starting points for analysis, not substitutes for it. Applying them without checking fit is dogmatism.

5. The specific contradiction determines the specific solution.
   Two systems may both have "performance problems," but one may need query optimization while the other needs architectural decomposition. The general category (performance) does not determine the concrete intervention.

## Engineering Translation

- Before adopting any pattern, tool, or approach, list the conditions under which it succeeds. Then verify which of those conditions hold in the current project. Missing conditions are not minor caveats—they are reasons the pattern may fail.
- When someone says "we should use X because company Y does," ask: What is company Y's traffic pattern? Team size? Deployment cadence? Data model? If you cannot answer, you cannot justify the adoption.
- Treat metrics targets as context-dependent. "80% test coverage" means different things for a safety-critical payment service and an internal admin tool. "Sub-100ms latency" matters differently for a real-time game and a batch reporting system.
- When a standard approach fails, do not assume the implementation is wrong. The approach itself may not fit the conditions. Investigate the fit before retrying harder.
- Derive conventions from the actual codebase, not from external authority. If the project uses pattern A consistently and it works, switching to pattern B because a blog post recommends it is not improvement—it is disruption without justification.

## What This Means For Agent Behavior

When the agent considers using a common pattern:
- State the conditions the pattern assumes. Check each condition against the current project. Proceed only if the conditions hold or can be made to hold at reasonable cost.

When the agent encounters a failed approach:
- Before concluding "we did it wrong," ask "was this the right approach for these conditions?" Correctly implementing the wrong approach is still wrong.

When the agent reads external documentation or recommendations:
- Treat all external advice as general principles requiring concrete analysis. "Use connection pooling" is advice. "Use connection pooling with these settings for this traffic pattern" is concrete application.

When the agent must justify a decision:
- Ground justification in the specific conditions of this project, not in general authority. "We use retry logic because our upstream has measured 2% transient failures at peak" is concrete. "We use retry logic because it's best practice" is dogmatic.

## Common Mistakes Through This Lens

- Cargo-culting: adopting patterns because successful projects use them, without understanding the conditions that make them work.
- Metric dogmatism: optimizing for a number (coverage, latency, uptime) without asking whether that number is the right measure for this specific system's actual failure modes.
- Pattern loyalty: continuing to apply a pattern that was correct six months ago without re-examining whether conditions have changed.
- Authority substitution: "The documentation says X" or "The industry standard is Y" used as arguments without concrete analysis of fit.
- Premature generalization: solving one instance of a problem and immediately abstracting it into a framework, before encountering enough concrete cases to know what the general form actually is.

## Short Prompts This Reference Supports

- "What specific conditions make this pattern work? Do they hold here?"
- "Are we adopting this because it fits, or because it's popular?"
- "What is the actual failure mode we're trying to prevent in this specific system?"
- "Has this approach been re-derived for our conditions, or just copied?"
- "What would need to be true for this best practice to apply here?"
