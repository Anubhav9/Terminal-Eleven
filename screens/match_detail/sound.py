"""Fire-and-forget sound effects for live match events.

Used by :class:`MatchDetailScreen` so the user can leave the match running
in the background and still hear when a goal is scored or the period
changes.

Cross-platform strategy (no third-party deps):

* **Goal** always plays the same bundled ``goal.wav`` (a Game Boy-style
  victory stinger by Bogart — see ``sounds/ATTRIBUTION.md``). Same
  asset on every OS so users hear the same celebration regardless of
  platform.
* **Whistle** plays the bundled ``whistle.wav``, falling back to a nice
  built-in macOS system sound where available.
* **Playback backend** per OS:
    - macOS  → ``afplay``
    - Linux  → ``paplay`` (PulseAudio) → ``pw-play`` (PipeWire) →
               ``aplay`` (ALSA), whichever is found first
    - Windows → stdlib ``winsound.PlaySound``
* **Last resort** — terminal bell (``app.bell()``).

Playback is always non-blocking and never raises.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal

from textual.app import App


SoundName = Literal["goal", "half_time", "full_time", "whistle", "info"]


# ─── asset locations ──────────────────────────────────────────────────────────

_SOUNDS_DIR = Path(__file__).parent / "sounds"

_BUNDLED_WAVS: dict[SoundName, Path] = {
    "goal":      _SOUNDS_DIR / "goal.wav",
    "half_time": _SOUNDS_DIR / "half_time.wav",
    "full_time": _SOUNDS_DIR / "full_time.wav",
    # ``whistle`` is the legacy alias kept for the test binding; it now
    # points at the same single-blast asset as ``half_time``.
    "whistle":   _SOUNDS_DIR / "half_time.wav",
    "info":      _SOUNDS_DIR / "goal.wav",
}

_MAC_SYSTEM_SOUNDS: dict[SoundName, str] = {
    "goal":      "/System/Library/Sounds/Hero.aiff",
    "half_time": "/System/Library/Sounds/Submarine.aiff",
    "full_time": "/System/Library/Sounds/Submarine.aiff",
    "whistle":   "/System/Library/Sounds/Submarine.aiff",
    "info":      "/System/Library/Sounds/Glass.aiff",
}

# Linux players we try in order. paplay is PulseAudio, pw-play is PipeWire,
# aplay is ALSA — between them they cover essentially every modern desktop.
_LINUX_PLAYERS: tuple[str, ...] = ("paplay", "pw-play", "aplay")


# ─── public API ───────────────────────────────────────────────────────────────


def play(name: SoundName, *, app: App | None = None) -> None:
    """Play a named effect without blocking. Never raises.

    Always prefers the bundled WAV (consistent across OSes), then falls
    back to a macOS system sound, then to the terminal bell.

    Parameters
    ----------
    name:
        Logical effect name — see :data:`SoundName`.
    app:
        Used only for the terminal-bell fallback. Safe to pass ``None``.
    """
    if _play_bundled_wav(name):
        return
    if sys.platform == "darwin" and _play_macos_system_sound(name):
        return
    if app is not None:
        app.bell()


# ─── bundled WAV playback (the primary path on every OS) ──────────────────────


def _play_bundled_wav(name: SoundName) -> bool:
    """Play the bundled WAV for ``name`` using the right backend for this OS."""
    wav = _BUNDLED_WAVS.get(name)
    if wav is None or not wav.exists():
        return False

    if sys.platform == "win32":
        return _play_with_winsound(wav)

    # Everywhere else: try a list of CLI players in priority order.
    for player in _wav_players_for_platform():
        exe = shutil.which(player)
        if exe and _spawn_player(exe, wav):
            return True
    return False


def _wav_players_for_platform() -> tuple[str, ...]:
    """Return the CLI WAV-player names to try, ordered by preference."""
    if sys.platform == "darwin":
        return ("afplay", "ffplay", "play")
    if sys.platform.startswith("linux"):
        return _LINUX_PLAYERS + ("ffplay", "play")
    # BSD / unknown unix
    return _LINUX_PLAYERS + ("afplay", "ffplay", "play")


def _play_with_winsound(wav: Path) -> bool:
    """Windows-only: stdlib ``winsound.PlaySound`` with SND_ASYNC."""
    try:
        import winsound  # type: ignore[import-not-found]
    except ImportError:
        return False
    try:
        winsound.PlaySound(
            str(wav),
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT,
        )
        return True
    except (RuntimeError, OSError):
        return False


# ─── macOS system-sound fallback ──────────────────────────────────────────────


def _play_macos_system_sound(name: SoundName) -> bool:
    """Last-resort macOS playback against built-in ``/System/Library/Sounds``."""
    afplay = shutil.which("afplay")
    if afplay is None:
        return False
    path = _MAC_SYSTEM_SOUNDS.get(name)
    if path is None or not Path(path).exists():
        return False
    return _spawn_player(afplay, Path(path))


# ─── subprocess helper ────────────────────────────────────────────────────────


def _spawn_player(exe: str, path: Path | None) -> bool:
    """Spawn ``exe path`` in a detached subprocess. Returns True on launch."""
    if path is None:
        return False
    args = [exe, str(path)]
    # ffplay needs flags to actually run headless.
    if exe.endswith("ffplay"):
        args = [exe, "-nodisp", "-autoexit", "-loglevel", "quiet", str(path)]
    try:
        subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,  # detach from our process group
        )
        return True
    except OSError:
        return False
