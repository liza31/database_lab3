from .._helpers import make_composite

from wwweather.data.model import AirTemp


# Define publicly visible members
__all__ = ['make_composite__AirTemp']


# noinspection PyPep8Naming
def make_composite__AirTemp(cls: AirTemp.__class__):
    """
    Modifies passed `cls` class, which expected to be a class of :class:`AirTemp` or one derived from it
    adding to it `__composite_generate__()` class method & `__composite_values__()` method,
    enabling support of the SQLAlchemy CompositeAPI for the modified class.
    """

    def generate(_cls: AirTemp.__class__, celsius: float = None) -> AirTemp | None:
        """
        SQLAlchemy composite factory for the target :class:`AirTemp`-like class

        :param _cls: :class:`type` of :class:`AirTemp` class or one derived from it

        :param celsius: temperature value in degrees Celsius

        :return: :class:`AirTemp` instance if not-`None` `celsius` value was provided - else `None`
        """

        return cls(celsius=celsius)

    def get_vals(_obj: AirTemp) -> tuple[float]:
        """
        SQLAlchemy composite values unpack method for the target :class:`AirTemp`-like class

        :return: :class:`tuple` of (`celsius`,)
        """

        return (_obj.celsius,)

    make_composite(cls, generate=generate, get_vals=get_vals, allow_empty=False)


# Invoke `AirTemp` class modification
make_composite__AirTemp(AirTemp)
