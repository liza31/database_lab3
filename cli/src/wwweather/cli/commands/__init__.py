# Declare package-global `CLICommandsMapper` instance for all CLI command scripts

from .._helpers import CLICommandsMapper
commands_mapper = CLICommandsMapper()
"""
Package-global :class:`CLICommandsMapper` instance to register all existing CLI commands configs & handlers in.
"""


# Import all command scripts, invoking their registration

from ._import import *
from ._export import *
from ._search import *
