from .. import ComparableMixin


class WindSpeed(ComparableMixin):
    """
    Wind speed value, represented in both kilometers per hour (kmh / kph) and miles per hour (mph) at once.
    """

    _mph: float     # Speed value in mph
    _kmh: float     # Speed value in kmh

    def __init__(self, kmh: float = None, mph: float = None):
        """
        Initializes new :class:`WindSpeed` instance

        :param kmh: speed value in kilometers per hour (calculated from `mph` if not provided)
        :param mph: speed value in miles per hour (calculated from `kmh` if not provided)
        """

        super().__init__()

        self._kmh = kmh if kmh is not None else mph * 1.609344
        self._mph = mph if mph is not None else kmh * 0.621371

    @property
    def kmh(self) -> float:
        """
        Speed value in kilometers per hour
        """

        return self._kmh

    kph = kmh                       # Define `kph` as alias for the `kmh` property

    @property
    def mph(self) -> float:
        """
        Speed value in miles per hour
        """

        return self._mph

    __comparison_value__ = kmh      # Override `__comparison_value__` as alias of the `kmh` property

    def __repr__(self) -> str:
        return f"{type(self).__name__}(kmh={self._kmh}, mph={self._mph})"

    def __str__(self) -> str:
        return f"v({self._kmh:5.1f} Kmh / {self._mph:5.1f} Mph)"
