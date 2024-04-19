from abc import ABCMeta
from collections.abc import Iterable

# noinspection PyUnresolvedReferences
from argparse import ArgumentParser


class ABCArgsFormatter(metaclass=ABCMeta):
    """
    CLI arguments formatter abstraction.
    Designed to be used with the `argparse` module and declares methods for formatting all basic name-related
    parameters typically needed to add a new argument to the `argparse`'s :class:`ArgumentParser`
    """

    def dest(self, base: str) -> str:
        """
        Format argument's `dest` parameter from the given base string.

        Where `dest` - the name of the parse results object attribute corresponds to the given argument.
        See :meth:`ArgumentParser.add_argument` method docs for more details about the `dest` parameter.
        """

    def metavar(self, base: str) -> str:
        """
        Format argument's `metavar` parameter from the given base string.

        Where `metavar` - the name for the given argument in the usage message.
        See :meth:`ArgumentParser.add_argument` method docs for more details about the `dest` parameter.
        """

    def flags(self, *bases: str) -> Iterable[str] | None:
        """
        Format argument's full-format flags from the given base strings.

        :return: an :class:`Iterable` of formatted flag names or `None` if full-format flags formatting
                 isn't supported by the formatter itself or its current configuration
        """

    def flags_compact(self, *bases: str) -> Iterable[str] | None:
        """
        Format argument's compact-format flags from the given base strings.

        :return: an :class:`Iterable` of formatted flag names or `None` if compact-format flags formatting
                 isn't supported by the formatter itself or its current configuration
        """
