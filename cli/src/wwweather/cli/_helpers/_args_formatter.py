from collections.abc import Iterable

from . import ABCArgsFormatter


class DefaultArgsFormatter(ABCArgsFormatter):
    """
    Default CLI arguments formatter - implements :class:`ABCArgsFormatter` abstraction.
    Provides simple args formatting, based on the Python's formatted strings.

    **Format patterns convention**

    To be supported, formatted string patterns must:
    * follow the C-style Python's formatted strings syntax
    * contain at least one named placeholder with the name '`base`', which will be replaced
      with the base string, provided at the time of generation
    """

    _dest_fmt: str
    _metavar_fmt: str

    _flags_fmt: str | None
    _flags_compact_fmt: str | None

    def __init__(self,
                 dest_fmt: str,
                 metavar_fmt: str = None,
                 flags_fmt: str = None,
                 flags_compact_fmt: str = None):
        """
        Initialize new :class:`DefaultArgsFmtParams` instance.

        **INFO:** see :class:`DefaultArgsFmtParams` class docs for details about formating patterns

        :param dest_fmt: argument's `dest` parameter formating pattern
        :param metavar_fmt: argument's `metavar` parameter formating pattern (defaults to the `dest_fmt`)
        :param flags_fmt: argument's full-format flags formating pattern (optional, if not specified
                          full-format flags formatting will not be supported)
        :param flags_compact_fmt: argument's compact-format flags formating pattern (optional, if not specified
                                  compact-format flags formatting will not be supported)
        """

        self._dest_fmt = dest_fmt
        self._metavar_fmt = metavar_fmt

        self._flags_fmt = flags_fmt
        self._flags_compact_fmt = flags_compact_fmt

    def dest(self, base: str) -> str:

        return self._dest_fmt % {'base': base}

    def metavar(self, base: str) -> str:

        return self._metavar_fmt % {'base': base}

    def flags(self, *bases: str) -> Iterable[str] | None:

        return None if self._flags_fmt is None else (self._flags_fmt % {'base': base} for base in bases)

    def flags_compact(self, *bases: str) -> Iterable[str] | None:

        return None if self._flags_compact_fmt is None else (self._flags_compact_fmt % {'base': base} for base in bases)
