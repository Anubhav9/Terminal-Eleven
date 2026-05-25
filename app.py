from textual.app import App

from screens.fixtures.fixtures_screen import FixturesScreen
from screens.groups.groups_screen import GroupsScreen
from screens.live_scores.live_scores_screen import LiveScoresScreen
from screens.main.main_screen import MainScreen


class TerminalElevenApp(App[None]):
    """Application shell and screen orchestration for Terminal Eleven."""

    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.install_screen(MainScreen(), name="main")
        self.install_screen(GroupsScreen(), name="groups")
        self.install_screen(LiveScoresScreen(), name="live-scores")
        self.install_screen(FixturesScreen(), name="fixtures")
        self.push_screen("main")


def main() -> None:
    TerminalElevenApp().run()


if __name__ == "__main__":
    main()
