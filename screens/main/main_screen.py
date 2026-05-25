from textual import events
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Header, ListItem, ListView, Static

from screens.main.text import (
    ASCII_TITLE,
    MEDIUM_ASCII_TITLE,
    MENU_ITEMS,
    MENU_TITLE,
    SMALL_ASCII_TITLE,
    SUBTITLE,
    TAGLINE,
    TITLE,
    TINY_ASCII_TITLE,
)
from screens.text import apply_text_spec, render_static

MIN_WIDTH_FOR_ASCII_TITLE = 92
MIN_WIDTH_FOR_MEDIUM_ASCII_TITLE = 76
MIN_WIDTH_FOR_SMALL_ASCII_TITLE = 64


class MainScreen(Screen[None]):
    """Landing screen for Terminal Eleven."""

    CSS_PATH = "main.tcss"

    def on_mount(self) -> None:
        self._sync_title_for_width(self.size.width)
        self.query_one("#menu", ListView).focus()

    def on_resize(self, event: events.Resize) -> None:
        self._sync_title_for_width(event.size.width)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="main"):
            yield render_static(TITLE)
            yield render_static(SUBTITLE)
            yield render_static(TAGLINE)
            yield render_static(MENU_TITLE)
            yield ListView(
                *(ListItem(render_static(item), id=item.styling.get("screen")) for item in MENU_ITEMS),
                id="menu",
            )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id != "menu" or event.item.id is None:
            return

        self.app.push_screen(event.item.id)

    def _sync_title_for_width(self, width: int) -> None:
        if width >= MIN_WIDTH_FOR_ASCII_TITLE:
            title = ASCII_TITLE
        elif width >= MIN_WIDTH_FOR_MEDIUM_ASCII_TITLE:
            title = MEDIUM_ASCII_TITLE
        elif width >= MIN_WIDTH_FOR_SMALL_ASCII_TITLE:
            title = SMALL_ASCII_TITLE
        else:
            title = TINY_ASCII_TITLE

        apply_text_spec(self.query_one("#title", Static), TITLE, text=title)
