from typing import Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class AirToxics:
    """
    Air toxics concentration measurements data
    """

    co: Optional[float] = field(default=None)
    """
    Average Carbon Monoxide (CO) μg/m3 concentration
    """

    o3: Optional[float] = field(default=None)
    """
    Average Ozone (O3) μg/m^3 concentration
    """

    no2: Optional[float] = field(default=None)
    """
    Average Nitrogen Dioxide (NO2) μg/m^3 concentration
    """

    so2: Optional[float] = field(default=None)
    """
    Average Sulphur Dioxide (SO2) μg/m^3 concentration
    """

    pm25: Optional[float] = field(default=None)
    """
    Average PM2.5 particles (<= 2.5 μm) μg/m^3 concentration
    """

    pm10: Optional[float] = field(default=None)
    """
    Average PM10 particles (<= 10 μm) μg/m^3 concentration
    """
