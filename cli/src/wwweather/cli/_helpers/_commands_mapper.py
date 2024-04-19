from typing import Any
from collections.abc import MutableMapping, Mapping
from types import MappingProxyType

from argparse import ArgumentParser

from . import CLICommand


class CLICommandsMapper:
    """
    CLI commands mapping class designed to work with `argparse` :class:`ArgumentParser` subcommands API
    """

    _commands: MutableMapping[str, CLICommand]      # Mapping of registered commands onto their names

    def __init__(self):
        """
        Initialize new :class:`CLICommandsMapper` instance
        """

        # Initialize registered commands mapping with empty dict
        self._commands = dict()

    @property
    def commands(self) -> Mapping[str, CLICommand]:
        """
        Registered commands mapping
        """

        return self._commands

    def map_subparsers(self, subparsers):
        """
        Map registered commands onto the given subparsers object
        (instance returned by `ArgumentParser.add_subparser()` method)

        :return: given subparsers object
        """

        # Map all registered commands by CLICommand.map_subparser()
        # method invocation for registered instances
        for command in self._commands.values():
            command.map_subparser(subparsers)

        return subparsers

    def map_commands(self, parser: ArgumentParser, **kwargs):
        """
        Map registered commands onto the given :class:`ArgumentParser` instance,
        creating a new subparsers object by invocation of `ArgumentParser.add_subparsers()`

        :param parser: :class:`ArgumentParser` instance to map registered commands on
        :param kwargs: subparsers initialization kwargs (will be passed to the `ArgumentParser.add_subparsers()` method)

        :return: created and configured subparsers object
        """

        # Create new subparsers object with the given parameters and call map_subparsers() method
        return self.map_subparsers(parser.add_subparsers(**kwargs))

    def add_command(self, command: CLICommand) -> CLICommand:
        """
        Register command :class:`CLICommand` instance in the current mapper

        :return: given :class:`CLICommand` instance
        """

        # Add new command to the underlying commands mapping
        self._commands[command.name] = command

        return command

    def new_command(self, name: str, **kwargs: Any) -> CLICommand:
        """
        Create a new command :class:`CLICommand` instance and register in the current mapper

        :param name: command name (will be passed to the `add_parser()` method as the `name` parameter)
        :param kwargs: command subparser initialization kwargs (will be passed to the `add_parser()` method)

        :return: created :class:`CLICommand` instance
        """

        # Initialize new CLICommand instance and call add_command() method
        return self.add_command(CLICommand(name=name, **kwargs))
