from typing import TypeVar
from collections.abc import Iterable, Sequence

from itertools import islice, chain

from . import ABCResultsPage


_TResultsElement = TypeVar('_TResultsElement')


class IterResultsPage(ABCResultsPage[Sequence[_TResultsElement]]):
    """
    :class:`Iterable`-based :class:`ABCResultsPage` implementation.

    Supports only forward pagination over the iterable of result elements, converting it into a
    sequence of fixed-size result elements :class:`Sequence` objects - one per page
    """

    _page_size: int                                     # Page size

    _current_number: int                                # Current page number
    _current_results: Sequence[_TResultsElement]        # Current page results block

    _results_iter: Iterable[_TResultsElement] | None    # Results iterator for next page instantiation
    _next: ABCResultsPage[_TResultsElement] | None      # Link to the next page (if already instantiated)

    def __init__(self, results: Iterable[_TResultsElement], /, *, page_size: int, number: int = 0):
        """
        Initializes new :class:`IterResultsPage` instance

        :param results: results :class:`Iterable`

        :param page_size: page size
        :param number: first page number (defaults to 0)
        """

        # Store page_size
        self._page_size = page_size

        # Create results iterable iterator
        results_iter = iter(results)

        # Bind current page results block, store it and current page number
        self._current_results = list(islice(results_iter, page_size))
        self._current_number = number

        # Check if results iterator already exhausted
        try:
            next_results_0 = next(results_iter)

        except StopIteration:
            # Iterator already exhausted - throw it away
            self._results_iter = None

        else:
            # Iterator has more elements - save it for next page instantiation
            self._results_iter = chain((next_results_0,), results_iter)

        # Plug link to the next with None before it will be instantiated
        self._next = None

    @property
    def page_size(self):
        """
        Page results block size
        """

        return self._page_size

    @property
    def number(self) -> int:
        return self._current_number

    @property
    def results(self) -> Sequence[_TResultsElement]:
        return self._current_results

    @property
    def has_next(self) -> bool:
        return self._results_iter is not None or self._next is not None

    def get_next(self) -> ABCResultsPage[Sequence[_TResultsElement]]:

        # Return link to the next page if it already instantiated
        if self._next is not None:
            return self._next

        # Instantiate next page if possible
        if self._results_iter is not None:

            # Instantiate next page
            self._next = IterResultsPage(
                self._results_iter,
                page_size=self._page_size,
                number=self._current_number + 1
            )

            # Burn link to the results iterable iterator
            self._results_iter = None

            # Return link to the next page
            return self._next

        # Raise RuntimeError if there are no pages ahead
        raise RuntimeError('There are no pages ahead')
