from typing import ContextManager
from abc import ABCMeta, abstractmethod


class ReleasableResourceMixin(ContextManager, metaclass=ABCMeta):
    """
    Mix-in class for releasable resources.
    Defines special `release()` method for resource releasing and provides
    :class:`ContextManager` interface support based on it.
    """

    @abstractmethod
    def release(self):
        """
        Release releasable resource after performing operations.

        **NOTE:** Must be called after all operations with resource are performed for proper resource releasing.

        **INFO:** Alternatively will be called automatically when using class in the `with` statement.

        :return: `self`
        """

    def __exit__(self, __exc_type, __exc_value, __traceback):
        try:
            self.release()

        except:

            return False
