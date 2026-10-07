# Total Battle Stack Calculator

A single-file calculator for Total Battle. It works out how many troops of each type to send (Leadership = army pool, Dominance = monster pool) and in which order they should die, for the 3-, 4-, 6- and 8-stack modes and the special modes (Killshot v. 3 and Renegades).

Open `index.html` in a browser or use the GitHub Pages site of this repository. Nothing is installed or uploaded; everything is calculated in the page.

## Attack modes

The modes are in three rows, each with its own icon: Regular (4-stack, 8-stack), Sniper (3-stack, 6-stack, Killshot v. 3) and **PvP** (two emoji shooting each other): **CP kill**, **CP death**, Max damage and Renegades. In the PvP row **CP kill** and **CP death** work (see CP kill and CP death below), **Max damage** is still only a placeholder (its rules are not defined yet, the button is greyed out) and Renegades is switched off (see Renegades below).

Below the mode buttons there is a **bubble with a short explanation of the mode that is on** (full width; it changes when another mode is chosen): the enemy (number of stacks, mounted or not, epic or flying), how the order is made and what is special about the mode. The texts are in the constant `MODEINFO` in the page. The **Tiers to use** card has a bubble of the same design with two tips, always both shown (no switching with the mode). **Tip against epics** (3-, 4-, 6-, 8-stack and Killshot): for the maximum damage per hit choose the top 2 tiers of each troop type you have available (for example G8 + G9, S8 + S9, E8 + E9) and the top 3 Monster tiers (for example M7 + M8 + M9); leaving out the 2nd tier of Engineers may be the most cost-effective option, with similar damage per hit. **Tip against players** (CP kill and CP death): for maximum damage the top 2 tiers of Guardsmen and Engineers, the top 3 tiers of Specialists and the top 4 tiers of Monsters; leaving out the lowest tiers of Monsters and Specialists may be more cost-effective. Only the two labels are bold, the text is not.

## Troop data

The troop lists are written inside the page. For every troop (army, monsters, engineers, mercenaries) they store the health, the strength, the food consumption (all mercenaries use no food - the JSON lists a food value for most of them, but it is wrong, so it is not stored), the Leadership / Dominance / Authority cost and the vs melee / ranged / mounted / flying bonuses exactly as in the troop JSON. The strength is stored, not calculated from the health. The summary line above the result shows the **food consumption** of all the units together (number of units x food per unit), before the estimated damage.

Every unit eats **25 % less** than the stored food value (the constant `FOODCUT` in the page): the food consumption in the second summary line and everything that is counted from it (the hits the Food production pays for) use the reduced value. The stored values stay the plain JSON ones, so the cut can be changed in one place.

Every troop also stores its **revival cost in gold** (the attack figure of the troop JSON; the silver cost of defending is always 10 times it and is not stored). It is only stored - nothing shows or uses it yet.

## Army capacity, Food capacity & settings

Two cards at the top. **Army capacity** holds Leadership, Dominance and Authority. **Food capacity & settings** holds **Food production** (default 0) and the **Revive** select (90% of a revived stack comes back; None / Top line / Monsters only / Monsters and top line / All, default Top line). All the boxes are saved per tab like the other boxes. **Every input of the page looks the same**: one row with the label on the left (the same width everywhere, 78 px) and the box taking the whole rest of the row, the same height (32 px) for the number boxes and the selects. The labels are written out: `Health`, `Strength` and `Double hit` in the bonus cards, and `Food prod.` for the Food production box (the long name did not fit). **Thousands separators**: every number box (Leadership, Dominance, Authority, Food prod. and the bonuses) formats what you type, `1875508` becomes `1,875,508` (decimals such as `6,304.5` are kept); only digits and one decimal point are accepted, the cursor stays next to the same digit while you type, and the formatting is also applied when a tab is opened (tabs saved earlier included). The calculation reads the box without the commas. On a phone every card is one column, so every box is as wide as its card; on a wide screen the Army capacity and Food capacity cards put their boxes side by side and the bonus cards stand four in a row (equal widths). Food production and Revive only decide how many hits (and how many units to prepare) are shown (see Result views - Hits the food production pays for)

## Mercenaries

Mercenaries are hired troops. They use Authority only (not Leadership or Dominance), and all of them last 7 days. The Authority box is next to Leadership and Dominance. The 15 mercenaries we have a picture for are in the calculation (list `MERC`, with class, tier, category, type, health, strength, Authority per unit, the vs melee / ranged / mounted / flying bonuses and the bonus against epic enemies). The other 31 mercenaries from the troop JSON are stored apart in the list `MERC_LATER`, with the same columns; nothing reads that list, so they change no number and show nowhere, until a picture is added and the row is moved up into `MERC`. The swarm bonus of a jungle guardian is stored in the same vs column as a regular bonus, and a flag marks the jungle guardians.

### Mercenaries in the attack

- **They come last.** The Leadership and Dominance stacks are solved first and never change (the same numbers for any Authority, in every mode). The mercenary stacks are added behind the last of them in the dying order, so they strike and die after all Leadership / Dominance stacks. The strikes continue the place numbering (place p strikes ceil(p / K) times, as everywhere).
- **Authority is a cap, and every mercenary that is on gets a stack.** The mercenary stacks form a chain like the other stacks: the first one steps down in health (and in total strength) from the last Leadership / Dominance stack, every next one steps down from the one before it. When the Authority is enough for that, the stacks follow the chain and the Authority that is left over stays unused, nothing has to fill it. When the Authority is short (for example 10 % of the Leadership), all the mercenary stacks that are on are still brought: they stand about level - one common health level, the highest the Authority pays for, with only the tiny step down along the order - so a cheap unit and an expensive one end with about the same stack health. A stack that cannot get one unit does not exist (the places after it move up; the places Kn+1 stay exempt from the strength rule, as for the other stacks). With no Leadership / Dominance stack at all, the common level is simply the highest one the Authority reaches.
- **What is shown.** With Authority 0 the Mercenaries section is not shown at all. With Authority above 0 it shows only the mercenaries that get units (a mercenary that you turned off stays on the list, so that you can turn it on again). If none gets a unit, the section says so.
- **Every mercenary in the list takes part.** Click a mercenary card to turn it off (or on again); it is saved in the tab like the army cards. There is no owned-number box. The number on a card is the count the calculation gives; `#` is the place in the dying order.
- **Bonuses.** A Guardsman mercenary gets the Guardsmen health / strength bonuses plus the bonus of its category, a Specialist the Specialists' (Renegades: x2 strength), the Engineer the Engineers', a monster mercenary the Monster bonuses plus its category and, when its type is Giant / Elemental / Dragon / Beast, the type bonus and the Double hit of that group (Demon, Undead, Elves and Cursed have no type box). A Beast-type Guardsman or Specialist mercenary (Jago, Warregal, Shedu) gets the Beast bonuses like the Beast army units. Its own vs bonus counts like every troop's bonus (the biggest one against the enemy stacks that are present). The Epic Monster Hunters (Superior: +1000 %, VII: +934 %, VI: +709 %) also have a bonus against epic enemies. The enemy stacks are epic in every mode except Renegades, so the bonus counts in all modes but Renegades; it counts against every enemy stack, so it adds to the class bonus (the order row shows e.g. `+1,000% vs. epic`). The other kinds of bonus in the JSON (vs fortifications, vs beasts and so on) are not used.
- **Order.** Simply by the squad bonus - the smaller one dies first, so the strongest bonuses die last and strike the most (the squad bonus is the same measure as everywhere: the unit's own bonus against the enemy stacks that are present, plus the Double hit). A bonus against epic enemies counts against every enemy stack, a class bonus only against the stacks of that class, so at the same size the epic bonus is the better one (the Superior Epic Monster Hunter, +1000 %, dies after Slavic Warrior and the other +1000 % class bonuses). The same bonus: nominal bonus, category, higher tier first. The strength / health ratio groups and the group search that the Leadership / Dominance stacks use are not used for the mercenaries.
- **Short Authority.** No mercenary is left out because of it - the stacks just become smaller together. Turn cards off yourself to leave a mercenary out; the Authority then goes to the others.

## Result views

The Result section only shows what there is a capacity for: with **Leadership, Dominance and Authority all 0** the whole Result section is hidden (a new tab starts that way); the **Army** section is not shown while Leadership is 0, the **Monsters** section while Dominance is 0 and the **Mercenaries** section while Authority is 0.

Above the result there is a View switch: **Grouped**, **Mobile** and **Computer**. The View and Action rows (and the Monsters Boost research buttons) each have their label on a line of its own with the buttons below it, all the buttons the same size (three equal columns).

- **Grouped** (the default) is the cards in groups, 5 per row, with the label of a group (for example Guardsmen 9) in one row above its cards, one block for the Mercenaries, one for the Monsters and one for the Army (in this order, in every view).
- **Mobile**: one unit per line. The line starts with the picture; to the right of it is the name of the unit and below the name the number of units. The three sections (Mercenaries - Authority, Monsters - Dominance, Army - Leadership) keep their headings. A line can be clicked to turn the troop off or on, like a card, and it shows the `#` number (the place in the kill order) at the right edge, as the Grouped cards do. Inside every section the units stand by the **original health of one unit, the biggest first** (Mercenaries: Wyvern, Warden, Eternal Cannoneer, Demonic Salamander, Warregal, Jago, Ariel, Superior Epic Monster Hunter, Quicksand, Galloper, Highlander, Slavic Warrior, Pounder, Scarface, Grace; Monsters: Kraken, Fire Phoenix, Devastator, Trickster of tier 9, then 8, then Wind Lord, Black Dragon, Destructive Colossus, Ancient Terror, then the lower tiers the same way; Army: Corax II, Royal Lion II, Corax I, Royal Lion I, Josephine II, Josephine I, ...). Units with the same health: the mercenary list order, then the higher tier, Guardsmen before Specialists, then ranged before melee (the full order: flying, mounted, ranged, melee), then the order of the Grouped cards. The Grouped view keeps its own order. In the Mobile and Computer lines the `#` badge sits at the right edge and the name keeps a gap for it, so the badge never covers the name or the numbers (on narrow phones the Computer lines get a smaller icon and the badge moves to the top-right corner).
- **Computer**: the same lines as Mobile in two columns - the units 1 and 2 next to each other, 3 and 4 in the next row, and so on. The order is the Mobile order with a few units moved by hand: Mercenaries ... Highlander, Scarface, Pounder, Slavic Warrior, Grace; Monsters as in Mobile; Army: Royal Lion II, Corax II, Corax I, Royal Lion I, Josephine II, Josephine I, Smiter II, Whitemane II, Smiter I, Whitemane I, Purifier II, Punisher II, Legitimist II, Duelist II, and last Legitimist I, Punisher I, Duelist I, Purifier I. Clicking a line turns the troop off or on.

The chosen view is one setting for the whole page (saved in the browser, not per tab).

### Hits the food production pays for

The **Food production** box (Food capacity & settings, saved per tab, default 0) sets how much food you have. The preparing calculations use the box **plus 0.9 %** (`production x 1.009`, the constant `FOODADD` in the page); the box itself shows what you typed. The food consumption of the calculated army (all the units of one hit, after the 25 % cut, the number shown in the summary line) is the food one hit costs when every unit has to be prepared. The hits are rounded **down to 2 decimals** and shown with 2 decimals.

**Without revival** (all the units are gone after the hit): `hits = food production / food consumption` (20,000,000 / 15,990,240 = 1.2507... shows as 1.25).

**With revival.** After a hit 90 % of a revived stack comes back, **rounded down per stack** (a stack of 334 units: 300 come back, 34 are lost; a stack of 5: 4 come back). Revival costs gold, not food (the gold cost per unit is stored, see Troop data), so only the lost units have to be prepared again. The first hit needs the whole army, every next hit only the lost units:

`hits = 1 + (food production - food of the whole army) / (food of the units that are not revived)`

(when the production is smaller than one army, it is `production / food of the army` as above).

**Revive** (the select in Food capacity & settings, saved per tab, default **top line**) chooses which stacks come back, from the least revival to the most:

- **none**: nothing comes back, `units x hits`.
- **top line**: only the top line stacks. The *top line* is the highest tier in use, taken separately for the Army (with the engineers), the Monsters and the Mercenaries - with the army and monsters on tiers 8 and 9 it is the 9s, with units 7 + 8 only it is the 8s (the tooltip of the select names the tiers); all the lower tiers are lost every hit.
- **monsters only**: only the monster stacks - the Monsters and the mercenary monsters (Wyvern, Warden, Eternal Cannoneer, Demonic Salamander) - all their tiers; the Army, the engineers and the other mercenaries are lost every hit.
- **monsters and top line**: the monster stacks (all tiers) and the top line of the Army and of the Mercenaries.
- **all**: every stack comes back (90 %).

The second line under the summary starts with the food consumption of the calculated army and, when at least one revive mode pays for more than 1 hit (1.01 or more), goes on with the hits for all five: `Food consumption 11,990,595 · hits per revive mode: 10.66 none · 14.25 top line · 16.38 monsters · 22.98 monsters + top line · 97.26 all` (the chosen one in bold). Without such hits only the food consumption is shown. The estimated damage in the first line is always the damage of one hit.

**Action: Hitting / Preparing** (Result, under View, saved per tab, default **Hitting**) choose which number the cards and lines show. While the **Food production is 0** there is nothing to prepare for: the Preparing button is disabled (greyed out), Hitting is shown, and the line `To see the preparing numbers, fill in the Food production (Food capacity & settings).` appears under the buttons. The Preparing choice itself stays saved and is active again as soon as the production is filled in:

- **Hitting**: the units of one hit - the number to hit with (the 1x number, as always).
- **Preparing**: only the units to **prepare** for the hits the chosen Revive pays for, as a range, `380 – 400`: **from** the units for the whole hits the Food production pays for **to** the units for all the hits. With 2.09 hits that is the units for 2.00 hits (for example 360 + 1 x lost units = 380) up to the units for 2.09 hits (360 + 1.09 x lost units = 400), so the lower number is what you need for at least 2 hits. Every number is **rounded up to a whole piece**: the whole stack for the first hit plus the lost units for every next hit, `units + (hits - 1) x lost units`. Without revival the lost units are the whole stack, so it is `units x hits`. With 1.25 hits the lower number is the stack itself (the units for 1.00 hit), for example `400 – 418`. A single number is shown only when the two ends are the same (a whole number of hits, such as 8.00, or nothing is lost when a stack is revived) and when the food pays for 1 hit or less (then it is the stack itself). On a narrow card the range breaks into two lines in front of the dash. A **mercenary** eats no food, so it gets no upper end: where the other troops show a range, a mercenary shows only the lower number and a plus (`240+`, not `240 – 246`); a mercenary with a single number shows it as it is. A troop that is turned off shows `off`.

The Leadership / Dominance / Authority used, the number of stacks and strikes and the `#` kill order are not affected. The 90 % is the constant `REV` in the page.

## Tabs

The page starts with four tabs: `1 cap`, `3 cap`, `Hero` and `Hero+3 cap`. They are ordinary tabs: rename (double-click), duplicate or delete them, or add your own with `+`. Each tab keeps its own settings, saved in your browser only. A **new tab** (the four start tabs and every `+`) starts blank: Leadership, Dominance, all the basic bonuses, all the monster bonuses (health, strength and Double hit) and the Food production are 0 (the constant `BLANK` in the page); the special bonuses, Authority, the tiers and the Revive choice start as before. Tabs you already have keep their numbers.


## CP kill and CP death (PvP)

The two buttons are in the PvP row (CP kill was called CP run before). In both modes the enemy is **one flying stack**, and the PvP rules differ from the Regular and Sniper modes (which fight an epic monster):

- **No epic bonuses.** The Epic strength box is not used, and the bonus against epic enemies (for example the Superior Epic Monster Hunter) is not counted. Every other bonus you entered is applied as usual.
- **Specialists deal double damage.** The unit strength is the base strength with all your strength bonuses (no epic strength); it is what the SH ratio (strength per health) is built from. A Specialist hits with two single strengths, and the squad bonus is added to **one** of them (the single strength), it is never doubled: `damage of a unit = (strength + squad bonus) + strength = 2 x strength + squad bonus`, in numbers `base x (2 x your strength multiplier + squad bonus)`. For everybody else it is `base x (multiplier + squad bonus)`. For example a Specialist with a strength multiplier of 64 and +859 % against flying deals `base x (2 x 64 + 8.59) = base x 136.59` (not `base x 145.18`, which would double the bonus too). 
- **Only the bonus against flying counts** (the squad bonus of a troop against melee, ranged or mounted enemies is ignored).
- **Fixed order, nothing is ranked by strength.** The dying order is: all the **Engineers** first (higher tier first), then the army tier by tier from the top, Guardsmen before Specialists (**G9, S9, G8, S8 ...**), and the **monsters last**, tier by tier from the top. Inside a class and tier the troops with the smaller squad bonus (against flying) come first. Mercenaries (Authority) are still added behind the last stack, as in the other modes.
- **The Double hit is unused.** The only enemy is one stack, there is no second enemy to hit, so in CP kill and CP death the Double hit (of the monsters and of the Beast units Royal Lion and Battle Griffin) adds no damage and is not a squad bonus: the damage is calculated without it, it is not shown in the dying-order list, and for the order and the groups only the bonus against flying counts. The Double hit boxes keep their values and still work in the other modes.
- **Groups of equals.** In CP kill troops with the same class, tier, squad bonus and SH ratio (for example every G9 without a squad bonus against flying) are **one group**: the game picks their order at random, so their stacks get **about the same total health** (as equal as whole units allow) and the group shares its places in the order. Inside a class and tier the groups follow the smaller bonus first, then the smaller SH ratio first (the Royal Lion stands before the Duelist group of its tier). For the estimated damage every stack of the group strikes the average of the group's places. In the dying-order list (and on the cards) the group is printed **with the biggest stack first, in declining health, and every stack has its own place number** (the order inside a group is the game's choice, so the list only shows one possible order); a range such as `3–4` is shown only for stacks whose health is exactly equal (for example Punisher and Smiter of one tier).
- **Tight by health only.** Between the groups there is the same small step down along the order as in the other modes; the total strength is **not** kept falling along the order, because the strength order does not matter here. As everywhere, the monsters stay below the army's health level, so a Dominance that is far bigger than that level allows partly stays unused. The mercenaries start below the smallest stack of the last group.
- The number of full monster tiers is chosen by the damage, like in Killshot. The estimated damage counts one enemy stack: the stack in place p of the order strikes p times (one strike for the first, two for the second ...).

**CP kill** is the order described above (E, G9, S9, G8, S8 ..., the monsters last). **CP death** is the same enemy and the same rules (no epic bonuses, Specialists double damage, only the bonus against flying, no Double hit, groups of equals, stacks tight by health), but the order is the one that gives the most damage - the Specialists deal double damage, so they stand near the end and strike the most. A troop "has a bonus" when it has a squad bonus against flying. The order is:

1. all the **Engineers** (higher tier first)
2. the **Guardsmen and the full monster tiers without a bonus, by the rising SH ratio - the smaller ratio first** (strength per health with your multipliers; the later a troop stands, the more it strikes, so the higher ratio goes later): with the default numbers first the Beast Guardsman (Battle Griffin, the smallest ratio), then the Guardsmen (G9, G8 ... down to G1, the same ratio), then the monsters (all tiers, the highest ratio)
3. the **Guardsmen and the full monsters with a bonus**, mixed, the **lowest bonus first** (it dies first; the same bonus: the smaller SH ratio first, then the higher tier)
4. the **Specialists** the same way: without a bonus by the rising SH ratio (Royal Lion, the smaller ratio, then Duelist, Whitemane ...), then with a bonus, the lowest bonus first
5. at the very end the **partial monster tier** (the tier where the Dominance runs out, and the tiers below it; the same rules inside). It stands last because it has the lowest health: placed before the Specialists it would pull their stacks down. It is what spends the Dominance that is left (with the default numbers M9 and M8 are full and M7 is the partial tier). The partial tier is always a group of its own.

Every rule works for all the tiers you tick, down to tier 1 (the order is built from the ticked tiers, nothing is fixed to tiers 8 and 9). **Groups: the SH ratio decides first, only troops with the same ratio and the same bonus form a group** - they stand together and get about the same health (as equal as whole units allow); troops with a different ratio (monsters, Guardsmen, Beast units) are NOT forced to the same health, they follow each other in the order with the small step down between the groups. In CP death the tier does not matter (G9 and G8 without a bonus have exactly the same ratio, so they are one group; the same for the Specialists and the monsters), in CP kill the group is class + tier + bonus + ratio (the Royal Lion is then a group of its own in front of the Duelist group of its tier). An Engineer is a group of its own. A monster stack has only a few big units, so a monster group can differ by some tenths of a percent (it cannot be closer than one unit); because the next group has to stay below the smallest stack of the group before, a very big monster group (all tiers 1-9 ticked) can leave a part of the Leadership unspent - with the usual tiers (8 and 9, or 7-9) nearly all of it is spent. The full monster tiers follow the army's level (the Dominance decides when it is short). The number of full monster tiers is chosen by the damage (every choice is solved, the most damage wins). The total health never rises along the order. In both modes the Leadership that the chain cuts away (a stack that has to stay below a smaller stack before it) is given back to the whole army: the level of all the army stacks is raised as far as the chain and the Leadership allow, so only a few units stay unspent.

## How the order is chosen

These notes used to be shown inside the page, under "Show the dying order, troop by troop" (the list is as wide as the page).

### 3-, 4-, 6- and 8-stack (one engine)

All four modes use the same logic. They differ only in K, the number of enemy stacks, and in whether the enemy has a mounted stack.

- **Goal:** maximum damage. A troop in place `p` strikes `ceil(p / K)` times, so the strongest squad bonuses belong among the last places.
- **Ratio groups:** all troops (engineers, army and monsters together) are grouped by strength / health (SH). Troops with the same or nearly the same ratio (within 2.5 %) stay together in one group. Engineers are ordinary troops: they usually come first only because they almost always have the lowest ratio.
- **Inside a group** the smaller squad bonus dies first, so the strongest bonuses are among the last. Tiers are mixed. When troops have the same ratio and the same bonus, the higher tier dies first (for example E9 before E8).
- **Order of the groups:** the order that gives the most damage with all the Leadership spent. Lowest ratio first is tried first; the monsters usually have the highest ratio, so they usually come after the army, but there is no fixed rule.
- **Outliers:** the places `Kn+1` are exempt from the strength rule, so a small group of outliers (for example Royal Lion and Battle Griffin, or a group with a very different ratio) may stand there, each on the place that suits its squad bonus. Not every `Kn+1` place has to be used.

| Mode | K | `Kn+1` places | Mounted enemy |
|------|---|---------------|---------------|
| 3-stack | 3 | 4, 7, 10 ... | no |
| 4-stack | 4 | 5, 9, 13 ... | yes |
| 6-stack | 6 | 7, 13, 19 ... | no |
| 8-stack | 8 | 9, 17, 25 ... | yes |

In the 3- and 6-stack modes the squad bonus is counted against melee, ranged and flying only, so many army troops show 0 % and ties are ordered by category and tier.

### Leadership and Dominance

- **Leadership** (army): all of it is spent. An order that leaves more than 0.1 % unused only wins when no other order spends it.
- **Dominance** (monsters) is used tier by tier from the top. The strongest monster tiers are used fully, on the army's health level, for as long as the Dominance reaches. The next tier is the partial one: it takes what is left and stands at the end of the order. Tiers below it get nothing. **The army's level is a ceiling only while it is useful.** If every selected monster tier standing on the army's level still cannot spend the Dominance (a small Leadership, a big Dominance, only one monster tier selected, no army tier selected or Leadership 0), the ceiling is lifted: the Dominance is the only limit and the whole of it goes to the monsters, on one common level above the army's. The damage then decides how many monster tiers are full (e.g. Leadership 0 with M7 + M8 + M9: 3- and 4-stack use M9 + M8, 6- and 8-stack only M9; on a tie the larger number of tiers wins), and the monsters stand in front of the army in the dying order when their stacks are bigger. When the army's level can absorb the Dominance nothing changes (the monsters stand on the army's level, as before).
- So a tier never depends on the tiers below it: leaving the lowest tier out does not change the others. When there is enough Dominance for every selected tier, they are all full and ordered together by squad bonus.

### Stack sizes

- Every stack aims for about the same total health, stepping down slightly along the order.
- Total strength (without squad bonus) must not rise along the order, so a health gap shows only where the strength rule forces it, for example where the strength / health ratio rises.
- The `Kn+1` places and the engineers are exempt from the strength rule; they only follow the health of the stack before them.

### Dying order list

Each row of "Show the dying order, troop by troop" shows the troop, its squad bonus and: SH (strength / health), Health, Strength (without squad bonus) and Damage (strength with the squad bonus and the other damage modifiers applied).

The bonus is written as the troop's best bonus against a class of the enemy, for example `+333% vs. mounted`. In the 3- and 6-stack modes there is no mounted enemy, so a bonus against mounted is still shown but it is not counted in Damage.

### Renegades

The button is in the PvP row. **Switched off for now** (the constant `RENEGADES = false` in the page): the button is greyed out and does nothing, and a tab that was saved in Renegades opens in Max damage instead. Nothing else was removed - set the constant to `true` to bring it back.

Highest troop types die first, G before S, up to 16 stacks. Then all the rest of the army is equal and dies at random. These rules maximize the damage and reduce the cost of attacks.

### Killshot v. 3

Killshot is a special type of the 3-stack mode. The enemy is the same (3 stacks, no mounted one) and the damage is counted the same way, but a little of the total damage is sacrificed for a drastically reduced cost of training and reviving. With the default inputs it deals under 1 % less than the 3-stack mode.

To get that, the order does not come from the damage search. All the engineers stand first (higher tier first), then the army tier by tier from the top, so the top level units die first. Inside a tier the weaker troops die first. The monsters stand after the army, the fully used tiers first. Royal Lion and Battle Griffin stand on the places 4, 7, 10 ... as in the 3-stack mode.
