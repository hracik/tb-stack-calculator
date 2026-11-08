# Training (the Preparation button)

How many units to train when the Food production pays for several hits. Shown on every stack when the Preparation button is on. The code: unitsTxt, rangeOf, fracSpread, tipsFor, brkTip, stdTs, cycTxt (app.js).

## Terms
- Hit - one attack; the army loses units and the Revive (90 %) brings back part of them.
- Loss (L) - the units of a stack that are NOT revived in one hit (a stack that is not revived loses the whole stack n). Rounded down per stack.
- MUL - the hits the Food production pays for with the chosen Revive: the first hit trains the whole army (food F), every next hit only the losses (food R): MUL = 1 + (food - F) / R, rounded down to 2 decimals.
- Revive choice - none / top line / monsters / monsters + top line / all. Only the revived stacks have a small loss (e.g. with "top line" the 9s are revived, the 8s are trained again whole).
- Barracks - Barracks Leadership (Food settings): the most Leadership trained in one training; the Dominance trained in one training is always 1/4 of it (no input of its own). A full training = capacity / the cost of one unit.

## 1st training (starts from zero)
- A stack needs n + (hits - 1) x L units for the whole hits. The upper end adds the food of the fractional hit.
- The range shows "units for the whole hits - units for all the hits" (one number when they are the same). A mercenary shows the lower number with a "+" (no food, no upper end).
- The food of the fractional hit is shared EQUALLY: every stack gets the same amount of food (units = that food / the food of one unit), no cap, so a revived stack may end above its one-hit loss.
- Round number (under the range): one round base per army tier, the units of a troop = base / its Leadership cost; one round number per monster tier; the food left over raises the numbers step by step. Mercenaries have no tip.
- Barracks tip (under the round number): the units as full trainings - a whole number of full trainings inside the range when there is one (the fewest trainings, e.g. "3 × 96,000"), else the full trainings under the range plus a last training, the roundest number that lands inside the range (e.g. "2 × 533 + 400"). Without a range (up to 1 hit) it is shown for the number of units itself.

## The next trainings (↻ and ↺ lines)
After the 1st training and its max hits (+ revive) a revived stack has n - L units left. A hit needs n units, so every hit only needs the loss back: whole hits x L units. The hits per training stay the SAME in every training (the food of the revived units still counts; the hits never alternate or grow). The numbers change once (training 1 -> 2) and then stay the same for any number of trainings.
Example, 2 hits, Purifier I: 85,633 in the 1st training, then 15,570 in the 2nd, 3rd ... 21st.

Under the 1st training every stack shows two more lines (not for mercenaries):
1. ↻ the retraining - the number every next training trains, e.g. "16,000" or "3 × 96,000".
2. ↺ the cycle - "↺ 17 × → 8,260": train the retraining number 17 times, then ONE adjusting training of 8,260 units, then the same again.

### Why the cycle
The retraining number T is a bit above the need (lo), so a surplus d = T - lo piles up in stock every training. The adjusting training uses the surplus up (it trains lo - N x d), the surplus is then 0 and the same N trainings follow again.

### Rules
- T stays close above the need: at most 3 % surplus per training (15,570 -> 16,000, not 20,000), so the same training repeats as many times as possible (36 x 16,000 -> 90, instead of 3 x 20,000 -> 2,280). Whole barracks trainings (3 × 96,000) are used only when they are within the 3 %. Without the barracks capacity T is the roundest number just above the need.
- ALL the stacks make the same number of trainings N before the adjusting one: N = the most that every stack can do = the smallest floor(need / surplus) of all the stacks. The adjusting training of a stack = need - N x surplus.
- The army stacks of the same tier, cost, food and health retrain the SAME number of units** (Corax and Royal Lion, Purifier and Punisher): the window is from the bigger need up to 3 % above it, the roundest number in it. The smaller stack has a bigger surplus, so N drops a bit (36 -> 17 in the test army). 
- The monsters of one tier: the SAME addition after the full trainings (it does NOT need to be round, e.g. 366 or 404), each stack with its own full trainings (Dominance / its cost): e.g. "2 × 558 + 366", "2 × 533 + 366" ... The addition is the one with the smallest surplus for the tier (the biggest surplus of any stack, in % of its need), not above the food of any stack. N is back to 17 in the test army. The barracks tip of the 1st training uses the same addition too ("2 × 558 + 366" in both lines) when it fits the range; a whole number of full trainings inside the range (e.g. "3 × 461") is still preferred.
- The lines are shown for EVERY stack, also for the ones that are not revived (the 8s with the revive on the top line): they are trained again whole, so their ↻ number is hits x the stack.
- When the adjusting training is more than the barracks train at once, it is shown as full trainings + the last one, e.g. "↺ 17 × → 1 × 96,000 + 55,344" (not 151,344).

## Training plan (many hits, few clicks)
Under the stacks in Preparation. The clicks of the game: changing the captains 14, selecting a unit 3, one training at the barracks maximum 4 (the number field always shows the maximum: 96,000 Leadership, e.g. 4,800 Corax; a monster: 24,000 Dominance / its cost); a typed number costs extra clicks (deleting the maximum digit by digit, typing the new one).
- A MONOTONOUS plan: after every N hits the troops are checked, always the same way. Every troop has ONE fixed rule:
  - a threshold: "fewer than X units: x(m+1) full barracks, else xm" (usually "x1 full barracks below 145,000"); X is rounded up to a memorable number; nothing is typed;
  - or the same typed number at every check (its loss of N hits as full barracks + one typed number; the troops of one tier with about the same loss type ONE common number, rounded up to a memorable one when it costs at most 1 %).
- The captains are changed (14 clicks) only when a check finds something to train. Shown: the check interval N, the clicks per hit, how often a training is really needed (e.g. "about every 1.3 hits": at some checks nothing is below its number), the clicks per hit of the other N, the food of all the units alive against the Food production, and every troop's rule.
- Food = the consumption of ALL the units alive (the army and the stock), within the Food production. A threshold troop keeps a stock (up to a full barracks more) that eats food, so the thresholds go to the troops that save the most clicks per food while the food allows; the others type.
- N: 1 to the hits the chosen Revive mode pays for, the one with the fewest clicks per hit, checked over 240 hits (every hit has its full stacks, the food stays within the Food production).
- **Suggested Barracks Leadership: the plan is also worked out for lower capacities (90, 80, 75, 70, 60, 50, 40, 33 and 25 % of the typed one, rounded to thousands). The suggestion has the fewest clicks per hit; within 5 % of it a regular rhythm wins (a training at every check), then the longer check interval. When the typed one is the best, it says so. A lower capacity helps only if the game shows that number in the field (typing it is not counted).**
- A stack is never trimmed to suit the plan. Mercenaries are not in the plan; monsters are.
- The revive counts: a troop the chosen Revive mode brings back loses only the part not revived per hit (top line: a 9 loses 10 %, an 8 the whole stack).

## Open
- Whether the adjusting training should fit into the same number of barracks trainings as a regular one (it would lower N further).
- The 3 % is a constant in the code (STDSUR).
