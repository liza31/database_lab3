from dataclasses import dataclass


@dataclass(frozen=True)
class GeoPosition:
    """
    Geographical position, represented by a (latitude, longitude) coordinates
    """

    lat: float
    """
    Position latitude coordinate
    """

    lng: float
    """
    Position longitude coordinate
    """
