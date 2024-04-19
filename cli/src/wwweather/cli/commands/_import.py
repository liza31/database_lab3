from argparse import ArgumentParser

from pathlib import Path
from typing import Literal

from wwweather.data.utils import ResultsPagesIterator

# noinspection PyUnresolvedReferences
from wwweather.data.csv import CSVOpts
from wwweather.data.csv import CSVRecordsLoader

from .. import AppContext
from . import commands_mapper

from .._helpers import DefaultArgsFormatter
from .._arguments import setargs_csv_opts, csv_opts_from_context

# noinspection PyUnresolvedReferences
from .._arguments import CSVQuoting


# Define publicly visible members
__all__ = [
    'run_records_import', 'setargs_records_import',
    'IMPORT_DEFAULT_FEED_ENCODING',
    'IMPORT_DEFAULT_BLOCK_SIZE'
]


# Declare default values variables

IMPORT_DEFAULT_FEED_ENCODING: str = 'utf-8'
"""
Default encoding for loading from feed CSV files
"""

IMPORT_DEFAULT_BLOCK_SIZE: int = 1000
"""
Default maximum number of records to be imported in one commit
"""

IMPORT_DEFAULT_ON_DUPLICATE: Literal['raise', 'ignore'] = 'ignore'
"""
Default records duplication handling option
"""


# Initialize new CLICommand from global commands maper
_command = commands_mapper.new_command(
    name='import',
    help="Import weather records into the database from a CSV file feed"
)


# Create args formatters to be used for CLI arguments setup and data extraction

# -- Initialize args formatter for the feed file CSV options arguments group
_argsfmt_feed_csv_opts = DefaultArgsFormatter(
    dest_fmt='feed_csv_%(base)s',
    metavar_fmt='FEED.CSV.%(base)s',
    flags_compact_fmt='-F.CSV%(base)s',
    flags_fmt='--feed.csv.%(base)s'
)


@_command.add_argsetter
def setargs_records_import(parser: ArgumentParser):
    """
    Configure CLI arguments for the 'import' command on the given `argparse` :class:`ArgumentParser` parser.

    **Arguments to be added**

    * `feed_path` - feed CSV file path
    * `feed_encoding` - feed CSV file encoding
      (defaults to the `IMPORT_DEFAULT_FEED_ENCODING`)

    * `import_block_size - maximum number of records to be imported in one commit
      (defaults to the `IMPORT_DEFAULT_BLOCK_SIZE`)
    * `import_on_duplicate` - records duplication handling option, may be:
      '`raise`' - to raise an error on records duplication or
      '`ignore`' - skip duplicate record without an error
      (defaults to the `IMPORT_DEFAULT_ON_DUPLICATE`)

    * Feed file CSV options group:

      * `feed_datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
      (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

      * `feed_csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
        (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

      * formatting parameters set
        (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

        * `feed_csv_delimiter` - character used to separate fields
        * `feed_csv_doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
        * `feed_csv_escapechar` - character used to escape special characters in unquoted strings,
          `None` value disables escaping
        * `feed_csv_lineterminator` - string used to terminate produced lines on dumping
        * `feed_csv_quotechar` - quotes character
        * `feed_csv_quoting` - :class:`CSVQuoting` strings quoting option
    """

    # Add feed file params arguments
    parser.add_argument(
        'feed_path',
        metavar='FEED.PATH',
        type=Path,
        help="Feed CSV file path."
    )
    parser.add_argument(
        '-Fe', '--feed.enc', '--feed.encoding',
        dest='feed_encoding', metavar='FEED.ENCODING',
        default=IMPORT_DEFAULT_FEED_ENCODING,
        help=f"Feed CSV file encoding (defaults to {repr(IMPORT_DEFAULT_FEED_ENCODING)})."
    )

    # Add import settings arguments
    parser.add_argument(
        '-Ib', '--import.block', '--import.block-size',
        dest='import_block_size', metavar='IMPORT.BLOCK_SIZE',
        type=int,
        default=IMPORT_DEFAULT_BLOCK_SIZE,
        help=f"Maximum number of records to be imported in one commit (defaults to {IMPORT_DEFAULT_BLOCK_SIZE})."
    )
    parser.add_argument(
        '-Id', '--import.duplicates', '--import.on-duplicate',
        dest='import_on_duplicate', metavar='IMPORT.ON_DUPLICATE',
        type=str,
        choices=["raise", "ignore"], default=IMPORT_DEFAULT_ON_DUPLICATE,
        help=f"Records duplication handling option, may be: "
             f"'raise' - to raise an error on records duplication or "
             f"'ignore' - skip duplicate record without an error "
             f"(defaults to {repr(IMPORT_DEFAULT_ON_DUPLICATE)})."
    )

    # Add feed file CSV options arguments group
    setargs_csv_opts(
        parser.add_argument_group(
            title="feed file CSV options",
            description="CSV loading options for the feed CSV file"
        ),
        args_fmt=_argsfmt_feed_csv_opts
    )


@_command.add_handler
def run_records_import(context: AppContext):
    """
    Run weather records import into the database from a CSV file feed.

    **Recognized `context.ns_args` attributes**

    * `feed_path` - feed CSV file path
    * `feed_encoding` - feed CSV file encoding
      (defaults to the `IMPORT_DEFAULT_FEED_ENCODING`)

    * `import_block_size - maximum number of records to be imported in one commit
      (defaults to the `IMPORT_DEFAULT_BLOCK_SIZE`)
    * `import_on_duplicate` - records duplication handling option, may be:
      '`raise`' - to raise an error on records duplication or
      '`ignore`' - skip duplicate record without an error
      (defaults to the `IMPORT_DEFAULT_ON_DUPLICATE`)

    * Feed file CSV options group:

      * `feed_csv_datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
        (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

      * `feed_csv_csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
        (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

      * formatting parameters set
        (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

        * `feed_csv_delimiter` - character used to separate fields
        * `feed_csv_doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
        * `feed_csv_escapechar` - character used to escape special characters in unquoted strings,
          `None` value disables escaping
        * `feed_csv_lineterminator` - string used to terminate produced lines on dumping
        * `feed_csv_quotechar` - quotes character
        * `feed_csv_quoting` - :class:`CSVQuoting` strings quoting option

    :param context: application context :class:`AppContext` instance
    """

    # Extract complex & frequently used data from the context

    # -- Extract feed file CSV options from the context
    feed_csv_opts = csv_opts_from_context(context.ns_args, attrs_fmt=_argsfmt_feed_csv_opts)

    # -- Extract records duplication handling mode from the context
    import_on_duplicate = getattr(context.ns_args, 'import_on_duplicate', IMPORT_DEFAULT_ON_DUPLICATE)

    # Define total and successfully imported records counters
    records_total = 0
    records_imported = 0

    # Open feed CSV file for reading
    with open(context.ns_args.feed_path,
              mode='r',
              newline='',
              encoding=getattr(context.ns_args, 'feed_encoding', IMPORT_DEFAULT_FEED_ENCODING)) as feed:

        # Connect to the weather records repository
        with context.repository() as repo:

            # Initialize records paginated loading from the given feed
            load_pages_iter = ResultsPagesIterator(
                CSVRecordsLoader(feed, csv_opts=feed_csv_opts)
                .load(page_size=getattr(context.ns_args, 'import_block_size', IMPORT_DEFAULT_BLOCK_SIZE))
            )

            # Load & import all records block by block
            for page in load_pages_iter:
                records_total += len(page.results)
                records_imported += repo.import_all(page.results, on_duplicate=import_on_duplicate)

    # Display (if allowed) imported records statistics
    if not context.ns_globals.silent:
        print(f"Import complete: {records_imported} of {records_total} records imported.", end='\n\n')
