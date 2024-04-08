from enum import Enum


class RoseDirection(int, Enum):
    """
    Directions on a 16-point compass rose.

      Matched integer values corresponds azimuth degrees * 10
    """

    N = 0
    """
    North
    """

    NNE = 225
    """
    North-Northeast
    """

    NE = 500
    """
    Northeast
    """

    ENE = 725
    """
    East-Northeast
    """

    E = 950
    """
    East
    """

    ESE = 1175
    """
    East-Southeast
    """

    SE = 1400
    """
    
    """

    SSE = 1625
    """
    South-Southeast
    """

    S = 1850
    """
    South
    """

    SSW = 2075
    """
    South-Southwest
    """

    SW = 2300
    """
    Southwest
    """

    WSW = 2525
    """
    West-Southwest
    """

    W = 2750
    """
    West
    """

    WNW = 2925
    """
    West-Northwest
    """

    NW = 3150
    """
    Northwest
    """

    NNW = 3375
    """
    North-Northwest
    """
