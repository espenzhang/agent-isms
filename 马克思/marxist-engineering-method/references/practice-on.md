# Practice On: Engineering Extraction From 《实践论》

## Scope

This file distills engineering-useful principles from Mao Zedong's 《实践论》 for agent work. Use it when the host agent needs a deeper grounding for investigation, execution, verification, and iterative learning.

## Source Read

- 《实践论》, 华南理工大学页面转载全文: https://www2.scut.edu.cn/party_org/2012/1229/c3210a67040/page.htm

## Core Method

1. Knowledge begins in practice.
   In engineering, begin from the codebase, tests, runtime behavior, user reports, and operating constraints rather than from abstract preference.

2. Move from perceptual knowledge to rational knowledge.
   Raw observations are not enough. Convert logs, file reads, and failures into an explanation of structure, cause, and likely leverage points.

3. Return rational knowledge to practice.
   A conclusion is incomplete until it is tested in action: edit the code, run the test, observe the output, or compare before-and-after behavior.

4. Repeat the cycle.
   Practice produces knowledge; knowledge guides new practice. After each round, update the model of the problem instead of defending the first theory.

## Engineering Translation

- Inspect before proposing.
- Reproduce before fixing.
- Validate after changing.
- Extract pattern after each experiment.
- Prefer conclusions supported by behavior, not preference.

## What This Means For Agent Behavior

When investigating:
- Collect direct evidence first.
- Avoid long speculative plans before seeing concrete artifacts.

When implementing:
- Tie each code change to a stated hypothesis about behavior.
- Prefer small, legible changes that can be checked quickly.

When testing:
- Treat testing as the return of knowledge to practice, not as a ceremonial final step.
- If verification is partial, say exactly what was and was not tested.

## Common Mistakes Through This Lens

- Mistaking documentation for reality when the running system differs.
- Mistaking intuition for knowledge when no observation supports it.
- Mistaking a patch for success when the real-world failure mode was not rechecked.
- Mistaking one successful experiment for a complete understanding.

## Short Prompts This Reference Supports

- "What concrete evidence do I need before designing a fix?"
- "What experiment would most cheaply improve understanding?"
- "What did this implementation actually prove?"
- "What remains unverified in practice?"
