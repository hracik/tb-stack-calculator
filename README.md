# Total Battle Stack Calculator

A single-file calculator for Total Battle. It works out how many troops of each type to send (Leadership = army pool, Dominance = monster pool) and in which order they should die, for the 3-, 4-, 6- and 8-stack modes and the special modes (Killshot v. 3 and Renegades).

Open `index.html` in a browser or use the GitHub Pages site of this repository. Nothing is installed or uploaded; everything is calculated in the page.

## Attack modes

The modes are in three rows: Regular (4-stack, 8-stack), Sniper (3-stack, 6-stack) and Special (Killshot v. 3, Renegades).

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
