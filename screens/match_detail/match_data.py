"""Typed match-snapshot data and a demo factory for layout previews."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Goal:
    scorer: str
    minute: str  # e.g. "24'" or "45+2'"


@dataclass(frozen=True)
class Card:
    player: str
    minute: str
    color: str  # "yellow" | "red"


@dataclass(frozen=True)
class TeamStats:
    possession_pct: int
    shots: int
    shots_on_target: int
    passes: int
    pass_accuracy_pct: int
    fouls: int
    corners: int
    offsides: int


@dataclass(frozen=True)
class MatchSnapshot:
    team_a: str
    team_b: str
    score_a: int
    score_b: int
    minute: str       # "63'", "HT", "FT", "0'"
    period: str       # "1st Half" | "2nd Half" | "Half Time" | "Full Time" | "Not Started"
    goals_a: list[Goal] = field(default_factory=list)
    goals_b: list[Goal] = field(default_factory=list)
    cards_a: list[Card] = field(default_factory=list)
    cards_b: list[Card] = field(default_factory=list)
    stats_a: TeamStats | None = None
    stats_b: TeamStats | None = None
    is_live: bool = False


def demo_snapshot(team_a: str, team_b: str) -> MatchSnapshot:
    """Realistic-looking placeholder used until the ESPN fetch is wired in."""
    return MatchSnapshot(
        team_a=team_a,
        team_b=team_b,
        score_a=2,
        score_b=1,
        minute="63'",
        period="2nd Half",
        is_live=True,
        goals_a=[
            Goal(scorer="Vega", minute="24'"),
            Goal(scorer="Lozano", minute="58'"),
        ],
        goals_b=[
            Goal(scorer="Mokoena", minute="45+2'"),
        ],
        cards_a=[
            Card(player="Edson Álvarez", minute="31'", color="yellow"),
        ],
        cards_b=[
            Card(player="Mvala", minute="17'", color="yellow"),
            Card(player="Modise", minute="55'", color="yellow"),
        ],
        stats_a=TeamStats(
            possession_pct=55, shots=12, shots_on_target=5,
            passes=412, pass_accuracy_pct=87,
            fouls=9, corners=6, offsides=2,
        ),
        stats_b=TeamStats(
            possession_pct=45, shots=8, shots_on_target=3,
            passes=367, pass_accuracy_pct=82,
            fouls=11, corners=3, offsides=1,
        ),
    )
