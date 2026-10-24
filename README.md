# Krappy Calculator

A free calculator for **Total Battle** that tells you how to build your army for a hit on an epic monster or on other players. It runs in your browser as one page (`index.html`, with `app.css`, `app.js` and `i18n.js` next to it). Nothing needs to be installed, and your inputs stay on your device.

## What it is for

You type in what you have (Leadership, Dominance, Authority and your bonuses). It tells you:

- **Which troops to send, how many of each, and in which order they should fall.** The aim is the most damage from the capacity you have.
- **What a hit is worth.** For epics you get an estimated damage and epic score, shown as a likely range, along with the number of strikes and the revive cost.
- **What to train.** The Preparation view turns your food production into the units to train per stack for the strongest hits.
- **How your own army compares.** Type your stacks or read them from battle report screenshots, and Compare shows the difference in damage, score, revive cost and strikes against the suggested army.
- **Whether other tiers would do better.** The Tier check looks for the tiers that give the most damage or the best damage per gold, and shows the next best choices.

## Attack modes

- **Epics:** 3-stack, 4-stack, 6-stack and 8-stack, plus Killshot v. 3 and v. 4, which give up a little damage for a much cheaper revive and training.
- **Players:** CP kill, CP death, One v. One, Max damage and Renegades.

## Handy to know

- Every tab keeps its own inputs, and you can have several, for example one per setup.
- Export turns a tab into a short text you can keep in a note or chat, and Import brings it back as a new tab.
- Battle in detail shows the target order, the strike order and a full battle report.
- Help buttons on each card explain where to find the numbers in the game.

## Feedback

Spotted something that looks wrong, or a mode or epic that is missing? Open an issue or tell the author.

## For the author: files and versions

- `index.html` holds the page; the styles are `app.css`, the program is `app.js`, the translations are `i18n.js`. `eng.traineddata.gz.b64.txt` is the language data of the screenshot reader (admin only, fetched only when used).
- Raise the version with `python3 bump.py MAJOR.MINOR.PATCH`. It writes the version into `app.js` (`APP_VERSION`), `version.json` and the `?v=` of the three files in `index.html`, so a browser never mixes an old file with a new page. Upload all files together.

## Traffic statistics

The page can report visits to GoatCounter (no cookies, no personal data). It is off until `GC_CODE` at the top of `app.js` holds the code of the GoatCounter site. It runs only on the live site, never for an admin account, and sends only the page visit plus once per visit the view, attack mode, epic and language in use. Nothing typed in the app, no export text and no account data is sent.
