from typing import Any
from abc import ABCMeta, abstractmethod


class ComparableMixin(metaclass=ABCMeta):
    """
    Mix-in class, implements comparison & hashing operations,
    based onto single value provided by `__comparison_value__` abstract property.
    """

    @property
    @abstractmethod
    def __comparison_value__(self):
        """
        Value used for all comparison operations and hashing
        """

    def __hash__(self) -> int:
        return hash(self.__comparison_value__)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.__comparison_value__ == other.__comparison_value__

    def __ne__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.__comparison_value__ != other.__comparison_value__

    def __lt__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.__comparison_value__ < other.__comparison_value__

    def __le__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.__comparison_value__ <= other.__comparison_value__

    def __gt__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.__comparison_value__ > other.__comparison_value__

    def __ge__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and self.__comparison_value__ >= other.__comparison_value__
