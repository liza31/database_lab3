from collections.abc import Callable

from argparse import Namespace

from wwweather.data.storage import ABCRecordsRepositoryManager


class AppContext:
    """
    Application context.
    Holds input arguments, runtime globals and repository managers factory
    """

    _ns_args: Namespace
    _ns_globals: Namespace

    _repos_factory: Callable[[], ABCRecordsRepositoryManager]

    def __init__(self,
                 ns_args: Namespace,
                 repos_factory: Callable[[], ABCRecordsRepositoryManager],
                 ns_globals: Namespace = None):
        """
        Initializes new :class:`AppContext` instance

        :param ns_args: input arguments namespace
        :param ns_globals: runtime globals namespace (empty :class:`Namespace` instance by default)
        :param repos_factory: weather records repository managers factory (callable, takes no arguments
                              and returns :class:`ABCRecordsRepositoryManager` instance)
        """

        self._ns_args = ns_args
        self._ns_globals = ns_globals or Namespace()

        self._repos_factory = repos_factory

    @property
    def ns_args(self) -> Namespace:
        """
        Input arguments namespace
        """

        return self._ns_args

    @property
    def ns_globals(self) -> Namespace:
        """
        Runtime globals namespace
        """

        return self._ns_globals

    def repository(self) -> ABCRecordsRepositoryManager:
        """
        Returns newly initialized weather records repository manager
        """

        return self._repos_factory()
