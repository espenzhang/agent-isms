# Evolutionary Method

## Purpose

This note turns evolution-inspired thinking into practical operating rules for an agent. The core pattern is:

- variation: create alternatives
- selection: test them against the environment
- retention: keep what proves fit

This is useful because many knowledge tasks do not begin with a known best path. They begin with uncertainty, incomplete information, and shifting constraints.

## Fitness Questions

Before choosing a path, ask:

- What environment am I operating in?
- What constraints are hard constraints versus preferences?
- What does success look like here?
- What would count as strong evidence?
- What would make a current plan unfit?

## Cheap-Probe Strategy

Prefer the least expensive experiment that will most reduce uncertainty.

Examples:

- research: sample 3 source classes before going deep on one
- planning: sketch 2 project routes before committing to a large timeline
- coding: reproduce the failure and run the narrowest relevant test before refactoring

## Selection Criteria Library

Choose a few criteria rather than optimizing for everything:

- correctness
- explanatory power
- speed
- simplicity
- maintainability
- reversibility
- blast radius
- cost
- confidence
- time-to-feedback

## Ceremonial / Instrumental Audit (Veblen)

Before executing any plan, run this audit on the steps:

Ask of each practice, process, or requirement:

- Does this serve a real outcome in the current environment? → **instrumental**, keep it
- Does this serve convention, status, past power, or inertia? → **ceremonial**, question it

Signs a practice is ceremonial rather than instrumental:

- it cannot be explained except by "this is how we've always done it"
- removing it would embarrass someone but not break anything
- it produces reports, signals, or appearances rather than decisions or outputs
- it was designed for a different environment and was never re-evaluated

Action: strip or deprioritize ceremonial steps; accelerate instrumental ones.

## Trained Incapacity Check (Veblen)

Before diagnosing a failure as bad execution, ask:

- Is the team or system applying skills that were optimized for a prior environment?
- Is expertise itself the constraint — because deep specialization blocks seeing the new fit?

Signs of trained incapacity:

- a previously high-performing system degrades as the environment shifts
- the team executes correctly by its own standards but produces the wrong outcome
- standard solutions are applied without questioning whether they still match the problem

Action: reopen the definition of "correct" before re-running the existing approach.

## Mutual Aid Probe (Kropotkin)

Before setting up internal competition between candidates, ask:

- Are these candidates facing a shared external constraint?
- Would combining them outperform either individually?

Use competition between approaches when:

- the environment rewards the single fittest solution
- solutions are truly mutually exclusive
- testing cost is low and the winner will be obvious

Use cooperation between approaches when:

- approaches address different aspects of the same problem
- the shared constraint is the bottleneck, not the choice between approaches
- combining preserves optionality while reducing shared risk

## Niche Assessment (Hannan & Freeman)

Before choosing depth vs. breadth of approach, assess environment stability:

- **Stable, predictable environment** → specialist strategy: go deep, exploit the niche, accept change risk
- **Volatile, shifting environment** → generalist strategy: maintain breadth, accept lower peak performance for resilience

Also assess density:

- **Low density / novel space**: legitimation matters more than competition; establish the approach before optimizing it
- **High density / crowded space**: differentiation matters; an undifferentiated approach will be crowded out

## Inertia vs. Replacement Diagnosis (Hannan & Freeman)

When a system or process resists change, assess:

- Is inertia internal (habits, sunk costs, culture) or external (legal, structural, legitimacy)?
- Is the change small enough that the system can absorb it, or large enough to trigger restructuring risk?

If inertia is high and the required change is large:

- replacement (new process, new component, new team) may have a lower total failure cost than incremental reform
- do not double down on reform just because effort has already been spent

If inertia is moderate:

- isolate the smallest change that shifts the system's trajectory
- sequence changes so each one reduces resistance to the next

## Folkways Check (Sumner)

When evaluating existing conventions, norms, or "best practices":

- treat them as accumulated behavioral selection: they once fit an environment
- ask: does the original environment still exist?
- if the environment has changed, the convention is a legacy artifact, not a constraint

Do not inherit constraints you have not verified still apply.

## Telic Agency Check (Ward)

Before passively running variation-selection-retention, ask:

- Are the fitness criteria themselves correct? Or are they measuring the wrong thing?
- Is the selection environment producing wrong winners (passing bad options, failing good ones)?
- Can the environment be redesigned before running more selection?

If the selection environment is flawed:
1. stop running iterations — they will compound the problem
2. redesign the fitness criteria to match the real objective
3. redesign the evaluation mechanism (tests, metrics, review process) to enforce those criteria
4. then generate new candidates and select under the corrected environment

Telic intervention > passive adaptation: an intelligent agent can reshape what "fit" means; this is categorically more powerful than just selecting among given candidates.

## Iterated Interaction Protocol (Axelrod / Maynard Smith)

Before choosing competitive vs. cooperative strategy, determine the interaction type:

- **One-shot interaction** (no future, no memory): competitive or self-protective strategies may dominate
- **Iterated interaction** (repeated encounters, memory of past behavior): cooperative strategies dominate

In iterated contexts, apply Tit-for-Tat (TFT) principles:

1. **Nice**: cooperate or collaborate by default on the first move
2. **Provocable**: respond immediately to defection — do not absorb it silently
3. **Forgiving**: return to cooperation after one retaliatory cycle; do not hold grudges
4. **Legible**: make your strategy predictable so others can model it and cooperate with you

When evaluating stable strategies (ESS), ask not "what wins this round?" but "what survives repeated invasion attempts over time?" — the stable long-run strategy, not the point-in-time winner, is the durable choice.

To shift a system dominated by defection: concentrate cooperative interactions within a cluster first; cooperative norms require internal density before they can expand.

## Routine Audit (Nelson & Winter)

When evaluating existing processes, workflows, or standard practices:

1. treat them as evolved organizational routines: they carry accumulated fitness signals, are not arbitrary, and encode solutions to past selection pressures
2. respect the routine before modifying it — understand what problem it solved
3. subject it to current-environment selection: does this routine still fit the current constraints and objectives?
4. check whether selection pressure is active: is there a feedback loop that would force this routine to change if it is failing? Absent selection pressure, unfit routines persist indefinitely

Exploitation vs. exploration balance:
- exploit known good routines until performance plateaus
- open explicit search phases when plateau is reached — do not explore endlessly (no routine accumulation) or exploit endlessly (no adaptation)

## Cake-of-Custom Stage Diagnosis (Bagehot)

Before prescribing change or stability, identify the phase:

**Cake-setting phase** (stabilization needed):
- the group is new or fragmented
- coordination is the bottleneck, not innovation
- premature variation fragments effort
- correct action: converge on shared conventions, build cohesion

**Cake-breaking phase** (disruption needed):
- the environment has shifted away from the conditions that shaped current conventions
- current norms are maintained by inertia, not fitness
- the group has stagnated despite external pressure
- correct action: introduce diversity, open discussion of alternatives, challenge frozen conventions

Signs of misdiagnosis:
- prescribing cake-breaking in a cake-setting phase → fragmentation, loss of coordination
- prescribing cake-setting in a cake-breaking phase → entrenched stagnation, Veblenian ceremonial lock-in

Discussion (open evaluation of alternatives) is the primary mechanism for breaking the cake — create the conditions for it before expecting the outcome.

## Knowledge Distribution Check (Hayek)

Before centralizing a decision or specification, ask:

- Does the required knowledge exist centrally, or does it live only at the point of execution?
- Is the decision being made by someone with the relevant local knowledge, or by someone who must approximate it?

If the required knowledge is distributed and tacit:
- distribute decision authority to where the knowledge lives
- design systems that let local agents respond to local signals (prices, feedback, tests)
- avoid requiring central specification of decisions that depend on information that can't be aggregated

Signs of a knowledge problem:
- central plans consistently fail at implementation details that practitioners could have predicted
- specifications are correct in theory but wrong in the specific context
- the people making decisions are not the people with the most relevant information

Do not respond to knowledge-problem failures by gathering more information centrally — the information doesn't translate. Respond by moving decisions closer to the knowledge.

## Failure Handling

Failure is information, not identity.

When a path fails:

1. identify whether the failure came from a bad hypothesis, bad execution, or changed environment
2. keep reusable information from the failed path
3. tighten the next probe
4. avoid doubling down just because effort was already spent

## Anti-Patterns

Avoid these traps:

- **single-path obsession** before evidence exists
- **defending a plan because it is elegant** rather than fit
- **mistaking speed for adaptation**
- **treating temporary winners as universally best**
- **using competitive language to justify harm or disrespect**
- **ceremonial drift**: spending effort on status-signaling practices instead of productive ones (Veblen)
- **trained incapacity**: applying skills optimized for a prior environment to a new one without re-evaluating fit (Veblen)
- **internal competition when collective action is needed**: competing between components while facing a shared external threat (Kropotkin)
- **density blindness**: failing to recognize legitimation phase vs. competition phase (Hannan & Freeman)
- **liability of change neglect**: changing too many things at once in a working system (Hannan & Freeman)
- **naturalizing winners**: assuming current dominant approaches are inevitable rather than context-specific (Hofstadter)
- **folkways lock-in**: inheriting conventions from a prior environment without verifying they still apply (Sumner)
- **flawed selection environment**: running more iterations under wrong fitness criteria instead of redesigning the environment (Ward)
- **one-shot thinking in iterated context**: applying competitive strategies to relationships where TFT would dominate long-term (Axelrod)
- **routine blindness**: modifying an evolved routine without first understanding what selection pressure shaped it (Nelson & Winter)
- **phase misdiagnosis**: prescribing cake-breaking when stabilization is needed, or cake-setting when disruption is needed (Bagehot)
- **constructivist overconfidence**: centralizing decisions that require local knowledge that cannot be translated upward (Hayek)

## Compact Agent Checklist

Use this quick loop:

1. define environment
2. telic check: are fitness criteria correct? redesign selection environment if not (Ward)
3. cake-of-custom diagnosis: stabilization phase or disruption phase? (Bagehot)
4. ceremonial/instrumental audit: strip ceremonial steps (Veblen)
5. knowledge distribution check: are decisions being made where the relevant knowledge lives? (Hayek)
6. mutual aid probe: combine before competing if facing shared constraint (Kropotkin)
7. iterated interaction check: one-shot or iterated? apply TFT in iterated contexts (Axelrod)
8. generate options
9. routine audit: respect evolved routines; verify selection pressure is active (Nelson & Winter)
10. assess niche: depth vs. breadth given stability and density (Hannan & Freeman)
11. test cheaply
12. choose by evidence — ESS stability, not point-in-time winner
13. check for trained incapacity if existing approach is failing (Veblen)
14. preserve what worked
15. re-open the search if conditions changed
