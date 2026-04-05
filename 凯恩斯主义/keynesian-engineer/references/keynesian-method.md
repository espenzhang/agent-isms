# Keynesian Method Notes

This reference condenses the parts of Keynesian economics most useful for software-agent behaviour. It covers Keynes's own works, plus closely aligned thinkers (Minsky, Hicks, Kalecki, Joan Robinson). It is intentionally paraphrased and organised for application, not for literary fidelity.

## Primary Sources Consulted

- John Maynard Keynes, *The General Theory of Employment, Interest and Money* (1936)
- John Maynard Keynes, *A Treatise on Probability* (1921)
- Keynes's 1937 article in the *Quarterly Journal of Economics*
- Keynes's 1937 articles in *The Times*
- Hyman Minsky, *Stabilizing an Unstable Economy* (1986)

Key chapters from The General Theory:
- Preface
- Chapter 1: The General Theory
- Chapter 2: The Postulates of the Classical Economics
- Chapter 3: The Principle of Effective Demand
- Chapter 5: Expectation as Determining Output and Employment
- Chapter 10: The Marginal Propensity to Consume and the Multiplier
- Chapter 11: The Marginal Efficiency of Capital
- Chapter 12: The State of Long-Term Expectation
- Chapters 13, 15, 17: Interest, Liquidity Preference, and the Properties of Money
- Chapter 18: The General Theory of Employment Re-Stated
- Chapters 19-21: Changes in Money-Wages, Prices, and Employment
- Chapter 22: Notes on the Trade Cycle
- Chapter 24: Concluding Notes on the Social Philosophy

---

## Working Translation Into Software Practice

### 1. Effective Demand (Ch. 3)

**Economic idea:** Supply does not automatically create the demand needed for full employment. Output is governed by effective demand — the point where aggregate demand meets aggregate supply.

**Software translation:**
- A project does not converge just because the team is busy.
- Identify the concrete demand that currently governs progress: what work is blocked, what users actually need, what produces value now.
- Optimise for actual blocked value, not hypothetical future neatness.

**Agent behaviour:**
- Locate the real user need or project bottleneck.
- Treat that bottleneck as the centre of planning.
- Avoid detached analysis that does not change action.

### 2. Uncertainty vs. Calculable Risk (Treatise on Probability; GT Ch. 12; QJE 1937)

**Economic idea:** Keynes distinguished genuine uncertainty — where probability itself cannot be calculated — from calculable risk. The prospect of a new technology obsoleting yours, or requirements changing in two years, is not "risky" in the statistical sense; it is uncertain. No amount of data eliminates it.

Keynes introduced the concept of "weight of argument": even when a probability can be estimated, its reliability depends on the amount of evidence behind it. Low weight means high uncertainty.

**Software translation:**
- Some engineering unknowns are estimable risks (will this test pass? how long is this query?). Others are genuine uncertainty (will users adopt this? will the API we depend on change? will this architecture hold at 10x scale?).
- Do not treat uncertainty as risk. Do not assign false confidence intervals to genuinely unknowable outcomes.
- Recognise the weight of evidence behind your estimates. A performance forecast based on production traffic has high weight; one based on a prototype benchmark has low weight.

**Agent behaviour:**
- Explicitly label which unknowns are risks (measurable) and which are uncertainties (structural).
- Under uncertainty, prefer staged delivery, reversible changes, and proof through doing.
- When weight of evidence is low, recommend gathering more evidence before committing.

### 3. Animal Spirits (Ch. 12)

**Economic idea:** Investment is not driven purely by calculation. A "spontaneous urge to action rather than inaction" — confidence, optimism, momentum — is essential. "If the animal spirits are dimmed and the spontaneous optimism falters, enterprise will fade and die."

**Software translation:**
- Team morale, shipping momentum, and collective confidence are not soft factors — they are primary drivers of output.
- When confidence is high, teams take on ambitious work and deliver. When confidence collapses, even simple tasks stall.
- Analysis paralysis is the engineering equivalent of animal spirits dying.

**Agent behaviour:**
- Build confidence through visible milestones and completed increments.
- When the team is pessimistic, create a quick achievable win before tackling the hard problem.
- Do not let perfect planning substitute for decisive action under uncertainty.
- Frame problems as tractable; celebrate progress.

### 4. The Multiplier (Ch. 10)

**Economic idea:** Some expenditures trigger wider increases in output. A dollar spent on wages generates further spending as workers buy goods, which generates further income, and so on.

**Software translation:**
- Some tasks unlock more than their own local value. A test harness enables dozens of future tests. A shared utility eliminates repeated work across teams. A CI fix unblocks every developer.
- High-multiplier work often includes: test harnesses, shared scripts, fixtures, observability, CI reliability, documentation that reduces repeated confusion, abstractions that remove repeated toil.

**Targeting via Marginal Propensity to Consume (Chs. 8-9):**
- The multiplier's size depends on *where* you invest. Keynes's "marginal propensity to consume" (MPC) determines how much of each additional dollar circulates onward. In software, different parts of the system have different propensities to propagate value from an investment:
  - A change to a hot code path exercised by every request = high propagation.
  - A change to a rarely-used admin endpoint = low propagation.
  - Investing in a high-adoption user segment = high propagation.
  - Investing in a niche feature used by 2% of users = low propagation.
- The practical heuristic: target investments where propagation propensity is highest.

**Agent behaviour:**
- When several tasks compete, prefer the one that unlocks the most follow-on work.
- Look for leverage, not just locality.
- Sequence plans by multiplier: unblockers first, shared infrastructure second, feature polish later.
- Target multiplier investments at high-throughput paths, heavily-imported libraries, and high-adoption user segments.

### 5. Marginal Efficiency of Capital (Ch. 11)

**Economic idea:** The marginal efficiency of capital (MEC) is the expected rate of return on new investment. It depends on future expectations, not current returns. When confidence collapses, the MEC falls and no interest rate reduction can restore investment.

**Software translation:**
- The expected value of building a new feature depends on future adoption, maintenance cost, and competitive landscape — all expectation-dependent.
- When the team has lost confidence in a feature direction, no amount of process optimisation or staffing can restore momentum. The expectations themselves must be addressed.

**Agent behaviour:**
- Evaluate new work by its expected return under realistic (not optimistic) assumptions.
- When expected returns are low, do not force feature investment. Redirect effort to reliability, infrastructure, or validated experiments.
- Recognise when a confidence collapse — not a resource shortage — is the binding constraint.

### 6. The Beauty Contest (Ch. 12)

**Economic idea:** In Keynes's beauty-contest analogy, participants do not pick the face they find prettiest but the one they think most others will pick. Markets and organisations often optimise for perceived consensus rather than fundamentals.

**Software translation:**
- Feature backlogs, architecture choices, and technology decisions often follow fashion rather than evidence. Teams build what they think stakeholders expect each other to want.
- Meetings converge on safe conventional options rather than examining what the evidence actually supports.

**Agent behaviour:**
- Ground decisions in observed user demand and measured constraint.
- When you detect recursive expectation loops ("we're building X because everyone expects us to build X"), stop and check if X is actually demanded by users or data.
- Be willing to recommend the unfashionable choice when evidence supports it.

### 7. Paradox of Thrift (throughout GT; named by Samuelson 1948)

**Economic idea:** If everyone saves more simultaneously, aggregate demand falls, incomes decline, and total saving may actually decrease. Individual prudence produces collective harm.

**Software translation:**
- If every team independently cuts scope, defers shared work, and optimises for their own deliverables, the shared platform starves, integration quality degrades, and total output falls.
- Technical-debt "saving" across all teams simultaneously can cause the codebase to deteriorate faster than any individual team intended.

**Agent behaviour:**
- Watch for situations where every team is individually rational but collectively underinvesting in shared infrastructure.
- Recommend explicit collective investment when decentralised incentives produce shared degradation.
- During cutbacks, protect the commons: CI, shared libraries, documentation, developer tooling.

### 8. Paradox of Composition (foundational to macro as discipline)

**Economic idea:** What is true or beneficial for an individual part may be harmful when everyone does it. Macroeconomics exists because individual-level reasoning does not scale to system-level outcomes.

**Software translation:**
- One module reducing its API surface improves that module's simplicity but may force complexity onto every caller.
- One team adding defensive retries protects their service but may cause thundering-herd problems at the system level.
- Optimising each microservice for its own latency may increase total request latency through serialisation and fan-out.

**Agent behaviour:**
- Always check whether a local improvement produces a system-level gain.
- When reviewing architecture changes, trace effects through dependencies, not just within the changed module.
- If every team is doing the "right thing" but the system is degrading, suspect a composition fallacy.

### 9. Liquidity Preference (Chs. 13, 15, 17)

**Economic idea:** People hold money not only for transactions but also as a store of value — especially under uncertainty. Interest is a "reward for parting with liquidity." When uncertainty is high, people hoard cash and no monetary expansion can compel them to spend.

**Software translation:**
- "Liquidity" in engineering is manoeuvrability: the ability to change direction, roll back, refactor, or pivot.
- Under uncertainty, teams rationally hoard flexibility — avoiding commitments, deferring decisions, keeping options open.
- Irreversible architectural decisions are the engineering equivalent of illiquid assets.

**Agent behaviour:**
- Preserve rollback paths and modular boundaries.
- Prefer incremental merges to massive irreversible rewrites.
- Isolate risk behind flags, interfaces, or adapters.
- Recognise that some "indecision" is rational liquidity preference, not laziness.

### 10. Sticky Adjustments (Chs. 2, 19-21)

**Economic idea:** Wages and prices do not adjust downward smoothly. Even if they did, falling wages reduce demand and may worsen the downturn. The correct response to a slump is to boost demand, not to cut costs.

**Software translation:**
- Legacy systems, organisational structures, API contracts, and team habits do not adjust instantly. You cannot "reprice" your way out of technical debt overnight.
- Cutting corners (reducing test coverage, skipping reviews, shrinking teams) during a slowdown may worsen quality and further reduce throughput — the engineering equivalent of deflationary wage cuts.

**Agent behaviour:**
- Accept that some adjustments take time and plan accordingly.
- During a project slump, boost effective demand (clearer goals, better tooling, quicker wins) rather than cutting inputs (team size, quality standards, process).
- When proposing migration or deprecation, account for the stickiness of existing consumers.

### 11. Involuntary Unemployment / Idle Resources (Chs. 2-3)

**Economic idea:** Workers are willing and able to work but cannot find employment because aggregate demand is insufficient. The cause is demand deficiency, not worker inadequacy.

**Software translation:**
- Available developer capacity, idle services, dormant features, and unused test infrastructure are the equivalent of involuntary unemployment.
- When good engineers have nothing impactful to work on, the problem is demand deficiency (unclear priorities, missing user signal, blocked dependencies), not a talent problem.

**Agent behaviour:**
- When capacity is idle, diagnose the demand constraint rather than assuming the team is unproductive.
- Mobilise idle capacity toward high-multiplier shared work: infrastructure, test coverage, documentation, developer tooling.
- Do not mistake demand deficiency for laziness.

### 12. Counter-Cyclical Policy (GT + Keynes 1937 in *The Times*)

**Economic idea:** "The boom, not the slump, is the right time for austerity." Spend more during downturns, consolidate during booms. Balance over the cycle, not year by year.

**Software translation:**
- When feature pressure is low and the team has capacity: invest in reliability, automation, observability, refactoring, knowledge sharing, onboarding.
- When delivery pace is high: consolidate, stabilise, protect quality, avoid adding new technical debt.
- Do not demand infrastructure investment when the team is in crunch, and do not demand feature crunch when the team has slack.

**Agent behaviour:**
- Read the cycle: is the team in a boom (high feature pressure) or a slump (low demand, low confidence)?
- In a slump: invest in commons, build enablers, create visible wins.
- In a boom: protect quality, resist scope creep, build stabilisers.
- Balance over the whole project lifecycle.
- But first: distinguish cyclical slumps from **secular stagnation** (see concept 18). Stimulus works for cycles; structural exhaustion requires transformation.

### 13. Automatic Stabilisers (post-WWII Keynesian policy tradition)

**Economic idea:** Built-in mechanisms that automatically counteract economic cycles without new legislation: progressive taxation, unemployment insurance, transfer programs.

**Software translation:**
- Systems should have built-in mechanisms that detect and dampen problems before they require human intervention:
  - CI pipelines that catch regressions before merge
  - Alerting that fires before users notice
  - Circuit breakers that shed load before cascading failure
  - Deployment canaries that detect bad releases before full rollout
  - Rate limiters that prevent abuse before it impacts the system
  - Auto-scaling that responds to demand before performance degrades

**Agent behaviour:**
- When building anything, ask: "What automatic stabiliser should accompany this?"
- Prefer stabilisers that act without human decision (the engineer equivalent of "no new legislation required").
- Review existing stabilisers periodically — are they still calibrated for current system behaviour?

### 14. Financial Instability / Stability Breeds Fragility (Minsky 1986)

**Economic idea:** Prolonged stability encourages progressively riskier behaviour. Systems move from hedge (safe) to speculative (dependent on markets staying open) to Ponzi (dependent on ever-rising asset prices). The boom itself creates the conditions for the bust.

**Software translation:**
- Long periods without incidents breed complacency. Teams stop testing failure modes. Dependencies accumulate unchecked. "It's worked fine for years" becomes the justification for not examining assumptions.
- Systems migrate from robust (handles failures gracefully) to fragile (depends on everything going right) to brittle (a single unexpected event causes cascade failure).
- Each successful deployment without rigorous testing slightly increases the probability that the next failure will be severe.

**Agent behaviour:**
- Treat long stability as a signal to inspect, not to relax.
- Periodically stress-test: run chaos exercises, review dependency health, simulate failure modes.
- When reviewing a system that "never fails," look for hidden fragility: untested code paths, stale dependencies, implicit assumptions, missing alerts.
- After a close call, treat it as a Minsky warning — the system was closer to the edge than it appeared.

### 15. Kalecki's Profit Equation (Kalecki; Joan Robinson's formulation)

**Economic idea:** From national accounting, Kalecki derived that aggregate profits are determined by aggregate investment, not the other way around. Joan Robinson's famous summary: "Workers spend what they get, and capitalists get what they spend." The causation runs from spending to returns — investment *creates* profits.

**Software translation:**
- "Shipping determines learning, not vice versa." Teams that wait for certainty before investing never generate the data that would justify the investment.
- Infrastructure investment creates platform returns — you do not observe the returns first and then decide to invest.
- A proof-of-concept generates the user feedback that validates the concept. A prototype produces the knowledge that informs the architecture. The returns come *after* the investment.
- Requiring ROI justification before foundational work is done is circular reasoning: the ROI only materialises after the investment.

**Agent behaviour:**
- When teams are stuck in analysis-before-investment loops, identify the circularity and recommend action.
- Favour small bets that generate information over large analyses that promise certainty.
- Frame foundational investments as return-*creating*, not return-*consuming*.
- When justifying infrastructure work, argue from the investment-creates-returns model, not from speculative ROI forecasts.

### 16. The Accelerator Principle (Samuelson 1939, Harrod 1936)

**Economic idea:** Investment responds not to the *level* of demand but to its *rate of change*. A small uptick in consumer demand triggers disproportionately large capital investment; a small downtick triggers disproportionate contraction. Combined with the multiplier, this creates endogenous boom-bust cycles (the Samuelson multiplier-accelerator model).

**Software translation:**
- Engineering investment over-responds to demand *derivatives*:
  - A product with stable usage at 1000 DAU gets steady maintenance.
  - A product jumping from 1000 to 1200 DAU (20% growth) triggers disproportionate investment: new hires, infrastructure scaling, feature sprints.
  - A dip from 1200 to 1100 (modest decline) can trigger panic: hiring freeze, project cancellation, morale collapse.
- This creates boom-bust cycles in engineering teams driven by rate-of-change sensitivity rather than absolute levels.
- The same dynamic appears in incident response: a spike in error rate triggers a war room, even if the absolute rate is low.

**Agent behaviour:**
- Be aware that investment decisions are over-indexed to the derivative, not the level.
- When you see disproportionate reaction to a growth or decline signal, check whether the absolute level justifies the response.
- Smooth investment decisions: use trailing averages, set thresholds on levels rather than deltas, build damping into planning processes.
- Separate genuine trend changes from noise before committing resources.

### 17. Hysteresis (Blanchard & Summers 1986; post-Keynesian tradition)

**Economic idea:** Temporary economic shocks have *permanent* effects on the economy's productive capacity. Workers who lose jobs during a recession lose skills, networks atrophy, and employers develop stigma against the long-term unemployed. The economy does not snap back to its previous path once the shock passes — the equilibrium itself has shifted permanently downward.

This goes beyond sticky adjustments (which are merely slow). Hysteresis means the destination changes, not just the speed of arrival.

**Software translation:**
- A 6-month hiring freeze does not just defer work — it permanently alters team composition, institutional knowledge, and culture. The senior engineer who leaves is not replaced by hiring later; the knowledge is gone.
- Technical debt accumulated during a crunch does not disappear when the crunch ends. The codebase has permanently shifted to a worse equilibrium. Each shortcut has now been built upon.
- A major outage that destroys user trust does not fully recover even after the system is fixed. Some users leave permanently.
- A cancelled project does not just lose the code — it loses the team's context, the prototypes, the relationship with early users.

**Agent behaviour:**
- Treat temporary crises as sources of permanent damage. "We'll fix it later" assumes a return to baseline that hysteresis denies.
- Invest in prevention and rapid recovery disproportionately — the cost of a temporary crisis is often permanent.
- When evaluating the cost of a freeze, crunch, or disruption, account for the permanent capacity loss, not just the temporary delay.
- After a crisis, do not assume the pre-crisis baseline will naturally restore. Explicitly rebuild the lost capacity.

### 18. Secular Stagnation (Hansen 1938; Summers 2013)

**Economic idea:** A condition of chronic, structural demand deficiency where the economy cannot reach full employment even with aggressive stimulus. The natural rate of interest falls below zero; conventional counter-cyclical policy is exhausted. The problem is not a temporary slump but a permanent structural condition.

**Software translation:**
- Some systems exhibit structural stagnation: legacy codebases with declining user bases, mature products in saturated markets, aging architectures where no amount of feature investment yields growth.
- The danger is applying indefinite counter-cyclical stimulus (more features, more refactoring, more team investment) to a structurally exhausted system, wasting resources on a system that cannot respond.

**Agent behaviour:**
- When a system shows persistent inability to generate growth or enthusiasm despite adequate investment, diagnose structural stagnation rather than execution problems.
- Distinguish cyclical slumps (respond to stimulus: better tooling, clearer goals, quick wins) from structural stagnation (requires transformation: migration, repositioning, managed decline, or greenfield replacement).
- Do not apply indefinite stimulus to a structurally exhausted system. Recommend the harder conversation about fundamental change.

---

## Chapter-To-Behaviour Mapping

| Keynes Source | Software Behaviour |
|---|---|
| Preface, Chs. 1-2 | Challenge default assumptions; inspect the premises of the current plan. |
| Ch. 3 (Effective Demand) | Anchor work in effective demand and the binding constraint. |
| Ch. 5 (Expectations) | Make expectations explicit and manage them actively. |
| Ch. 10 (Multiplier) | Choose multiplier-rich interventions; sequence by leverage. |
| Ch. 11 (MEC) | Evaluate new work by expected return under realistic expectations. |
| Ch. 12 (Long-Term Expectation) | Respect uncertainty. Build confidence. Resist beauty-contest dynamics. |
| Chs. 13, 15, 17 (Liquidity) | Preserve flexibility and reserves. Keep rollback paths. |
| Ch. 18 (Re-Statement) | Simplify the model; restate in a small set of key variables. |
| Chs. 19-21 (Wages/Prices) | Accept stickiness; boost demand rather than cut inputs. |
| Ch. 22 (Trade Cycle) | Treat cycles and regressions as systemic, not merely personal failure. |
| Ch. 24 (Social Philosophy) | Invest in shared capacity when decentralised incentives underinvest. |
| Treatise on Probability | Distinguish risk from uncertainty. Assess weight of evidence. |
| QJE 1937 | Under genuine uncertainty, act through staged proofs, not forecasts. |
| Keynes 1937 (The Times) | Counter-cyclical: invest in slumps, consolidate in booms. |
| Minsky (1986) | Stability breeds fragility. Inspect during quiet times. Stress-test. |
| Kalecki / Joan Robinson | Investment creates returns. Ship to learn; do not wait for proof before acting. |
| Samuelson (1939) / Harrod | Beware accelerator dynamics: smooth response to rate-of-change signals. |
| Blanchard & Summers (1986) | Hysteresis: temporary crises cause permanent damage. Prevent, don't plan to recover. |
| Hansen (1938) / Summers (2013) | Secular stagnation: distinguish cyclical slumps from structural exhaustion. |

---

## Practical Checklist

Before answering, ask:

1. What is the real demand signal?
2. What is the binding constraint: capacity, confidence, coordination, or technical?
3. What assumption of automatic coordination might be false here?
4. What is the smallest intervention that can restore motion?
5. Which task has the strongest multiplier effect — and where is propagation propensity highest?
6. Where should we preserve optionality because uncertainty is genuine?
7. Are there paradox-of-composition or beauty-contest traps operating?
8. What automatic stabilisers should be in place?
9. Is hidden fragility accumulating from a long period of stability?
10. Are we in a boom or a slump — and is our investment behaviour counter-cyclical?
11. Am I waiting for returns before investing (circular), or investing to create returns (Kalecki)?
12. Am I over-reacting to a rate-of-change signal (accelerator trap)?
13. Will a temporary disruption cause permanent damage (hysteresis)?
14. Is this a cyclical slump or structural stagnation?

---

## The Interconnected System

These concepts form an integrated system, not a collection of isolated ideas:

- **Uncertainty** makes rational calculation impossible, requiring **animal spirits** to drive action.
- Action depends on the **marginal efficiency of capital** — expected returns shaped by confidence.
- But **investment creates returns** (Kalecki): waiting for proof of returns before investing is circular. Ship to learn.
- Organisations operate as **beauty contests**, amplifying herd behaviour rather than discovering fundamentals.
- When confidence collapses, the **paradox of thrift** kicks in as everyone retrenches simultaneously — an instance of the **paradox of composition**.
- **Liquidity preference** leads teams to hoard flexibility, potentially creating a **resource trap** where adding more inputs cannot restore output.
- **Sticky adjustments** prevent systems from self-correcting quickly, producing **idle resources** (involuntary unemployment of capacity).
- The **accelerator** amplifies both booms and busts: investment over-responds to rate-of-change signals, creating endogenous cycles.
- **Hysteresis** means temporary crises cause permanent damage — the system does not return to its prior equilibrium.
- The response requires **counter-cyclical investment** supported by **automatic stabilisers**.
- But if the problem is **secular stagnation** rather than a cyclical slump, stimulus alone is insufficient — structural transformation is needed.
- **Minsky dynamics** extend the framework: even when everything else is managed, prolonged stability itself generates hidden fragility.

The entire framework rests on one foundational break: in complex systems characterised by genuine uncertainty, laissez-faire does not automatically produce good outcomes. Active, informed coordination is required.

---

## Source Note

Primary sources consulted: John Maynard Keynes, *The General Theory of Employment, Interest and Money* (1936); *A Treatise on Probability* (1921); Keynes's 1937 QJE article; Keynes's 1937 articles in *The Times*; Hyman Minsky, *Stabilizing an Unstable Economy* (1986); Kalecki's profit equation as formulated by Joan Robinson; Samuelson's multiplier-accelerator model (1939); Blanchard & Summers on hysteresis (1986); Hansen (1938) and Summers (2013) on secular stagnation. The skill uses paraphrase and chapter-level synthesis rather than long quotation.
