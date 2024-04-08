from .. import ComparableMixin


class AtmPressure(ComparableMixin):
    """
    Atmospheric pressure value, represented in both millibars and inches of Mercury at once.
    """

    _mbar: float    # Atmospheric pressure value in millibars
    _inch: float    # Atmospheric pressure value in inches of Mercury

    def __init__(self, mbar: float = None, inch: float = None):
        """
        Initializes new :class:`AtmPressure` instance

        :param mbar: atmospheric pressure value in millibars (calculated from `inch` if not provided)
        :param inch: atmospheric pressure value in inches of Mercury (calculated from `mbar` is not provided)
        """

        super().__init__()

        self._mbar = mbar if mbar is not None else inch * 33.8639
        self._inch = inch if inch is not None else mbar / 33.8639

    @property
    def mbar(self) -> float:
        """
        Atmospheric pressure value in millibars
        """

        return self._mbar

    __comparison_value__ = mbar     # Override `__comparison_value__` as alias of the `mbar` property

    @property
    def inch(self) -> float:
        """
        Atmospheric pressure value in inches of Mercury
        """

        return self._inch

    def __repr__(self) -> str:
        return f"{type(self).__name__}(mbar={self._mbar}, inch={self._inch})"

    def __str__(self) -> str:
        return f"P({self._mbar:6.1f} mBar / {self._inch:5.2f} inHg)"
