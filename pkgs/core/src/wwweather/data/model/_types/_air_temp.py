from .. import ComparableMixin


class AirTemp(ComparableMixin):
    """
    Air temperature value, represented in both degrees Celsius and Fahrenheit at once.
    """

    _celsius: float         # Temperature value in degrees Celsius
    _fahrenheit: float      # Temperature value in degrees  Fahrenheit

    def __init__(self, celsius: float = None, fahrenheit: float = None):
        """
        Initializes new :class:`AirTemp` instance

        :param celsius: temperature value in degrees Celsius (calculated from `fahrenheit` if not provided)
        :param fahrenheit: temperature value in degrees Fahrenheit (calculated from `celsius` is not provided)
        """

        super().__init__()

        self._celsius = celsius if celsius is not None else (fahrenheit - 32) / 1.8
        self._fahrenheit = fahrenheit if fahrenheit is not None else (celsius * 1.8) + 32

    @property
    def celsius(self) -> float:
        """
        Temperature value in degrees Celsius
        """

        return self._celsius

    __comparison_value__ = celsius  # Override `__comparison_value__` as alias of the `celsius` property

    @property
    def fahrenheit(self) -> float:
        """
        Temperature value in degrees Fahrenheit
        """

        return self._fahrenheit

    def __repr__(self) -> str:
        return f"{type(self).__name__}(celcius={self._celsius}, farenheit={self._fahrenheit})"

    def __str__(self) -> str:
        return f"T({self._celsius:4.1f}°C / {self._fahrenheit:5.1f}°F)"
