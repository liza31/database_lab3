from argparse import ArgumentParser

from pathlib import Path

from wwweather.data.utils import ResultsPagesIterator

# noinspection PyUnresolvedReferences
from wwweather.data.csv import CSVOpts
from wwweather.data.csv import CSVRecordsDumper

from .. import AppContext
from . import commands_mapper

from .._helpers import DefaultArgsFormatter
from .._arguments import setargs_csv_opts, csv_opts_from_context

# noinspection PyUnresolvedReferences
from .._arguments import CSVQuoting


# Define publicly visible members
__all__ = [
    'run_records_export', 'setargs_records_export',
    'EXPORT_DEFAULT_DEST_ENCODING'
]


# Declare default values variables

EXPORT_DEFAULT_DEST_ENCODING: str = 'utf-8'
"""
Default encoding for destination CSV file
"""

EXPORT_FETCH_BLOCK_SIZE: int = 1000
"""
Maximum number of records to be fetched from database at a time
"""


# Initialize new CLICommand from global commands maper
_command = commands_mapper.new_command(
    name='export',
    help="Export weather records from the database into a CSV file"
)


# Create args formatters to be used for CLI arguments setup and data extraction

# -- Initialize args formatter for the destination file CSV options arguments group
_argsfmt_dest_csv_opts = DefaultArgsFormatter(
    dest_fmt='dest_csv_%(base)s',
    metavar_fmt='DEST.CSV.%(base)s',
    flags_compact_fmt='-D.CSV%(base)s',
    flags_fmt='--dest.csv.%(base)s'
)


@_command.add_argsetter
def setargs_records_export(parser: ArgumentParser):
    """
    Configure CLI arguments for the 'export' command on the given `argparse` :class:`ArgumentParser` parser.

    **Arguments to be added**

    * `dest_path` - destination CSV file path
    * `dest_encoding` - destination CSV file encoding
      (defaults to the `EXPORT_DEFAULT_DEST_ENCODING`)
    * 'dest_append' - whether to append destination file instead of recreation if it already exists
      (defaults to `False`)

    * Destination file CSV options group:

      * `dest_datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
        (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

      * `dest_true_literals` - boolean `True` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_TRUE_LITERALS`)
      * `dest_false_literals` - boolean `False` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_FALSE_LITERALS`)

      * `dest_csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
        (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

      * formatting parameters arguments set
        (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

        * `dest_csv_delimiter` - character used to separate fields
        * `dest_csv_doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
        * `dest_csv_escapechar` - character used to escape special characters in unquoted strings,
          `None` value disables escaping
        * `dest_csv_lineterminator` - string used to terminate produced lines on dumping
        * `dest_csv_quotechar` - quotes character
        * `dest_csv_quoting` - :class:`CSVQuoting` strings quoting option
    """

    # Add destination file params arguments
    parser.add_argument(
        'dest_path',
        metavar='DEST.PATH',
        type=Path,
        help="Destination CSV file path."
    )
    parser.add_argument(
        '-De', '--dest.enc', '--dest.encoding',
        dest='dest_encoding', metavar='DEST.ENCODING',
        default=EXPORT_DEFAULT_DEST_ENCODING,
        help=f"Destination CSV file encoding (defaults to {repr(EXPORT_DEFAULT_DEST_ENCODING)})."
    )
    parser.add_argument(
        '-Da', '--dest.append',
        dest='dest_append',
        action='store_true',
        help=f"Append destination file instead of recreation if it already exists."
    )

    # Add destination file CSV options arguments group
    setargs_csv_opts(
        parser.add_argument_group(
            title="destination file CSV options",
            description="CSV dumping options for the destination CSV file"
        ),
        args_fmt=_argsfmt_dest_csv_opts
    )


@_command.add_handler
def run_records_export(context: AppContext):
    """
    Run records export from the database into a CSV file.

    **Recognized `context.ns_args` attributes**

    * `dest_path` - destination CSV file path
    * `dest_encoding` - destination CSV file encoding
      (defaults to the `EXPORT_DEFAULT_DEST_ENCODING`)
    * 'dest_append' - whether to append destination file instead of recreation if it already exists
      (defaults to `False`)

    * Destination file CSV options group:

      * `dest_datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
        (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

      * `dest_csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
        (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

      * `dest_true_literals` - boolean `True` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_TRUE_LITERALS`)
      * `dest_false_literals` - boolean `False` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_FALSE_LITERALS`)

      * formatting parameters arguments set
        (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

        * `dest_csv_delimiter` - character used to separate fields
        * `dest_csv_doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
        * `dest_csv_escapechar` - character used to escape special characters in unquoted strings,
          `None` value disables escaping
        * `dest_csv_lineterminator` - string used to terminate produced lines on dumping
        * `dest_csv_quotechar` - quotes character
        * `dest_csv_quoting` - :class:`CSVQuoting` strings quoting option

    :param context: application context :class:`AppContext` instance
    """

    # Extract complex & frequently used data from the context

    # -- Extract destination file CSV options from the context
    dest_csv_opts = csv_opts_from_context(context.ns_args, attrs_fmt=_argsfmt_dest_csv_opts)

    # Define exported records counter
    records_exported = 0

    # Open destination CSV file for writing (appending if necessary)
    with open(context.ns_args.dest_path,
              mode='a' if getattr(context.ns_args, 'dest_append', False) else 'w',
              newline='',
              encoding=getattr(context.ns_args, 'dest_encoding', EXPORT_DEFAULT_DEST_ENCODING)) as dest:

        # Connect to the weather records repository
        with context.repository() as repo:

            # Initialize records dumper for the given destination
            dumper = CSVRecordsDumper(dest, csv_opts=dest_csv_opts, dump_header=True)

            # Initialize paginated records export from the repository
            export_pages_iter = ResultsPagesIterator(repo.export_all(page_size=EXPORT_FETCH_BLOCK_SIZE))

            # Export & dump all records block by block
            for page in export_pages_iter:
                dumper.dump(page.results)
                records_exported += len(page.results)

    # Display (if allowed) exported records statistics
    if not context.ns_globals.silent:
        print(f"Export complete: {records_exported} records exported.", end='\n\n')
