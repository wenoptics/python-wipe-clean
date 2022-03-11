import os
import platform
import sys
from typing import Mapping, Optional, Callable, NamedTuple, IO, AnyStr

from ._windows import WindowsConsoleFeatures

WINDOWS = platform.system() == 'Windows'
_windows_console_features: Optional["WindowsConsoleFeatures"] = None


def get_windows_console_features() -> "WindowsConsoleFeatures":  # pragma: no cover
    global _windows_console_features
    if _windows_console_features is not None:
        return _windows_console_features
    from ._windows import get_windows_console_features

    _windows_console_features = get_windows_console_features()
    return _windows_console_features


class ConsoleDimensions(NamedTuple):
    """Size of the terminal."""

    width: int
    """The width of the console in 'cells'."""
    height: int
    """The height of the console in lines."""


class SimpleConsole:
    """This is port from `rich`. It is mostly a subset of a rich.console.Console"""

    _environ: Mapping[str, str] = os.environ

    def __init__(self, file: Optional[IO[str]] = None):
        self._file = file
        self._buffer = []

    @property
    def file(self) -> IO[str]:
        """Get the file object to write to."""
        file = self._file or sys.stdout
        return file

    @property
    def is_terminal(self) -> bool:
        """Check if the console is writing to a terminal.

        Returns:
            bool: True if the console writing to a device capable of
            understanding terminal codes, otherwise False.
        """
        isatty: Optional[Callable[[], bool]] = getattr(self.file, "isatty", None)
        try:
            return False if isatty is None else isatty()
        except ValueError:
            # in some situation (at the end of a pytest run for example) isatty() can raise
            # ValueError: I/O operation on closed file
            # return False because we aren't in a terminal anymore
            return False

    @property
    def is_dumb_terminal(self) -> bool:
        """Detect dumb terminal.

        Returns:
            bool: True if writing to a dumb terminal, otherwise False.

        """
        _term = self._environ.get("TERM", "")
        is_dumb = _term.lower() in ("dumb", "unknown")
        return self.is_terminal and is_dumb

    @property
    def legacy_windows(self) -> bool:
        return WINDOWS and not get_windows_console_features().vt

    @property
    def size(self) -> ConsoleDimensions:
        """Get the size of the console.

        Returns:
            ConsoleDimensions: A named tuple containing the dimensions.
        """
        if self.is_dumb_terminal:
            return ConsoleDimensions(80, 25)

        width: Optional[int] = None
        height: Optional[int] = None

        if WINDOWS:  # pragma: no cover
            try:
                width, height = os.get_terminal_size()
            except OSError:  # Probably not a terminal
                pass
        else:
            try:
                width, height = os.get_terminal_size(sys.__stdin__.fileno())
            except (AttributeError, ValueError, OSError):
                try:
                    width, height = os.get_terminal_size(sys.__stdout__.fileno())
                except (AttributeError, ValueError, OSError):
                    pass

        columns = self._environ.get("COLUMNS")
        if columns is not None and columns.isdigit():
            width = int(columns)
        lines = self._environ.get("LINES")
        if lines is not None and lines.isdigit():
            height = int(lines)

        # get_terminal_size can report 0, 0 if run from pseudo-terminal
        width = width or 80
        height = height or 25
        return ConsoleDimensions(
            width - self.legacy_windows,
            height
        )

    def write(self, s: AnyStr):
        self._buffer += s

    def flush(self):
        self.file.write(''.join(self._buffer))
        self._buffer = []
        self.file.flush()
