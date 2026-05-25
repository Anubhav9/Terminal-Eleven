from __future__ import annotations

from datetime import datetime, timedelta, timezone

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import DataTable, Header, Static

from screens.match_detail.match_data import demo_snapshot
from screens.match_detail.match_detail_screen import MatchDetailScreen
from static_data.fixtures.loader import Fixture, load_group_stage_fixtures


def _format_offset(offset: timedelta) -> str:
    total = int(abs(offset.total_seconds()))
    sign = "+" if offset >= timedelta(0) else "-"
    hours, rem = divmod(total, 3600)
    minutes = rem // 60
    return f"{sign}{hours:02d}:{minutes:02d}"


class LiveScoresScreen(Screen[None]):
    """Live scores from the 2026 FIFA World Cup."""

    CSS_PATH = "live_scores.tcss"
    BINDINGS = [
        ("b", "app.pop_screen", "Back"),
        ("escape", "app.pop_screen", "Back"),
        ("d", "preview_match", "Preview: Japan vs Spain (WC 2022, live ESPN data)"),
    ]

    # A finished real match from WC 2022 (group stage, 1 Dec 2022).
    # Used by the `d` preview binding so the user can see the match-detail
    # screen rendering live ESPN data even though the 2026 tournament hasn't
    # started yet. ESPN event id 633828.
    _DEMO_FIXTURE = Fixture(
        match_no=0,
        group="E",
        team_a="Japan",
        team_b="Spain",
        venue="Khalifa International Stadium, Al Rayyan",
        utc_datetime=datetime(2022, 12, 1, 19, 0, tzinfo=timezone.utc),
        espn_event_id="633828",
    )

    def __init__(self) -> None:
        super().__init__()
        self._fixtures: list[Fixture] = []
        self._today_fixtures: list[Fixture] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="live-scores-shell"):
            yield Static("LIVE SCORES", id="live-scores-title")
            yield Static("", id="live-scores-clock")
            yield Static("", id="live-scores-date-header")
            yield DataTable(
                id="live-scores-table",
                zebra_stripes=True,
                cursor_type="row",
            )
            yield Static(
                "Press Enter on a row to fetch its live score.",
                id="live-scores-hint",
            )
            yield Static("Press b to go back", id="live-scores-back-hint")

    def on_mount(self) -> None:
        self._fixtures = load_group_stage_fixtures()

        table = self.query_one("#live-scores-table", DataTable)
        table.add_column("Kickoff (Local)", key="kickoff", width=18)
        table.add_column("Team A", key="team_a", width=22)
        table.add_column("Team B", key="team_b", width=22)
        table.add_column("Venue", key="venue", width=34)
        table.add_column("Action", key="action", width=18)

        self._refresh_clock()
        self._populate_table()

        # Update the clock every second, and refresh the day's match list
        # every minute in case the local date rolls over while the user
        # has the screen open.
        self.set_interval(1.0, self._refresh_clock)
        self.set_interval(60.0, self._populate_table)

    def _refresh_clock(self) -> None:
        now_utc = datetime.now(tz=timezone.utc)
        local = now_utc.astimezone()
        tz_label = local.tzname() or "Local"
        offset_str = _format_offset(local.utcoffset() or timedelta(0))
        text = (
            f"Local: {local.strftime('%I:%M:%S %p')}  {tz_label} (UTC{offset_str})"
            f"     UTC: {now_utc.strftime('%H:%M:%S')}"
        )
        self.query_one("#live-scores-clock", Static).update(text)

    def _populate_table(self) -> None:
        now_utc = datetime.now(tz=timezone.utc)
        local_now = now_utc.astimezone()
        local_today = local_now.date()

        today_fixtures = [
            f for f in self._fixtures
            if f.utc_datetime.astimezone().date() == local_today
        ]
        self._today_fixtures = today_fixtures

        date_str = local_now.strftime("%A, %d %B %Y")
        header_widget = self.query_one("#live-scores-date-header", Static)
        if today_fixtures:
            header_widget.update(
                f"Today's Matches — {date_str} ({len(today_fixtures)} fixture"
                f"{'s' if len(today_fixtures) != 1 else ''})"
            )
        else:
            next_fixture = next(
                (f for f in self._fixtures if f.utc_datetime > now_utc),
                None,
            )
            if next_fixture is not None:
                next_local = next_fixture.utc_datetime.astimezone()
                header_widget.update(
                    f"No matches today ({date_str}).  "
                    f"Next up: {next_fixture.team_a} v {next_fixture.team_b} — "
                    f"{next_local.strftime('%a %d %b at %I:%M %p')}"
                )
            else:
                header_widget.update(
                    f"No more group-stage matches scheduled ({date_str})."
                )

        table = self.query_one("#live-scores-table", DataTable)
        table.clear()
        for f in today_fixtures:
            local_dt = f.utc_datetime.astimezone()
            table.add_row(
                local_dt.strftime("%I:%M %p"),
                f.team_a,
                f.team_b,
                f.venue,
                "▶ Fetch Score",
                key=str(f.match_no),
            )

    def action_preview_match(self) -> None:
        """Dev preview — open the match-detail screen pointed at a finished
        real ESPN event (Japan vs Spain, WC 2022 group stage).

        Initial render uses ``demo_snapshot`` only so the layout isn't blank
        before the first httpx call returns; the on-mount ``_refresh`` worker
        then overwrites everything with the actual ESPN payload.
        """
        fixture = self._DEMO_FIXTURE
        initial = demo_snapshot(fixture.team_a, fixture.team_b)
        self.app.push_screen(MatchDetailScreen(fixture, initial))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        match_no_str = str(event.row_key.value) if event.row_key.value is not None else None
        fixture = next(
            (f for f in self._today_fixtures if str(f.match_no) == match_no_str),
            None,
        )
        if fixture is None:
            return
        # Until the ESPN fetch is wired in, show a demo snapshot of the
        # match detail layout so we can iterate on the design.
        snap = demo_snapshot(fixture.team_a, fixture.team_b)
        self.app.push_screen(MatchDetailScreen(fixture, snap))
