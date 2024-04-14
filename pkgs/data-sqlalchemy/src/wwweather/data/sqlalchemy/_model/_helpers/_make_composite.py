from typing import TypeVar
from collections.abc import Callable

from functools import update_wrapper


# Define publicly visible members
__all__ = ['make_composite']


# Define type variables
_T = TypeVar('_T')


def make_composite(cls: type[_T],
                   generate: Callable[..., _T] = None,
                   get_vals: Callable[[_T], tuple] = None,
                   *,
                   allow_empty: bool = True) -> _T:
    """
    Modifies passed `cls` class, adding to it `__composite_generate__()` class method & `__composite_values__()` method,
    enabling support of the SQLAlchemy CompositeAPI for the modified class.

    Behaviour of added methods is defined by the passed `generate` & `get_vals` callables.

        ----

    Additional options:

    * `allow_empty`

      Special flag, indicates whether to allow composite instance creation when all passed values are `None`.

      If set to `True` (default), `generate` callable will be used as it is,
      else it will be wrapped with empty-check logic:

      if all passed `args` are `None`, wrapper will return `None` value without invoking original `generate` callable

    :param cls: class to be modified for CompositeAPI support
    :param generate: callable to be used for the `__composite_generate__()` class method logic
    :param get_vals: callable to be used for the `__composite_values__()` method logic

    :param allow_empty: whether to allow `empty` instances creation by `__composite_generate__()`
    """

    if generate is not None:
        cls.__composite_generate__ = classmethod(
            generate if allow_empty else update_wrapper(
                wrapper=lambda _cls, *args: None if all(arg is None for arg in args) else generate(_cls, *args),
                wrapped=generate
            ))

    if get_vals is not None:
        cls.__composite_values__ = get_vals

    return cls
