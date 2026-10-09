# Methods and interpretation

## Research question
Does planning **sets of member clarifications** yield better sequential matching utility than buying single questions greedily, once shared endpoints and future opportunities are considered?

## Synthetic experimental protocol
- 60 simulated decision days, bounded arrival/departure, temporally unavailable members, previously-used pair exclusion.
- Synthetic outcomes are independent Bernoulli events with observable scoring features. This does **not** model actual date windows or delayed MSMI followups.
- Real hard preferences remain hidden from the clarification optimizer. Portfolio planning instead resamples hard fields from a separate synthetic prior population.
- Each selected hard question reveals a complete synthetic mandatory bundle; the question budget is four bundles per day (12 units).
- Every algorithm sees identical seeded member populations; outcome random streams can still diverge after policies introduce different pairs, so cross-policy estimates are paired by seed but not guaranteed common random outcomes at the edge level.

## Policies
No-ask, FIFO, top valued edge endpoints, singleton marginal surrogate, joint portfolio screening and sampling, and a seven-day-inspired persistence bonus. These are intentionally modest implementations of the research ideas; they are not the entire proposed competition policy.

## Primary observable
`proxy-MSMI` = 100 times qualifying Bernoulli-positive introductions divided by synthetic member count. The term *proxy* is important: it is not the official MSMI event sequence.

## Interpretation rules
If a more complex method scores below a simple baseline, report it. This sandbox is designed to find failure cases, not manufacture positive evidence. Do not transfer conclusions to the official benchmark without running its actual evaluator.

## Next steps toward the official framework
1. Implement the exact `docs/DATA_CONTRACT.md` eligibility checks as unit-tested functions.
2. Implement the official `ask` and `match` JSON policy interface and policy memory.
3. Load the released dataset partitions and evaluate using the organisers' `evaluate.py` on paired seeds.
4. Compare the myopic clarification baseline and top-endpoint baseline before adding persistent-value calculations.
5. Model mature delayed acceptance/date/intention stages without hindsight leakage.
6. Deploy a tested general-graph max-weight matching solver and profile true container startup + invocation limits.
