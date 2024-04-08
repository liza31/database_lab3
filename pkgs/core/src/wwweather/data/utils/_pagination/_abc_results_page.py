from typing import TypeVar, Generic
from abc import ABCMeta, abstractmethod


# Define type variables
_TResultsBlock = TypeVar('_TResultsBlock')


class ABCResultsPage(Generic[_TResultsBlock], metaclass=ABCMeta):
    """
    Abstraction for the page of paginated operation results.

    Holds current page number, results block and getters for neighbour pages
    """

    @property
    @abstractmethod
    def number(self) -> int:
        """
        Number of the current page
        """

    @property
    @abstractmethod
    def results(self) -> _TResultsBlock:
        """
        Current page results block
        """

    @property
    @abstractmethod
    def has_next(self) -> bool:
        """
        Indicates if there are at least one accessible results page ahead
        """

    @abstractmethod
    def get_next(self) -> 'ABCResultsPage':
        """
        Get next results page if possible

        :raise RuntimeError: if there is no pages ahead
        """

    @property
    def has_prev(self) -> bool:
        """
        Indicates if there are at least one accessible results page behind
        """

        raise NotImplementedError(f"{type(self).__name__} paginator does not support reverse page access.")

    def get_prev(self) -> 'ABCResultsPage':
        """
        Get previous results page if possible

        :raise RuntimeError: if there is no pages behind
        :raise NotImplementedError: if reverse page access is not supported
        """

        raise NotImplementedError(f"{type(self).__name__} paginator does not support reverse page access.")

    @property
    def pages_num(self) -> int:
        """
        Total number of pages

        :raise NotImplementedError: if random page access is not supported
        """

        raise NotImplementedError(f"{type(self).__name__} paginator does not support random page access.")

    def pages_get(self, number: int) -> 'ABCResultsPage':
        """
        Get results page by number

        :raise RuntimeError: if there is no page with the given number
        :raise NotImplementedError: if random page access is not supported
        """

        raise NotImplementedError(f"{type(self).__name__} paginator does not support random page access.")
