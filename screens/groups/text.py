from screens.text import TextSpec

TITLE = TextSpec(
    text="GROUPS",
    id="groups-title",
    font_color="#ffbf69",
    font_size="large",
    font_type="terminal",
    text_style="bold",
)
SUBTITLE = TextSpec(
    text="48 teams. 12 groups. The road starts here.",
    id="groups-subtitle",
    font_color="#7dd3fc",
    font_size="small",
    font_type="terminal",
)
BACK_HINT = TextSpec(
    text="Press b to go back",
    id="back-hint",
    font_color="#cbf3f0",
    font_size="small",
    font_type="terminal",
)


def format_team(team: dict[str, str]) -> str:
    """One line if short; two lines (word-wrapped) if long."""
    name = team["name"]
    flag = team["flag"]
    if len(f"{name}  {flag}") <= 20:
        return f"{name}  {flag}"
    split = name.rfind(" ", 0, 16)
    if split == -1:
        split = 15
    return f"{name[:split]}\n{name[split:].lstrip()}  {flag}"
