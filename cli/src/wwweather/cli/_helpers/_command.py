from typing import Any
from collections.abc import Callable

from argparse import ArgumentParser
from .. import AppContext


class CLICommand:
    """
    Single CLI command mapping class designed to work with `argparse` :class:`ArgumentParser` subcommands API
    """

    _name: str                                              # Command name
    _kwargs: dict[str, Any]                                 # Command subparser initialization kwargs

    _handlers: list[Callable[[AppContext], Any]]            # Command handling delegates
    _argsetters: list[Callable[[ArgumentParser], None]]     # Command arguments setup delegates

    def __init__(self, name: str, **kwargs: Any):
        """
        Initializes new :class:`CLICommand` instance

        :param name: command name (will be passed to the `add_parser()` method as the `name` parameter)
        :param kwargs: command subparser initialization kwargs (will be passed to the `add_parser()` method)
        """

        # Store passed command name and other initialization kwargs
        self._name = name
        self._kwargs = kwargs

        # Initialize empty lists for delegates lists
        self._handlers = list()
        self._argsetters = list()

    @property
    def name(self) -> str:
        """
        Command name
        """

        return self._name

    def map_subparser(self, subparsers) -> ArgumentParser:
        """
        Map current command onto new :class:`ArgumentParser` within the given subparsers object
        (instance returned by `ArgumentParser.add_subparser()` method)

        :return: created and configured new subparser `ArgumentParser` instance
        """

        # Initialize new subparser for the command
        parser: ArgumentParser = subparsers.add_parser(name=self._name, **self._kwargs)

        # Invoke all registered parser setup delegates
        for argsetter in self._argsetters:
            argsetter(parser)

        # Return configured parser
        return parser

    def __call__(self, context: AppContext):
        """
        Invoke command handling within the given :class:`AppContext` context.

        **NOTE:** It is guaranteed that handlers will be called in accordance with their registration order
        """

        # Invoke all registered handler delegates
        for handler in self._handlers:
            handler(context)

    def add_argsetter(self, argsetter: Callable[[ArgumentParser], None]):
        """
        Register new arguments configuration :class:`Callable` for the :class:`ArgumentParser` instance,
        current command will be mapped on.

        To satisfy requirements, configuration callables must take configuring :class:`ArgumentParser` instance
        as the only positional argument.

        **NOTE:** May be used as a decorator method
        """

        # Store reference to the new parser setup callable
        self._argsetters.append(argsetter)

        return argsetter

    def add_handler(self, handler: Callable[[AppContext], None]):
        """
        Register new handling :class:`Callable` for the current command.

        To satisfy requirements, handling callables must take
        an :class:`AppContext` instance as the only positional argument.

        **NOTE:** May be used as a decorator method
        """

        # Store reference to the new command handling callable
        self._handlers.append(handler)

        return handler
