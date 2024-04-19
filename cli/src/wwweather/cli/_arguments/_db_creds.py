from argparse import Namespace

from sqlalchemy import URL

from .._helpers import ABCArgsFormatter


# Define publicly visible members
__all__ = ['setargs_db_creds', 'sqlalchemy_url_from_context']


def setargs_db_creds(parser, args_fmt: ABCArgsFormatter):
    """
    Add a set of SQLAlchemy-oriented database credentials arguments
    to the given `argparse` parser (can be either an :class:`ArgumentParser` instance or argument group object)
    and using the given `args_fmt` :class:`ABCArgsFormatter` instance to format arguments name-related parameters.

    **Arguments to be added**

    * `sqlalchemy_url` - SQLAlchemy connection URL

    * `sqlalchemy_dialect` - SQLAlchemy database dialect name
    * `sqlalchemy_driver` - SQLAlchemy database driver name

    * `server_host` - dbms server host name
    * `server_port` - dbms server port number

    * `dbname` - target database name

    * `user` - target database user login
    * `pass` - target database user password

    **NOTE:** Listed above argument keys are the same strings
    that are used as bases to format `dest` parameter values for those arguments

    :param parser: `argparse` parser (:class:`ArgumentParser` instance or argument group object) to add arguments
    :param args_fmt: :class:`ABCArgsFormatter` instance to be used for arguments name-related parameters formating
    """

    parser.add_argument(
        *{*args_fmt.flags_compact('url'), *args_fmt.flags('url', 'sqlalchemy.url')},
        dest=args_fmt.dest('sqlalchemy_url'), metavar=args_fmt.metavar('SQLALCHEMY.URL'),
        required=False,
        help="SQLAlchemy database connection URL (if present - other options will be ignored)."
    )

    parser.add_argument(
        *args_fmt.flags_compact('dia'), *args_fmt.flags('dialect', 'sqlalchemy.dialect'),
        dest=args_fmt.dest('sqlalchemy_dialect'), metavar=args_fmt.metavar('SQLALCHEMY.DIALECT'),
        required=False,
        help="SQLAlchemy database dialect name."
    )
    parser.add_argument(
        *args_fmt.flags_compact('drv'), *args_fmt.flags('driver', 'sqlalchemy.driver'),
        dest=args_fmt.dest('sqlalchemy_driver'), metavar=args_fmt.metavar('SQLALCHEMY.DRIVER'),
        required=False,
        help="SQLAlchemy database driver name."
    )

    parser.add_argument(
        *args_fmt.flags_compact('h'), *args_fmt.flags('host', 'server.host'),
        dest=args_fmt.dest('server_host'), metavar=args_fmt.metavar('SERVER.HOST'),
        required=False,
        help="DBMS server host name."
    )
    parser.add_argument(
        *args_fmt.flags_compact('p'), *args_fmt.flags('port', 'server.port'),
        dest=args_fmt.dest('server_port'), metavar=args_fmt.metavar('SERVER.PORT'),
        required=False, type=int,
        help="DBMS server port number."
    )

    parser.add_argument(
        *args_fmt.flags_compact('d'), *args_fmt.flags('dbname'),
        dest=args_fmt.dest('dbname'), metavar=args_fmt.metavar('DBNAME'),
        required=False,
        help="Target database name."
    )

    parser.add_argument(
        *args_fmt.flags_compact('U'), *args_fmt.flags('user'),
        dest=args_fmt.dest('user'), metavar=args_fmt.metavar('USER'),
        required=False,
        help="Target database user login."
    )
    parser.add_argument(
        *args_fmt.flags_compact('P'), *args_fmt.flags('pass'),
        dest=args_fmt.dest('pass'), metavar=args_fmt.metavar('PASS'),
        required=False,
        help="Target database user password."
    )


def sqlalchemy_url_from_context(context: Namespace, attrs_fmt: ABCArgsFormatter) -> str:
    """
    Extract SQLAlchemy connection URL (as a string) from the given `context` namespace
    using the given `attrs_fmt` :class:`ABCArgsFormatter` instance to format target attributes names

    **Recognized context attributes**

    * `sqlalchemy_url` - SQLAlchemy connection URL (optional, if provided - other options will be ignored)

    * `sqlalchemy_dialect` - SQLAlchemy database dialect name (required, if `sqlalchemy_url` is not provided)
    * `sqlalchemy_driver` - SQLAlchemy database driver name (required, if `sqlalchemy_url` is not provided)

    * `server_host` - dbms server host name (required, if `sqlalchemy_url` is not provided)
    * `server_port` - dbms server port number (required, if `sqlalchemy_url` is not provided)

    * `dbname` - target database name (required, if `sqlalchemy_url` is not provided)

    * `user` - target database user login (required, if `sqlalchemy_url` is not provided)
    * `pass` - target database user password (required, if `sqlalchemy_url` is not provided)

    **NOTE:** Listed above attribute keys will be used as base strings to determine the corresponding attribute names
    within the given context through formating them via the `dest()` method
    of the given `attrs_fmt` :class:`ABCArgsFormatter` instance.

    :param context: context namespace - holds necessary data as attributes (typically a :class:`Namespace` instance)
    :param attrs_fmt: :class:`ABCArgsFormatter` instance to be used for attribute names formating

    :return: extracted SQLAlchemy URL string

    :raise ValueError: on any issues with inputs, acquired from the context
                       (missed credentials attributes, validation fails, etc.)
    """

    try:
        # Try to return ready SQLAlchemy URL from the context
        # or create a new one using URL.create() and credentials from the context
        return getattr(context, attrs_fmt.dest('sqlalchemy_url'), None) or URL.create(
            "{}+{}".format(getattr(context, attrs_fmt.dest('sqlalchemy_dialect')),
                           getattr(context, attrs_fmt.dest('sqlalchemy_driver'))),
            host=getattr(context, attrs_fmt.dest('server_host')),
            port=getattr(context, attrs_fmt.dest('server_port')),
            database=getattr(context, attrs_fmt.dest('dbname')),
            username=getattr(context, attrs_fmt.dest('user')),
            password=getattr(context, attrs_fmt.dest('pass'))
        ).render_as_string(hide_password=False)

    except AttributeError as err:

        # -- Raise ValueError if URL creation failed because of some credentials are missed
        raise ValueError(f"Missed '{err.name}' value is required for the SQLAlchemy connection URL")
