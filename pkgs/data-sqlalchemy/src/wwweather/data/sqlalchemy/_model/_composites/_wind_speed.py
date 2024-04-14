from .._helpers import make_composite

from wwweather.data.model import WindSpeed


# Define publicly visible members
__all__ = ['make_composite__WindSpeed']


# noinspection PyPep8Naming
def make_composite__WindSpeed(cls: WindSpeed.__class__):
    """
    Modifies passed `cls` class, which expected to be a class of :class:`WindSpeed` or one derived from it
    adding to it `__composite_generate__()` class method & `__composite_values__()` method,
    enabling support of the SQLAlchemy CompositeAPI for the modified class.
    """

    def generate(_cls: WindSpeed.__class__, kmh: float = None) -> WindSpeed | None:
        """
        SQLAlchemy composite factory for the target :class:`WindSpeed`-like class

        :param _cls: :class:`type` of :class:`WindSpeed` class or one derived from it

        :param kmh: speed value in kilometers per hour

        :return: :class:`WindSpeed` instance if not-`None` `kmh` value was provided - else `None`
        """

        return cls(kmh=kmh)

    def get_vals(_obj: WindSpeed) -> tuple[float]:
        """
        SQLAlchemy composite values unpack method for the target :class:`WindSpeed`-like class

        :return: :class:`tuple` of (`kmh`,)
        """

        return (_obj.kmh,)

    make_composite(cls, generate=generate, get_vals=get_vals, allow_empty=False)


# Invoke `WindSpeed` class modification
make_composite__WindSpeed(WindSpeed)
