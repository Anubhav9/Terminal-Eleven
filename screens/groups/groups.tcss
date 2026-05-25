from __future__ import annotations

from rich.cells import cell_len

from textual import events
from textual.app import ComposeResult
from textual.containers import Container, Grid, VerticalScroll
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Header, Static

from screens.groups.text import BACK_HINT, SUBTITLE, TITLE
from screens.team.team_screen import TeamScreen
from screens.text import render_static
from static_data.groups import GROUPS

WIDE_WIDTH = 110  # >= this terminal width → 4 columns, else 3
MAX_CELL = 18


def format_team(team: dict) -> str:
    name = team["name"]
    if cell_len(name) <= MAX_CELL:
        return name
    split = name.rfind(" ", 0, 12)
    if split == -1:
        split = 12
    return f"{name[:split]}\n{name[split:].lstrip()}"


class TeamButton(Static):
    """A clickable, focusable team cell."""

    can_focus = True

    class Clicked(Message):
        def __init__(self, team_name: str) -> None:
            super().__init__()
            self.team_name = team_name

    def __init__(self, team_name: str) -> None:
        super().__init__(format_team({"name": team_name}), classes="team-cell")
        self.team_name = team_name

    def on_click(self) -> None:
        self.post_message(self.Clicked(self.team_name))

    def on_key(self, event: events.Key) -> None:
        if event.key in ("enter", "space"):
            event.stop()
            self.post_message(self.Clicked(self.team_name))


class GroupsScreen(Screen[None]):
    CSS_PATH = "groups.tcss"
    BINDINGS = [("b", "app.pop_screen", "Back")]

    def __init__(self) -> None:
        super().__init__()
        self._columns: int | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="groups-shell"):
            yield render_static(TITLE)
            yield render_static(SUBTITLE)
            yield VerticalScroll(id="groups-scroll")
            yield render_static(BACK_HINT)

    def on_mount(self) -> None:
        self.call_after_refresh(self._rebuild, self.size.width)

    def on_show(self) -> None:
        # Rebuild on re-entry so it picks up state correctly
        scroll = self.query_one("#groups-scroll", VerticalScroll)
        if not scroll.children:
            self._columns = None
            self._rebuild(self.size.width)

    def on_resize(self, event: events.Resize) -> None:
        self._rebuild(event.size.width)

    def on_team_button_clicked(self, message: TeamButton.Clicked) -> None:
        self.app.push_screen(TeamScreen(message.team_name))

    def _rebuild(self, width: int) -> None:
        columns = 4 if width >= WIDE_WIDTH else 3
        if columns == self._columns:
            return
        self._columns = columns

        scroll = self.query_one("#groups-scroll", VerticalScroll)
        scroll.remove_children()

        cells: list[Static] = []
        bands = (len(GROUPS) + columns - 1) // columns
        for band in range(bands):
            band_groups = [
                GROUPS[band * columns + col] if band * columns + col < len(GROUPS) else None
                for col in range(columns)
            ]
            for group in band_groups:
                text = group["name"] if group else ""
                cells.append(Static(text, classes="header-cell"))
            for row in range(4):
                for group in band_groups:
                    if group is not None:
                        cells.append(TeamButton(group["teams"][row]["name"]))
                    else:
                        cells.append(Static("", classes="team-cell"))

        grid_class = "teams-grid" if columns == 4 else "teams-grid compact"
        rows = bands * 5
        grid = Grid(*cells, classes=grid_class)
        grid.styles.grid_size_rows = rows
        scroll.mount(grid)
