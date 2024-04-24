from typing import Optional
from dataclasses import dataclass, field

from wwweather.data.model import AirToxics


@dataclass
class DataAirQuality:
    """
    Air quality scoring and toxics measurements data
    """

    # Air toxics concentration measurements data attributes

    toxics: Optional[AirToxics] = field(default=None)
    """
    Air toxics concentration measurements data
    """

    # Air quality indexes data attributes

    aqi_epa: Optional[int] = field(default=None)
    """
    Air Quality Index calculated by methodology of US Environmental Protection Agency (EPA)
    """

    aqi_defra: Optional[int] = field(default=None)
    """
    Air Quality Index calculated by methodology of UK Department for Environment Food & Rural Affairs (DEFRA)
    """
