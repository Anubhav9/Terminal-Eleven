"""5-line block-font digit renderer for the score display."""

from __future__ import annotations

_DIGITS: dict[str, list[str]] = {
    "0": ["██████", "██  ██", "██  ██", "██  ██", "██████"],
    "1": ["    ██", "  ████", "    ██", "    ██", "    ██"],
    "2": ["██████", "    ██", "██████", "██    ", "██████"],
    "3": ["██████", "    ██", "██████", "    ██", "██████"],
    "4": ["██  ██", "██  ██", "██████", "    ██", "    ██"],
    "5": ["██████", "██    ", "██████", "    ██", "██████"],
    "6": ["██████", "██    ", "██████", "██  ██", "██████"],
    "7": ["██████", "    ██", "    ██", "    ██", "    ██"],
    "8": ["██████", "██  ██", "██████", "██  ██", "██████"],
    "9": ["██████", "██  ██", "██████", "    ██", "██████"],
}

_DIGIT_WIDTH = 6
_DIGIT_GAP = "  "


def render_big_number(n: int) -> str:
    """Return a 5-line block representation of a non-negative integer."""
    s = str(max(0, n))
    rows = ["", "", "", "", ""]
    for i, ch in enumerate(s):
        glyph = _DIGITS.get(ch, _DIGITS["0"])
        for r in range(5):
            if i > 0:
                rows[r] += _DIGIT_GAP
            rows[r] += glyph[r]
    return "\n".join(rows)
