from typing import Optional
from dataclasses import dataclass, field

from uuid import UUID, uuid4
from datetime import datetime
from zoneinfo import ZoneInfo

from . import GeoPosition, AirTemp, AtmPressure, WindSpeed, RoseDirection, AirToxics


@dataclass
class WeatherRecord:
    """
    Weather record: holds measured/predicted weather conditions data
    with a context of location and time
    """

    # Key data attributes

    # -- Record location data attributes

    location_country: str
    """
    Record location country
    """

    location_name: str
    """
    Record location name
    """

    location_position: GeoPosition
    """
    Record location geo position
    """

    # -- Record time data attributes

    local_datetime: datetime
    """
    Local date & time
    (as :class:`datetime` instance without timezone info)
    """

    local_timezone: str
    """
    Local timezone name 
    (in accordance with IANA database)
    """

    def get_timezone(self) -> ZoneInfo:
        """
        Returns local timezone as :class:`ZoneInfo` instance
        """

        return ZoneInfo(self.local_timezone)

    def get_datetime(self) -> datetime:
        """
        Returns local date & time as :class:`datetime` instance
        with timezone info as :class:`ZoneInfo` instance
        """

        return self.local_datetime.replace(tzinfo=ZoneInfo(self.local_timezone))

    # -- Record unique identifier

    uuid: UUID = field(default_factory=uuid4)
    """
    Record UUID
    """

    # Measurements data attributes

    # -- Air temperature & humidity measurements data attributes

    air_temp: Optional[AirTemp] = field(default=None)
    """
    Air temperature
    """

    humidity: Optional[int] = field(default=None)
    """
    Humidity as a percentage
    """

    apparent_temp: Optional[AirTemp] = field(default=None)
    """
    Apparent temperature
    """

    # -- Atmospheric pressure measurements data attributes

    atm_pressure: Optional[AtmPressure] = field(default=None)
    """
    Atmospheric pressure
    """

    # -- Wind measurements data attributes

    wind_speed: Optional[WindSpeed] = field(default=None)
    """
    Wind speed
    """

    wind_gust: Optional[WindSpeed] = field(default=None)
    """
    Wind gust
    """

    wind_direction: Optional[RoseDirection] = field(default=None)
    """
    Wind direction
    """

    # -- Air quality measurements data attributes

    air_toxics: Optional[AirToxics] = field(default=None)
    """
    Air toxics concentration measurements data
    """

    aqi_epa: Optional[int] = field(default=None)
    """
    Air Quality Index calculated by methodology of US Environmental Protection Agency (EPA)
    """

    aqi_defra: Optional[int] = field(default=None)
    """
    Air Quality Index calculated by methodology of UK Department for Environment Food & Rural Affairs (DEFRA)
    """

    # Additional data attributes

    conditions_report: Optional[str] = field(default=None)
    """
    Weather conditions textual report
    """
