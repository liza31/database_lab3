from collections.abc import Callable

from sqlalchemy.orm import Session

from . import SQLAlchemyRecordsRepositoryManager


class SQLAlchemyRecordsRepositoryManagerFactory:
    """
    Simple factory class for the :class:`SQLAlchemyRecordsRepositoryManager`
    weather records repository managers.

    Stores all necessary context and allows to quickly initialize new repository managers as simple
    as just by calling the factory object as callable without any arguments.
    """

    _session_factory: Callable[[], Session] = None

    def __init__(self, session_factory: Callable[[], Session]):
        """
        Initializes new :class:`SQLAlchemyRecordsRepositoryManagerFactory` instance

        :param session_factory: SQLAlchemy :class:`sessionmaker` or other :class:`Session` factory
                                with the signature of `() -> Session`
        """

        # Store given sessions factory
        self._session_factory = session_factory

    def __call__(self):
        """
        Returns new :class:`SQLAlchemyRecordsRepositoryManager` weather records repository manager
        """

        # Initialize and return new repository manager with the stored sessions factory
        return SQLAlchemyRecordsRepositoryManager(session_factory=self._session_factory)
