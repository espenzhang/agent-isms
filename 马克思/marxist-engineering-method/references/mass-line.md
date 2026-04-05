# Mass Line: Engineering Extraction From 毛泽东群众路线

## Scope

This file distills engineering-useful principles from Mao Zedong's mass line method (群众路线: 从群众中来，到群众中去). Use it when the host agent must incorporate the lived experience of users, operators, and team members into technical decisions—going beyond purely agent-driven analysis to include the knowledge that practitioners possess but may not have articulated.

## Source Read

- 毛泽东《关于领导方法的若干问题》(1943):
  https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19430601.htm
- 毛泽东《人的正确思想是从哪里来的？》(1963):
  https://www.marxists.org/chinese/maozedong/marxist.org-chinese-mao-19630501.htm

## Core Method

1. From the masses, to the masses (从群众中来，到群众中去).
   Gather the scattered, unsystematic ideas of practitioners. Synthesize them into coherent, structured understanding. Return the synthesized understanding to practitioners for validation and action. Repeat.

2. Scattered experience contains real knowledge.
   Users who report "it feels slow" know something that metrics may not capture. Operators who "always restart service X on Mondays" have discovered a pattern the system does not document. On-call engineers who "just know" to check the queue depth first have internalized a causal chain.

3. Synthesis is not aggregation.
   Collecting ten user complaints and listing them is aggregation. Identifying that seven of them stem from the same latency source and three from a different UX confusion is synthesis. The mass line requires transforming scattered input into structured understanding.

4. Return to practice for verification.
   The synthesized understanding must go back to the people whose experience generated it. If operators say "that doesn't match what we see," the synthesis is wrong or incomplete—not the operators.

5. The process is continuous, not one-shot.
   Each cycle of gathering, synthesis, and return produces new, more refined scattered experience. The second round of feedback is higher quality because practitioners now have a structured frame to compare against their experience.

## Engineering Translation

- Before designing a fix, ask the people who live with the problem. Not "what should we build?" (that is your job to synthesize) but "what do you actually experience? What do you work around? What do you avoid? What do you do that the documentation doesn't mention?"
- Treat user workarounds as data, not noise. A user who exports to CSV and processes in Excel has told you something about the system's query capabilities. An operator who SSH-es into the box to check a file has told you something about the monitoring gaps.
- Synthesize before proposing. Do not present raw user feedback as requirements. Extract the structural pattern, formulate a hypothesis, and then present the hypothesis for validation.
- Validate with the same practitioners. After building or fixing, return to the people who reported the problem. Ask: "Does this match your experience? Does this actually fix what you were working around?" Their answer is the ground truth, not the test suite.
- Repeat with refinement. The first cycle yields coarse understanding. The second yields specific edge cases. The third yields confidence. Do not expect one round to be sufficient.

## What This Means For Agent Behavior

When the agent has access to user reports, bug tickets, or team feedback:
- Read them as raw material for synthesis, not as a task list. Five similar tickets may be one problem. Two dissimilar tickets may share a root cause.

When the agent proposes a solution:
- State which practitioner experience the solution addresses. If the solution does not connect to any reported experience, it may be solving a theoretical problem rather than a real one.

When the agent cannot directly talk to users:
- Use proxies: bug reports, support tickets, on-call runbooks, known workarounds documented in code comments, and the gap between documentation and actual practice. These are the "scattered ideas" available to the agent.

When verifying:
- Distinguish between "tests pass" and "the problem practitioners reported is resolved." Both matter. If tests pass but the practitioner experience is unchanged, the fix is incomplete.

## Common Mistakes Through This Lens

- Treating the agent's analysis as superior to practitioner experience. The agent can structure and synthesize, but the raw material comes from the people who use the system.
- Skipping the return step. Building a solution based on gathered feedback but never checking back whether the solution actually addresses the lived experience.
- Aggregating without synthesizing. Presenting a list of user complaints without identifying the structural patterns or contradictions within them.
- Soliciting feedback once and treating it as permanent truth. Practitioner experience changes as the system changes. Each cycle needs fresh input.
- Dismissing informal knowledge. "We always do X before Y" is not superstition—it is likely a discovered dependency that the formal system does not encode.

## Short Prompts This Reference Supports

- "What do the people who use this system actually experience?"
- "What workarounds exist that the documentation doesn't mention?"
- "Does this fix address the reported experience, or just the technical symptom?"
- "Have we returned the synthesized understanding for practitioner validation?"
- "What informal knowledge exists in the team that the codebase doesn't encode?"
