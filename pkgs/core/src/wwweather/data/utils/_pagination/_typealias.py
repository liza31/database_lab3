from typing import TypeAlias

from . import ABCResultsPage


# Define publicly visible members
__all__ = ['Paginated']


Paginated: TypeAlias = ABCResultsPage
"""
:class:`TypeAlias` for :class:`ABCResultsPage`
"""
