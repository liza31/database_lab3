from argparse import ArgumentParser

from itertools import chain, islice

from pathlib import Path

from wwweather.data.utils import ResultsPagesIterator

# noinspection PyUnresolvedReferences
from wwweather.data.csv import CSVOpts
from wwweather.data.csv import CSVRecordsDumper

from .. import AppContext
from . import commands_mapper

from .._helpers import DefaultArgsFormatter
from .._arguments import setargs_search_params, search_params_from_context
from .._arguments import setargs_csv_opts, csv_opts_from_context

# noinspection PyUnresolvedReferences
from .._arguments import CSVQuoting

from ..display import ABCWeatherRecordsFormatter, DefaultWeatherRecordsFormatter


# Define publicly visible members
__all__ = [
    'run_records_search', 'setargs_records_search',
    'SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP',
    'SEARCH_DEFAULT_EXPORT_ENCODING',
    'SEARCH_FETCH_BLOCK_SIZE',
    'SEARCH_RESULT_RECORDS_FORMATTER'
]


# Declare default values variables

SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP: int = 3
"""
Default maximum number of found records to display in group table
"""

SEARCH_DEFAULT_EXPORT_ENCODING: str = 'utf-8'
"""
Default encoding for results export CSV file
"""

SEARCH_FETCH_BLOCK_SIZE: int = 1000
"""
Maximum number of records to be fetched from database at a time
"""

SEARCH_RESULT_RECORDS_FORMATTER: ABCWeatherRecordsFormatter = DefaultWeatherRecordsFormatter()
"""
:class:`ABCWeatherRecordsFormatter` records formatter to be used for search results display
"""


# Initialize new CLICommand from global commands maper
_command = commands_mapper.new_command(
    name='search',
    help="Search in the database for weather records by the specified parameters"
)


# Create args formatters to be used for CLI arguments setup and data extraction

# -- Initialize args formatter for the records search params arguments group
_argsfmt_search_params = DefaultArgsFormatter(
    dest_fmt='search_%(base)s',
    metavar_fmt='SEARCH.%(base)s',
    flags_compact_fmt='-S%(base)s',
    flags_fmt='--search.%(base)s'
)

# -- Initialize args formatter for the results export file CSV options arguments group
_argsfmt_export_csv_opts = DefaultArgsFormatter(
    dest_fmt='export_csv_%(base)s',
    metavar_fmt='EXPORT.CSV.%(base)s',
    flags_compact_fmt='-E.CSV%(base)s',
    flags_fmt='--export.csv.%(base)s'
)


@_command.add_argsetter
def setargs_records_search(parser: ArgumentParser):
    """
    Configure CLI arguments for the 'search' command on the given `argparse` :class:`ArgumentParser` parser.

    **Arguments to be added**

    * `results_limit` - maximum number of results to fetch: if exceed last results will be truncated,
      `None` value sets to unlimited (defaults to `None`)

    * `results_display` - whether to display found results in console
      (defaults to `True`)
    * `results_display_group` - maximum number of found records to display in one group table
      (defaults to `SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP`)

    * `export_path` - results export CSV file path, `None` value disables results export
      (defaults to `None`)
    * `export_encoding` - results export CSV file encoding
      (defaults to `SEARCH_DEFAULT_EXPORT_ENCODING`)
    * 'export_append' - whether to append results export file instead of recreation if it already exists
      (defaults to `False`)

    * Records search params group:

      * `search_location_name` - target record(s) location name
      * `search_location_country` - target record(s) location country

      * `search_location_latitude` - target record(s) location position latitude
      * `search_location_longitude` - target record(s) location position longitude

      * `search_local_timezone` - target record(s) local timezone name (in accordance with IANA database)

      * `search_local_start_date` - target record(s) dates range start date in local time
      * `search_local_end_date` - target record(s) dates range end date in local time
      * `search_local_date` - target record(s) date in local time

    * Export file CSV options group:

      * `export_datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
        (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

      * `export_true_literals` - boolean `True` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_TRUE_LITERALS`)
      * `export_false_literals` - boolean `False` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_FALSE_LITERALS`)

      * `export_csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
        (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

      * formatting parameters set
        (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

        * `export_csv_delimiter` - character used to separate fields
        * `export_csv_doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
        * `export_csv_escapechar` - character used to escape special characters in unquoted strings,
          `None` value disables escaping
        * `export_csv_lineterminator` - string used to terminate produced lines on dumping
        * `export_csv_quotechar` - quotes character
        * `export_csv_quoting` - :class:`CSVQuoting` strings quoting option
    """

    # Add search options arguments
    parser.add_argument(
        '-Rlim', '--results.limit',
        dest='results_limit', metavar='RESULTS.LIMIT',
        type=int,
        default=None,
        help="Maximum number of results to fetch: if exceed last results will be truncated, unlimits if not set."
    )

    # Add results display options arguments
    parser.add_argument(
        '-Rndp', '--results.no-display',
        dest='results_display',
        action='store_false',
        help="Do not display found results in console."
    )
    parser.add_argument(
        '-Rdgs', '--results.display.group',
        dest='results_display_group', metavar='RESULTS.DISPLAY.GROUP',
        type=int,
        default=SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP,
        help=f"Maximum number of found records to display in one group table "
             f"(defaults to {SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP})."
    )

    # Add results export file params arguments
    parser.add_argument(
        '-Ep', '--export.path',
        dest='export_path', metavar='EXPORT.PATH',
        type=Path,
        default=None,
        help="Results export CSV file path, disables results export if not set."
    )
    parser.add_argument(
        '-Ee', '--dest.enc', '--dest.encoding',
        dest='export_encoding', metavar='EXPORT.ENCODING',
        default=SEARCH_DEFAULT_EXPORT_ENCODING,
        help=f"Results export CSV file encoding (defaults to {repr(SEARCH_DEFAULT_EXPORT_ENCODING)})."
    )
    parser.add_argument(
        '-Ea', '--dest.append',
        dest='export_append',
        action='store_true',
        help=f"Append destination file instead of recreation if it already exists."
    )

    # Add records search params arguments group
    setargs_search_params(
        parser.add_argument_group(
            title="records search params",
            description="Weather records search parameters"
        ),
        args_fmt=_argsfmt_search_params
    )

    # Add results export file CSV options arguments group
    setargs_csv_opts(
        parser.add_argument_group(
            title="results export file CSV options",
            description="CSV dumping options for the results export CSV file"
        ),
        args_fmt=_argsfmt_export_csv_opts
    )


@_command.add_handler
def run_records_search(context: AppContext):
    """
    Run search in the database for weather records by the specified parameters.

    **Recognized `context.ns_args` attributes**

    * `results_limit` - maximum number of results to fetch, `None` value sets to unlimited
      (defaults to `None`)

    * `results_display` - whether to display found results in console
      (defaults to `True`)
    * `results_display_group` - maximum number of found records to display in one group table
      (defaults to the `SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP`)

    * `export_path` - results export CSV file path, `None` value disables results export
      (defaults to `None`)
    * `export_encoding` - results export CSV file encoding
      (defaults to the `SEARCH_DEFAULT_EXPORT_ENCODING`)
    * 'export_append' - whether to append results export file instead of recreation if it already exists
      (defaults to `False`)

    * Records search params group (all optional):

      * `search_location_name` - target record(s) location name
      * `search_location_country` - target record(s) location country

      * `search_location_latitude` - target record(s) location position latitude
      * `search_location_longitude` - target record(s) location position longitude

      * `search_local_timezone` - target record(s) local timezone name (in accordance with IANA database)

      * `search_local_start_date` - target record(s) dates range start date in local time
      * `search_local_end_date` - target record(s) dates range end date in local time
      * `search_local_date` - target record(s) date in local time

    * Export file CSV options group:

      * `export_datetime_format` - datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
        (defaults to the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`)

      * `export_true_literals` - boolean `True` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_TRUE_LITERALS`)
      * `export_false_literals` - boolean `False` literals collection (all lowercase, first is taken for dumping,
        defaults to the :attr:`CSVOpts.DEFAULT_FALSE_LITERALS`)

      * `export_csv_dialect` - CSV dialect name (from :func:`csv.list_dialects`)
        (defaults to the :attr:`CSVOpts.DEFAULT_DIALECT`)

      * formatting parameters set
        (all defaults to values taken from the :attr:`CSVOpts.DEFAULT_FORMATTING_PARAMS`):

        * `export_csv_delimiter` - character used to separate fields
        * `export_csv_doublequote` - whether to double quoting characters instead of escaping them with `escapechar`
        * `export_csv_escapechar` - character used to escape special characters in unquoted strings,
          `None` value disables escaping
        * `export_csv_lineterminator` - string used to terminate produced lines on dumping
        * `export_csv_quotechar` - quotes character
        * `export_csv_quoting` - :class:`CSVQuoting` strings quoting option

    :param context: application context :class:`AppContext` instance
    """

    # Extract complex & frequently used data from the context

    # -- Extract records search params from the context
    search_params = search_params_from_context(context.ns_args, attrs_fmt=_argsfmt_search_params)

    # -- Extract results export options from the context
    export_path = getattr(context.ns_args, 'export_path', None)
    export_csv_opts = None if export_path is None else \
        csv_opts_from_context(context.ns_args, attrs_fmt=_argsfmt_export_csv_opts)

    # -- Extract results display options from the context
    results_display = getattr(context.ns_args, 'results_display') and not context.ns_globals.silent
    results_display_group = None if not results_display else \
        getattr(context.ns_args, 'results_display_group', SEARCH_DEFAULT_RESULTS_DISPLAY_GROUP)

    # Define found records counter
    records_found = 0

    # Connect to the weather records repository
    with context.repository() as repo:

        # Initialize paginated records search in the repository
        results_pages_iter = ResultsPagesIterator(
            repo.search_all(
                search_params,
                limit=getattr(context.ns_args, 'results_limit', None),
                page_size=SEARCH_FETCH_BLOCK_SIZE
            )
        )

        # Open records export CSV file for writing (appending if necessary) if export required
        export_file = None if export_path is None else open(
            context.ns_args.export_path,
            mode='a' if getattr(context.ns_args, 'export_append', False) else 'w',
            newline='',
            encoding=getattr(context.ns_args, 'export_encoding', SEARCH_DEFAULT_EXPORT_ENCODING)
        )

        try:

            # Initialize result records dumper for the export file (if opened)
            export_dumper = None if export_file is None else \
                CSVRecordsDumper(export_file, csv_opts=export_csv_opts, dump_header=True)

            # Initialize results display iterator with an empty tuple
            display_iter = tuple()

            # Display (if required & allowed) & dump to export file (if required) found records block by block
            for page in results_pages_iter:

                # -- Dump (if required) current block to the export CSV file
                if export_dumper is not None:
                    export_dumper.dump(page.results)

                # -- Display (if required) current block to console
                if results_display:

                    # Extend results display iterator with new block records
                    display_iter = chain(iter(list(display_iter)), iter(page.results))

                    # Run loop to display result records group by group
                    while True:

                        # -- Accumulate display group
                        display_group = list(islice(display_iter, results_display_group))

                        # -- Check if the current display group is shorter than required for exit
                        if len(display_group) < results_display_group:
                            display_iter = iter(display_group)
                            break

                        # -- Display group using SEARCH_RESULT_RECORDS_FORMATTER
                        print(SEARCH_RESULT_RECORDS_FORMATTER.format_from(display_group), end='\n\n')

                # -- Add current block size to the found records counter
                records_found += len(page.results)

            # Display (if required & allowed) last display group
            if results_display:

                # -- Acquire last display group
                display_group = list(display_iter)

                # -- If group is not empty, display it using SEARCH_RESULT_RECORDS_FORMATTER
                if len(display_group) > 0:
                    print(SEARCH_RESULT_RECORDS_FORMATTER.format_from(display_group), end='\n\n')

        except Exception as err:

            # Close export file if opened
            if export_file is not None:
                try:
                    export_file.close()
                except OSError:
                    pass

            raise err

        else:

            # Display (if allowed) found records statistics
            if not context.ns_globals.silent:
                print(f"Search complete:", records_found if records_found > 0 else "no", "records found.",
                      sep=' ', end='\n\n')
