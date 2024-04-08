from typing import TypeVar
from collections.abc import Iterator

from . import ABCResultsPage


# Define type variables
_TResultsBlock = TypeVar('_TResultsBlock')


class ResultsPagesIterator(Iterator[ABCResultsPage[_TResultsBlock]]):
    """
    Results pages iterator - wraps :class:`ABCResultsPage` forward pagination mechanism
    into a native Python :class:`Iterator` interface
    """

    _current_page: ABCResultsPage[_TResultsBlock] | None    # Link to the current page (if exists)

    def __init__(self, first_page: ABCResultsPage[_TResultsBlock] | None = None):
        """
        Initialize new :class:`ResultsPagesIterator` instance

        :param first_page: :class:`ABCResultsPage` instance of the first page in pagination
                           or `None` - for empty iterator (defaults to `None`)
        """

        self._current_page = first_page

    def __next__(self):

        # Raise StopIteration if there are no pages ahead
        if self._current_page is None:
            raise StopIteration("There are no pages ahead")

        # If exists, acquire link to the next page from the previous one
        prev_page = self._current_page
        self._current_page = prev_page.get_next() if prev_page.has_next else None

        # Return link to the previous (former current) page
        return prev_page
