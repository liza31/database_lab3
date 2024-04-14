from collections.abc import Callable

from sqlalchemy.orm import registry


class ModelsMapper:
    """
    Service class, responsible for registering all individual model objects mapping callables
    and providing a single endpoint for their invocation for any SQLAlchemy :class:`register`.

      ----

    Model object mapping callable to be compatible with :class:`ModelsMapper` must take
    :class:`registry` object as the only positional argument,
    using it to map one dedicated model object during invocation.
    """

    _mappers: list[Callable[[registry], None]]    # Registered mapping callables list

    def __init__(self):
        """
        Initializes new :class:`ModelsMapper` instance.
        """

        self._mappers = list()

    def register_mapper(self, mapper: Callable[[registry], None]) -> Callable[[registry], None]:
        """
        Registers new mapping callable, can be used as a decorator.

        See :class:`ModelsMapper` docstring for details about mapping callables

        :return: passed callable object
        """

        self._mappers.append(mapper)

        return mapper

    def map_registered(self, reg: registry) -> registry:
        """
        Invokes all registered mapping callables with the passed :class:`registry` object.

        :return: passed :class:`registry` instance
        """

        for mapper in self._mappers:
            mapper(reg)

        return reg
