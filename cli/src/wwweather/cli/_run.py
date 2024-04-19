from collections.abc import Sequence

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from wwweather.data.sqlalchemy import reposmaker

from argparse import Namespace, ArgumentParser

from .commands import commands_mapper
from ._helpers import DefaultArgsFormatter
from ._arguments import setargs_db_creds, sqlalchemy_url_from_context

from . import AppContext

from . import ARGPARSE_ROOT_DESCRIPTION
from . import ARGPARSE_FROMFILE_PREFIXES, ARGPARSE_ALLOW_ABBREW


# Declare publicly visible members
__all__ = ['run_cli']


def run_cli(args: Sequence[str] = None):
    """

    """

    # Setup arguments parser

    # -- Create a new ArgumentParser
    parser = ArgumentParser(
        description=ARGPARSE_ROOT_DESCRIPTION,
        fromfile_prefix_chars=ARGPARSE_FROMFILE_PREFIXES,
        allow_abbrev=ARGPARSE_ALLOW_ABBREW
    )

    # -- Setup argument formatters

    # -- -- Setup formatter for the db credentials arguments group
    argsfmt_db_creds = DefaultArgsFormatter(
        dest_fmt="db_%(base)s",
        metavar_fmt="DB.%(base)s",
        flags_fmt="--db.%(base)s",
        flags_compact_fmt="-DB%(base)s"
    )

    # -- Setup parser arguments

    # -- -- Add general options arguments
    parser.add_argument(
        '-s', '--silent',
        dest='__silent__',
        action='store_true',
        help='Run silent - suspends any nominal outputs.'
    )

    # -- -- Add db credentials arguemnts group
    setargs_db_creds(
        parser.add_argument_group(
            title="db credentials",
            description="Operational weather records database credentials"
        ),
        args_fmt=argsfmt_db_creds
    )

    # -- -- Add subcommands
    commands_mapper.map_commands(
        parser,
        title='commands',
        dest='__command__', metavar='COMMAND',
        required=True
    )

    # Parse arguments and build-up a context object

    # -- Parse cmd arguments to the args namespace
    ns_args = parser.parse_args(args)

    # -- Create runtime globals namespace
    ns_globals = Namespace(
        command=getattr(ns_args, '__command__'),
        silent=getattr(ns_args, '__silent__')
    )

    # -- Extract SQLAlchemy URL from args and build weather records repository managers factory
    repos_factory = reposmaker(session_factory=sessionmaker(bind=create_engine(
        url=sqlalchemy_url_from_context(ns_args, argsfmt_db_creds)
    )))

    # -- Assemble context object
    context = AppContext(ns_args=ns_args, ns_globals=ns_globals, repos_factory=repos_factory)

    # Run active command handlers

    # noinspection PyUnboundLocalVariable
    commands_mapper.commands[ns_globals.command](context)
