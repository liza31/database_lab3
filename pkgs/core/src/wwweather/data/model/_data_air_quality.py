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

    # Additional data attributes

    acceptable: Optional[bool] = field(default=None)
    """
    Whether air quality state is acceptable for general public to perform normal outdoor activities
    """

    def __post_init__(self):

        # Compute air quality acceptability if not specified explicitly
        if self.acceptable is None:
            self.acceptable = all(filter(None, [
                self.aqi_epa <= 3 if self.aqi_epa is not None else None,
                self.aqi_defra < 7 if self.aqi_defra is not None else None
            ]))
