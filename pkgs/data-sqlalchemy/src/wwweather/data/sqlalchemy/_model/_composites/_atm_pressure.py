from .._helpers import make_composite

from wwweather.data.model import AtmPressure


# Define publicly visible members
__all__ = ['make_composite__AtmPressure']


# noinspection PyPep8Naming
def make_composite__AtmPressure(cls: AtmPressure.__class__):
    """
    Modifies passed `cls` class, which expected to be a class of :class:`AtmPressure` or one derived from it
    adding to it `__composite_generate__()` class method & `__composite_values__()` method,
    enabling support of the SQLAlchemy CompositeAPI for the modified class.
    """

    def generate(_cls: AtmPressure.__class__, mbar: float = None) -> AtmPressure | None:
        """
        SQLAlchemy composite factory for the target :class:`AtmPressure`-like class

        :param _cls: :class:`type` of :class:`AtmPressure` class or one derived from it

        :param mbar: atmospheric pressure value in millibars

        :return: :class:`AtmPressure` instance if not-`None` `mbar` value was provided - else `None`
        """

        return cls(mbar=mbar)

    def get_vals(_obj: AtmPressure) -> tuple[float]:
        """
        SQLAlchemy composite values unpack method for the target :class:`AtmPressure`-like class

        :return: :class:`tuple` of (`mbar`,)
        """

        return (_obj.mbar,)

    make_composite(cls, generate=generate, get_vals=get_vals, allow_empty=False)


# Invoke `AtmPressure` class modification
make_composite__AtmPressure(AtmPressure)
