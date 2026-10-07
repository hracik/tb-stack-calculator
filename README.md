# Total Battle Stack Calculator

A single-file calculator for Total Battle. It works out how many troops of each type to send (Leadership = army pool, Dominance = monster pool) and in which order they should die, for the 3-, 4-, 6- and 8-stack modes and the special modes (Killshot v. 3 and Renegades).

Open `index.html` in a browser or use the GitHub Pages site of this repository. Nothing is installed or uploaded; everything is calculated in the page.

## Attack modes

The modes are in three rows: Regular (4-stack, 8-stack), Sniper (3-stack, 6-stack) and Special (Killshot v. 3, Renegades).

## Troop data

The troop lists are written inside the page. For every troop (army, monsters, engineers, mercenaries) they store the health, the strength, the food consumption (all mercenaries use no food), the Leadership / Dominance / Authority cost and the vs melee / ranged / mounted / flying bonuses exactly as in the troop JSON. The strength is stored, not calculated from the health. The summary line above the result shows the **food consumption** of all the units together (number of units x food per unit), before the estimated damage.

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

Above the result there is a View switch: **Grouped**, **Mobile** and **Computer**.

- **Grouped** (the default) is the cards in groups, 5 per row, with the label of a group (for example Guardsmen 9) in one row above its cards, one block for the Mercenaries, one for the Monsters and one for the Army (in this order, in every view).
- **Mobile**: one unit per line. The line starts with the picture; to the right of it is the name of the unit and below the name the number of units. The three sections (Mercenaries - Authority, Monsters - Dominance, Army - Leadership) keep their headings. A line can be clicked to turn the troop off or on, like a card, and it shows the `#` number (the place in the kill order) at the right edge, as the Grouped cards do. Inside every section the units stand by the **original health of one unit, the biggest first** (Mercenaries: Wyvern, Warden, Eternal Cannoneer, Demonic Salamander, Warregal, Jago, Ariel, Superior Epic Monster Hunter, Quicksand, Galloper, Highlander, Slavic Warrior, Pounder, Scarface, Grace; Monsters: Kraken, Fire Phoenix, Devastator, Trickster of tier 9, then 8, then Wind Lord, Black Dragon, Destructive Colossus, Ancient Terror, then the lower tiers the same way; Army: Corax II, Royal Lion II, Corax I, Royal Lion I, Josephine II, Josephine I, ...). Units with the same health: the mercenary list order, then the higher tier, Guardsmen before Specialists, then ranged before melee (the full order: flying, mounted, ranged, melee), then the order of the Grouped cards. The Grouped view keeps its own order.
- **Computer**: the same lines as Mobile in two columns - the units 1 and 2 next to each other, 3 and 4 in the next row, and so on. The order is the Mobile order with a few units moved by hand: Mercenaries ... Highlander, Scarface, Pounder, Slavic Warrior, Grace; Monsters as in Mobile; Army: Royal Lion II, Corax II, Corax I, Royal Lion I, Josephine II, Josephine I, Smiter II, Whitemane II, Smiter I, Whitemane I, Purifier II, Punisher II, Legitimist II, Duelist II, and last Legitimist I, Punisher I, Duelist I, Purifier I. Clicking a line turns the troop off or on.

The chosen view is one setting for the whole page (saved in the browser, not per tab).

### Multiplier

Under the View switch there is a **Multiplier** box with `−` and `+` (default 1, the minimum is 1; you can also type a number). With 2, 3, 4 ... every unit number, the food consumption and the estimated damage are multiplied by it, to see what several hits (or several armies) bring. The 1x number always stays the main one; when the multiplier is more than 1 the multiplied number is shown as a second, smaller number (`×3: 6,192` under a card or after the number on a Mobile / Computer line, and a second row under the summary line: `3 hits · food consumption 47,970,720 · estimated damage 17.18 T`). Not multiplied: the Leadership / Dominance / Authority used, the number of stacks and strikes, the `#` kill order. The multiplier is saved per tab, like the other settings; a troop that is turned off shows no second number.

## Tabs

The page starts with four tabs: `1 cap`, `3 cap`, `Hero` and `Hero+3 cap`. They are ordinary tabs: rename (double-click), duplicate or delete them, or add your own with `+`. Each tab keeps its own settings, saved in your browser only.

## How the order is chosen

These notes used to be shown inside the page, under "Show the dying order, troop by troop".

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
- **Dominance** (monsters) is used tier by tier from the top. The strongest monster tiers are used fully, on the army's health level, for as long as the Dominance reaches. The next tier is the partial one: it takes what is left and stands at the end of the order. Tiers below it get nothing.
- So a tier never depends on the tiers below it: leaving the lowest tier out does not change the others. When there is enough Dominance for every selected tier, they are all full and ordered together by squad bonus.

### Stack sizes

- Every stack aims for about the same total health, stepping down slightly along the order.
- Total strength (without squad bonus) must not rise along the order, so a health gap shows only where the strength rule forces it, for example where the strength / health ratio rises.
- The `Kn+1` places and the engineers are exempt from the strength rule; they only follow the health of the stack before them.

### Dying order list

Each row of "Show the dying order, troop by troop" shows the troop, its squad bonus and: SH (strength / health), Health, Strength (without squad bonus) and Damage (strength with the squad bonus and the other damage modifiers applied).

The bonus is written as the troop's best bonus against a class of the enemy, for example `+333% vs. mounted`. In the 3- and 6-stack modes there is no mounted enemy, so a bonus against mounted is still shown but it is not counted in Damage.

### Renegades

Highest troop types die first, G before S, up to 16 stacks. Then all the rest of the army is equal and dies at random. These rules maximize the damage and reduce the cost of attacks.

### Killshot v. 3

Killshot is a special type of the 3-stack mode. The enemy is the same (3 stacks, no mounted one) and the damage is counted the same way, but a little of the total damage is sacrificed for a drastically reduced cost of training and reviving. With the default inputs it deals under 1 % less than the 3-stack mode.

To get that, the order does not come from the damage search. All the engineers stand first (higher tier first), then the army tier by tier from the top, so the top level units die first. Inside a tier the weaker troops die first. The monsters stand after the army, the fully used tiers first. Royal Lion and Battle Griffin stand on the places 4, 7, 10 ... as in the 3-stack mode.
