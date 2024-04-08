from typing import Optional
from dataclasses import dataclass, field

from datetime import date

from wwweather.data.model import GeoPosition


@dataclass
class RecordsSearchParams:
    """
    Dataclass for the weather records search parameters
    """

    location_name: Optional[str] = field(default=None)
    """
    Target record(s) location name
    """

    location_country: Optional[str] = field(default=None)
    """
    Target record(s) location country
    """

    location_position: Optional[GeoPosition] = field(default=None)
    """
    Target record(s) location geo position
    """

    local_timezone: Optional[str] = field(default=None)
    """
    Target record(s) local timezone name
    (in accordance with IANA database)
    """

    local_start_date: Optional[date] = field(default=None)
    """
    Target record(s) dates range start date in local time
    (alternatively `local_date` can be used to search for only date)
    """

    local_end_date: Optional[date] = field(default=None)
    """
    Target record(s) dates range end date in local time
    (alternatively `local_date` can be used to search for only date)
    """

    local_date: Optional[date] = field(default=None)
    """
    Target record(s) date in local time
    (alternatively `local_start_date` & `local_end_date` can be used to search for dates range)
    """
