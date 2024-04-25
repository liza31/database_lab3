from collections.abc import Sequence
from enum import Enum

from argparse import Namespace

from itertools import chain

# noinspection PyUnresolvedReferences
import time
import csv

from wwweather.data.csv import CSVOpts

from .._helpers import ABCArgsFormatter


# Define publicly visible members
__all__ = ['CSVQuoting', 'setargs_csv_opts', 'csv_opts_from_context']


class CSVQuoting(int, Enum):
    """
    CSV read/write quoting options for the `csv` module readers/writers.
    Encloses corresponding '`csv.QUOTE_*`' constants
    """

    ALL = csv.QUOTE_ALL
    """
    Quote all fields on dumping, unquote on reading.
    Corresponds to the `csv.QUOTE_ALL`
    """

    MINIMAL = csv.QUOTE_MINIMAL
    """
    Quote only fields containing special characters.
    Corresponds to the `csv.QUOTE_MINIMAL`
    """

    NONUMERIC = csv.QUOTE_NONNUMERIC
    """
    Quote all non-numeric fields on writing, interpret all unquoted fields as numeric values on reading.
    Corresponds to the `csv.QUOTE_NONNUMERIC`
    """

    NONE = csv.QUOTE_NONE
    """
    Do not quote fields on writing, do not process quotes on reading.
    Corresponds to the `csv.QUOTE_NONE`
    """

    def __str__(self):

        # Return name of the option for help messages convenience
        return self.name


def char(char_str: str) -> str:
    """
    Verify given string is a single character

    :return: input string

    :raise ValueError: if validation failed
    """

    # Validate input string contains exactly one character
    if len(char_str) != 1:

        # -- Raise a ValueError if validation failed
        raise ValueError(f"Single character expected, got: {repr(char_str)}")

    # -- Return passed string otherwise
    return char_str


def literals_list(literals_str: str) -> Sequence[str]:
    """
    Parse list of comma-separated literals from the given string into a :class:`Sequence` of strings

    :return: :class:`Sequence` of separated trimmed string literals
    """

    return list(map(str.strip, literals_str.split(',')))


def setargs_csv_opts(parser, args_fmt: ABCArgsFormatter):
    """
    Add a set of records CSV load/dump options arguments corresponds to those supported by the :class:`CSSVOpts`,
    including formatting parameters mapping which is specified through the detailed standalone arguments
    corresponds to some of the `csv` module dialects and formatting parameters
    to the given `argparse` parser (can be either an :class:`ArgumentParser` instance or argument group object)
    and using the given `args_fmt` :class:`ABCArgsFormatter` instance to format arguments name-related parameters.

    **Arguments to be added**

    * `datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
      (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

    * `true_literals` - boolean `True` literals collection (all lowercase, first is taken for dumping,
      defaults to the :attr:`CSVOpts.DEFAULT_TRUE_LITERALS`)
    * `false_literals` - boolean `False` literals collection (all lowercase, first is taken for dumping,
      defaults to the :attr:`CSVOpts.DEFAULT_FALSE_LITERALS`)

    * `csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
      (defaults to the :attr:`CSVOpts.CSV_DEFAULT_DIALECT`)

    * formatting parameters set
      (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

      * `delimiter` - character used to separate fields
      * `doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
      * `escapechar` - character used to escape special characters in unquoted strings, `None` value disables escaping
      * `lineterminator` - string used to terminate produced lines on dumping
      * `quotechar` - quotes character
      * `quoting` - :class:`CSVQuoting` strings quoting option

    **NOTE:** Listed above argument keys are the same strings
    that are used as bases to format `dest` parameter values for those arguments

    :param parser: `argparse` parser (:class:`ArgumentParser` instance or argument group object) to add arguments
    :param args_fmt: :class:`ABCArgsFormatter` instance to be used for arguments name-related parameters formating
    """

    parser.add_argument(
        *args_fmt.flags_compact('dtf'), *args_fmt.flags('datetime-format'),
        dest=args_fmt.dest('datetime_format'), metavar=args_fmt.metavar("DATETIME_FORMAT"),
        default=CSVOpts.DEFAULT_DATETIME_FORMAT,
        help="Datetime formatting pattern in the time.strptime()/time.strftime() format "
             f"(defaults to {repr(CSVOpts.DEFAULT_DATETIME_FORMAT.replace('%', '%%'))})."
    )

    parser.add_argument(
        *args_fmt.flags_compact('tlt'), *args_fmt.flags('true-literals'),
        dest=args_fmt.dest('true_literals'), metavar=args_fmt.metavar("TRUE_LITERALS"),
        type=literals_list,
        default=None,
        help=f"Boolean 'True' literals (comma-separated, all lowercase, first is taken for dumping, "
             f"defaults to {repr(CSVOpts.DEFAULT_TRUE_LITERALS)})"
    )
    parser.add_argument(
        *args_fmt.flags_compact('flt'), *args_fmt.flags('false-literals'),
        dest=args_fmt.dest('false_literals'), metavar=args_fmt.metavar("FALSE_LITERALS"),
        type=literals_list,
        default=None,
        help=f"Boolean 'False' literals (comma-separated, all lowercase, first is taken for dumping, "
             f"defaults to {repr(CSVOpts.DEFAULT_FALSE_LITERALS)})"
    )

    parser.add_argument(
        *args_fmt.flags_compact('dia'), *args_fmt.flags('dialect', 'csv-dialect'),
        dest=args_fmt.dest('csv_dialect'), metavar=args_fmt.metavar("CSV_DIALECT"),
        **(
            dict(default=CSVOpts.DEFAULT_CSV_DIALECT)
            if type(CSVOpts.DEFAULT_CSV_DIALECT) is str else
            dict(required=False)
        ),
        choices=csv.list_dialects(),
        help="CSV dialect name (see Python's csv module docs for details)" +
             (f" (defaults to {repr(CSVOpts.DEFAULT_CSV_DIALECT)})."
              if type(CSVOpts.DEFAULT_CSV_DIALECT) is str else
              ".")
    )

    default_delimiter = CSVOpts.DEFAULT_FORMATTING_PARAMS.get('delimiter', ',')
    parser.add_argument(
        *args_fmt.flags_compact('del'), *args_fmt.flags('delimiter'),
        dest=args_fmt.dest('datetime_format'), metavar=args_fmt.metavar("DELIMITER"),
        type=char,
        default=default_delimiter,
        help=f"Character used to separate fields (defaults to {repr(default_delimiter)})."
    )

    default_doublequote = CSVOpts.DEFAULT_FORMATTING_PARAMS.get('doublequote', True)
    parser.add_argument(
        *args_fmt.flags_compact('ndq'), *args_fmt.flags('not-doublequote'),
        dest=args_fmt.dest('doublequote'),
        action='store_const', const=False, default=default_doublequote,
        help="Use `escapechar` to escape quotes characters instead of doubling them" +
             (" (default behaviour)." if not default_doublequote else ".")
    )

    default_escapechar = CSVOpts.DEFAULT_FORMATTING_PARAMS.get('escapechar', None)
    parser.add_argument(
        *args_fmt.flags_compact('esc'), *args_fmt.flags('escapechar'),
        dest=args_fmt.dest('escapechar'), metavar=args_fmt.metavar("ESCAPECHAR"),
        type=char,
        default=default_escapechar,
        help="Character used to escape special characters in unquoted strings, disables escaping if not set ({})"
             .format("default behaviour" if default_escapechar is None else f"defaults to {repr(default_escapechar)}")
    )

    default_lineterminator = CSVOpts.DEFAULT_FORMATTING_PARAMS.get('lineterminator', '\r\n')
    parser.add_argument(
        *args_fmt.flags_compact('lnt'), *args_fmt.flags('lineterminator'),
        dest=args_fmt.dest('lineterminator'), metavar=args_fmt.metavar("LINETERMINATOR"),
        default=default_lineterminator,
        help=f"String used to terminate produced lines on dumping (defaults to {repr(default_lineterminator)})."
    )

    default_quotechar = CSVOpts.DEFAULT_FORMATTING_PARAMS.get('quotechar', '\"')
    parser.add_argument(
        *args_fmt.flags_compact('qtc'), *args_fmt.flags('quotechar'),
        dest=args_fmt.dest('quotechar'), metavar=args_fmt.metavar("QUOTECHAR"),
        type=char,
        default=default_quotechar,
        help=f"Quotes character (defaults to {repr(default_quotechar)})."
    )

    default_quoting = CSVOpts.DEFAULT_FORMATTING_PARAMS.get('quoting', CSVQuoting.MINIMAL)
    parser.add_argument(
        *args_fmt.flags_compact('qtm'), *args_fmt.flags('quoting'),
        type=lambda name: CSVQuoting[name],
        choices=list(CSVQuoting), default=default_quoting,
        dest=args_fmt.dest('quoting'), metavar=args_fmt.metavar("QUOTING"),
        help="Strings quoting option, where the possible options are: "
             "'ALL' - quote all fields on dumping, unquote on loading; "
             "'MINIMAL' - quote only fields containing special characters; "
             "'NONNUMERIC' - quote all non-numeric fields on dumping; "
             "'NONE' - do not quote fields on dumping, do not process quotes on loading "
             f"(defaults to {repr(default_quoting.name)})."
    )


def csv_opts_from_context(context: Namespace, attrs_fmt: ABCArgsFormatter) -> CSVOpts:
    """
    Extract records CSV load/dump options as a :class:`CSVOpts` object from the given `context` namespace
    using the given `attrs_fmt` :class:`ABCArgsFormatter` instance to format target attributes names

    **Recognized context attributes**

    * `datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
      (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

    * `true_literals` - boolean `True` literals collection (all lowercase, first is taken for dumping,
      defaults to the :attr:`CSVOpts.DEFAULT_TRUE_LITERALS`)
    * `false_literals` - boolean `False` literals collection (all lowercase, first is taken for dumping,
      defaults to the :attr:`CSVOpts.DEFAULT_FALSE_LITERALS`)

    * `csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
      (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

    * formatting parameters set
      (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

      * `delimiter` - character used to separate fields
      * `doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
      * `escapechar` - character used to escape special characters in unquoted strings,
        `None` value disables escaping
      * `lineterminator` - string used to terminate produced lines on dumping
      * `quotechar` - quotes character
      * `quoting` - :class:`CSVQuoting` strings quoting option

    **NOTE:** Listed above attribute keys will be used as base strings to determine the corresponding attribute names
    within the given context through formating them via the `dest()` method
    of the given `attrs_fmt` :class:`ABCArgsFormatter` instance.

    :param context: context namespace - holds necessary data as attributes (typically a :class:`Namespace` instance)
    :param attrs_fmt: :class:`ABCArgsFormatter` instance to be used for attribute names formating

    :return: extracted :class:`RecordsSearchParams` object
    """

    # Initialize a new CSVOpts object from the context
    return CSVOpts(
        default_formatting_params=True,
        **dict(
            (key, val) for key, val in
            chain(
                [
                    ('datetime_format', getattr(context, attrs_fmt.dest('datetime_format'), None)),

                    ('true_literals', getattr(context, attrs_fmt.dest('true_literals'), None)),
                    ('false_literals', getattr(context, attrs_fmt.dest('false_literals'), None)),

                    ('csv_dialect', getattr(context, attrs_fmt.dest('csv_dialect'), None)),

                    ('quoting', getattr(
                        context,
                        attrs_fmt.dest('quoting'),
                        CSVOpts.DEFAULT_FORMATTING_PARAMS.get('quoting', Namespace(value=None))
                    ).value)
                ],
                (
                    (key, getattr(context, attrs_fmt.dest(key), CSVOpts.DEFAULT_FORMATTING_PARAMS.get(key)))
                    for key in ['delimiter', 'doublequote', 'escapechar', 'lineterminator', 'quotechar']
                )
            ) if val is not None
        )
    )
