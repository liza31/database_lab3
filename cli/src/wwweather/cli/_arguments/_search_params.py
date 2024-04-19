from argparse import Namespace

from datetime import date

from wwweather.data.model import GeoPosition
from wwweather.data.storage import RecordsSearchParams

from .._helpers import ABCArgsFormatter


# Define publicly visible members
__all__ = ['setargs_search_params', 'search_params_from_context']


def setargs_search_params(parser, args_fmt: ABCArgsFormatter):
    """
    Add a set of records search params arguments corresponds to those supported by the :class:`RecordsSearchParams`
    to the given `argparse` parser (can be either an :class:`ArgumentParser` instance or argument group object)
    and using the given `args_fmt` :class:`ABCArgsFormatter` instance to format arguments name-related parameters.

    **Arguments to be added**

    * `location_name` - target record(s) location name
    * `location_country` - target record(s) location country

    * `location_latitude` - target record(s) location position latitude
    * `location_longitude` - target record(s) location position longitude

    * `local_timezone` - target record(s) local timezone name (in accordance with IANA database)

    * `local_start_date` - target record(s) dates range start date in local time
    * `local_end_date` - target record(s) dates range end date in local time
    * `local_date` - target record(s) date in local time

    **NOTE:** Listed above argument keys are the same strings
    that are used as bases to format `dest` parameter values for those arguments

    :param parser: `argparse` parser (:class:`ArgumentParser` instance or argument group object) to add arguments
    :param args_fmt: :class:`ABCArgsFormatter` instance to be used for arguments name-related parameters formating
    """

    parser.add_argument(
        *args_fmt.flags_compact('loc'), *args_fmt.flags('location', 'location.name'),
        dest=args_fmt.dest('location_name'), metavar=args_fmt.metavar('LOCATION.NAME'),
        required=False,
        help="Target record(s) location name."
    )
    parser.add_argument(
        *args_fmt.flags_compact('cty'), *args_fmt.flags('country', 'location.country'),
        dest=args_fmt.dest('location_country'), metavar=args_fmt.metavar('LOCATION.COUNTRY'),
        required=False,
        help="Target record(s) location country."
    )

    parser.add_argument(
        *args_fmt.flags_compact('lat'), *args_fmt.flags('latitude', 'location.position.lat'),
        dest=args_fmt.dest('location_latitude'), metavar=args_fmt.metavar('LOCATION.POSITION.LAT'),
        required=False, type=float,
        help="Target record(s) location position latitude."
    )
    parser.add_argument(
        *args_fmt.flags_compact('lng'), *args_fmt.flags('longitude', 'location.position.lng'),
        dest=args_fmt.dest('location_latitude'), metavar=args_fmt.metavar('LOCATION.POSITION.LNG'),
        required=False, type=float,
        help="Target record(s) location position longitude."
    )

    parser.add_argument(
        *args_fmt.flags_compact('tmz'), *args_fmt.flags('timezone'),
        dest=args_fmt.dest('location_country'), metavar=args_fmt.metavar('TIMEZONE'),
        required=False,
        help="Target record(s) local timezone name "
             "(in accordance with IANA database)."
    )

    parser.add_argument(
        *args_fmt.flags_compact('datf'), *args_fmt.flags('date.from'),
        dest=args_fmt.dest('local_start_date'), metavar=args_fmt.metavar('LOCAL_DATE.FROM'),
        required=False, type=date.fromisoformat,
        help="Target record(s) dates range(for a single date use 'date') end date in local time "
             "(use one of the ISO 8601 formats)."
    )
    parser.add_argument(
        *args_fmt.flags_compact('datt'), *args_fmt.flags('date.to'),
        dest=args_fmt.dest('local_end_date'), metavar=args_fmt.metavar('LOCAL_DATE.TO'),
        required=False, type=date.fromisoformat,
        help="Target record(s) dates range (for a single date use 'date') start date in local time "
             "(use one of the ISO 8601 formats)."
    )

    parser.add_argument(
        *args_fmt.flags_compact('dat'), *args_fmt.flags('date'),
        dest=args_fmt.dest('local_date'), metavar=args_fmt.metavar('LOCAL_DATE'),
        required=False, type=date.fromisoformat,
        help="Target record(s) date (for a dates range use 'date.from'/'date.to') in local time "
             "(use one of the ISO 8601 formats)."
    )


def search_params_from_context(context: Namespace, attrs_fmt: ABCArgsFormatter) -> RecordsSearchParams:
    """
    Extract records search parameters as a :class:`RecordsSearchParams` object from the given `context` namespace
    using the given `attrs_fmt` :class:`ABCArgsFormatter` instance to format target attributes names

    **Recognized context attributes**

    * `location_name` - target record(s) location name (optional)
    * `location_country` - target record(s) location country (optional)

    * `location_latitude` - target record(s) location position latitude (optional)
    * `location_longitude` - target record(s) location position longitude (optional)

    * `local_timezone` - target record(s) local timezone name (in accordance with IANA database) (optional)

    * `local_start_date` - target record(s) dates range start date in local time (optional)
    * `local_end_date` - target record(s) dates range end date in local time (optional)
    * `local_date` - target record(s) date in local time (optional)

    **NOTE:** Listed above attribute keys will be used as base strings to determine the corresponding attribute names
    within the given context through formating them via the `dest()` method
    of the given `attrs_fmt` :class:`ABCArgsFormatter` instance.

    :param context: context namespace - holds necessary data as attributes (typically a :class:`Namespace` instance)
    :param attrs_fmt: :class:`ABCArgsFormatter` instance to be used for attribute names formating

    :return: extracted :class:`RecordsSearchParams` object
    """

    #
    location_latitude = getattr(context, attrs_fmt.dest('location_latitude'), None)
    location_longitude = getattr(context, attrs_fmt.dest('location_longitude'), None)
    location_position = None if location_latitude is None or location_longitude is None else \
        GeoPosition(lat=location_latitude, lng=location_longitude)

    # Initialize a new RecordsSearchParams object from the context
    return RecordsSearchParams(
        location_name=getattr(context, attrs_fmt.dest('location_name'), None),
        location_country=getattr(context, attrs_fmt.dest('location_country'), None),
        location_position=location_position,
        local_timezone=getattr(context, attrs_fmt.dest('local_timezone'), None),
        local_start_date=getattr(context, attrs_fmt.dest('local_start_date'), None),
        local_end_date=getattr(context, attrs_fmt.dest('local_end_date'), None),
        local_date=getattr(context, attrs_fmt.dest('local_date'), None)
    )
