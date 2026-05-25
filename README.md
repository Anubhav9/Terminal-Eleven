# Terminal Eleven

The 2026 World Cup, in your terminal. Built for people who can't watch it any other way.

---

Here in India, most of the matches kick off between 11:30 PM and 7:30 AM. The final is at 12:30 AM. And as far as anyone can tell, no broadcaster has bought the Indian rights yet. China is in the same spot.

So roughly two billion football fans get to follow the biggest tournament on the planet by refreshing tabs. Or just... not.

I'm one of them. This is what I built so I could still follow the games without keeping a phone awake at 4 AM.

## What it does

Four screens, all keyboard-driven, all dark-theme.

**Groups.** All twelve groups in a responsive grid. Click any team to open its profile — captain, coach, nickname, confederation, best-ever World Cup finish, and how it did in Qatar 2022.

**Fixtures.** Every group-stage match grouped by date, with kickoff times converted to *your* local timezone. So you can tell at a glance whether Brazil v Morocco lands in your evening or your 3 AM.

**Live Score.** Today's matches in a table. Pick one with Enter.

**Match Detail.** Big block-font scoreline, current minute, goal scorers under each team, yellow and red cards, and a live stats grid (possession, shots, shots on target, passes, pass accuracy, fouls, corners). Polled from ESPN every 60 seconds and patched in place — no flicker, no full redraw.

## The reason I actually wanted this

Open a match in a terminal tab. Switch to your editor. Forget about it. When something happens, the app tells you:

- a Game Boy-style victory stinger when a goal goes in,
- a desktop notification with who scored, what minute, and the new scoreline,
- one referee whistle at half-time,
- three referee whistles at full-time.

Works on macOS, Linux and Windows without any extra audio library to install — just Python plus the system audio tool each OS already ships with (`afplay`, `paplay` / `pw-play` / `aplay`, `winsound`). Run it on your laptop, run it over SSH on a server, run it on the office Linux box. As long as the machine can make a noise, you'll know when Argentina scores.

That's the part I wouldn't have got from any other app.

## Install

From PyPI:

```bash
pip install terminal-eleven
terminal-eleven
```

Or from source:

```bash
git clone https://github.com/Anubhav9/Terminal-Eleven
cd Terminal-Eleven
pip install -e .
terminal-eleven
```

Quit with `q`. Back out of any screen with `b` or `Esc`. Move with arrow keys, select with Enter.

## How it gets the data

ESPN has an undocumented but very reliable JSON endpoint behind the live-score pages on espn.com. We fetch it with `httpx` from a Textual async worker, parse the bits we care about (score, status, key events, boxscore), and only emit sound + a toast when the new snapshot actually differs from the previous one — so a single goal makes exactly one celebration noise, not one per refresh.

The 72 group-stage fixtures and their ESPN event IDs are checked into the repo (`terminal_eleven/static_data/fixtures/group_stage.csv`), so everything except the live view works fully offline.

## A note on prior art

If you want a general football TUI that does 65+ leagues year-round, look at [golazo](https://github.com/0xjuanma/golazo). It's mature, polished, and the reason I knew this kind of thing was even possible in a terminal.

Terminal Eleven is narrower on purpose. It runs for four weeks of your year, knows exactly which 48 teams and 72 matches matter, and has the half-time / full-time audio cues I wanted. That's the whole pitch.

## Credits

- Victory stinger: *GB Victory Stinger* by **Bogart** ([OpenGameArt](https://opengameart.org/content/gb-victory-stinger-and-game-over-man))
- Referee whistles: *Whistles* by **dklon**, CC-BY 3.0 ([OpenGameArt](https://opengameart.org/content/whistles))
- Group-stage fixture data parsed from the [Wikipedia article](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup).
- Live match data via ESPN's public scoreboard / summary endpoints.
- Built on [Textual](https://textual.textualize.io/) and [httpx](https://www.python-httpx.org/).

---

If this helps you make it through a 4 AM goal-scoring update, a GitHub star is the nicest way to say thanks. It also helps the next person searching for "how do I watch the World Cup from India" find this instead of nothing.
