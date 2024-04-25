from abc import ABCMeta
from typing import ClassVar
from collections.abc import Iterable
from dataclasses import dataclass, field, asdict, fields

from itertools import chain

from wwweather.data.model import WeatherRecord, AirToxics

# noinspection PyProtectedMember
from tabulate import tabulate, SEPARATING_LINE

from . import ABCWeatherRecordsFormatter


@dataclass
class _DefaultWeatherRecordsFmtOpts(metaclass=ABCMeta):
    """
    Dataclass for the :class:`DefaultWeatherRecordsFormatter` formatting parameters.

    **NOTE:** This class designed only to be a base class for the :class:`DefaultWeatherRecordsFormatter`
    and normally should never be used by itself or as a base class for other classes.
    """

    DEFAULT_SHOW_UUID: ClassVar[bool] = False
    """
    Whether to include records UUID in formatted string by default
    """

    show_uuid: bool = field(default=DEFAULT_SHOW_UUID)
    """
    Whether to include records UUID in formatted string
    """

    DEFAULT_DATE_FORMAT: ClassVar[str] = "%Y-%m-%d"
    """
    Default date format in :func:`time.strftime` format
    """

    date_format: str = field(default=DEFAULT_DATE_FORMAT)
    """
    Date format in :func:`time.strftime` format
    """

    DEFAULT_TIME_FORMAT: ClassVar[str] = "%H:%M"
    """
    Default time format in :func:`time.strftime` format
    """

    time_format: str = field(default=DEFAULT_TIME_FORMAT)
    """
    Time format in :func:`time.strftime` format
    """

    DEFAULT_TRUE_LITERAL: ClassVar[str] = "Yes"
    """
    Default boolean `True` literal
    """

    true_literal: str = field(default=DEFAULT_TRUE_LITERAL)
    """
    Boolean `True` literal
    """

    DEFAULT_FALSE_LITERAL: ClassVar[str] = "No"
    """
    Default boolean `False` literal
    """

    false_literal: str = field(default=DEFAULT_FALSE_LITERAL)
    """
    Boolean `False` literal
    """

    DEFAULT_POSITION_PATTERN: ClassVar[str] = "(%(lat)7.2f, %(lng)7.2f)"
    """
    Default formated string pattern for the location position. 
    Convention: C-style, named placeholders: 'lat', 'lng'
    """

    position_pattern: str = field(default=DEFAULT_POSITION_PATTERN)
    """
    Formated string pattern for the location position.
    Convention: C-style, named placeholders: 'lat', 'lng'
    """

    DEFAULT_HUMIDITY_PATTERN: ClassVar[str] = "%3d%%"
    """
    Default formated string pattern for the humidity percentage. 
    Convention: C-style, one positional placeholder
    """

    humidity_pattern: str = field(default=DEFAULT_HUMIDITY_PATTERN)
    """
    Formated string pattern for the humidity percentage. 
    Convention: C-style, one positional placeholder
    """

    DEFAULT_AIR_TOXIC_PATTERN: ClassVar[str] = "%9.3f μg/m^3"
    """
    Default formated string pattern for the air toxic concentration (in μg/m^3). 
    Convention: C-style, one positional placeholder
    """

    air_toxic_pattern: str = field(default=DEFAULT_AIR_TOXIC_PATTERN)
    """
    Formated string pattern for the air toxic concentration (in μg/m^3). 
    Convention: C-style, one positional placeholder
    """

    DEFAULT_AIR_TEMP_PATTERN: ClassVar[str] = "%(celsius)5.1f°C / %(fahrenheit)6.1f°F"
    """
    Default formated string pattern for the air temperature. 
    Convention: C-style, named placeholders: 'celsius', 'fahrenheit'
    """

    air_temp_pattern: str = field(default=DEFAULT_AIR_TEMP_PATTERN)
    """
    Formated string pattern for the air temperature. 
    Convention: C-style, named placeholders: 'celsius', 'fahrenheit'
    """

    DEFAULT_PRESSURE_PATTERN: ClassVar[str] = "%(mbar)5.1f mBar / %(inch)5.1f inHg"
    """
    Default formated string pattern for the atmospheric pressure. 
    Convention: C-style, named placeholders: 'mbar', 'inch'
    """

    pressure_pattern: str = field(default=DEFAULT_PRESSURE_PATTERN)
    """
    Formated string pattern for the atmospheric pressure. 
    Convention: C-style, named placeholders: 'mbar', 'inch'
    """

    DEFAULT_WIND_SPEED_PATTERN: ClassVar[str] = "%(kmh)5.1f Kmh / %(mph)5.1f Mph"
    """
    Default formated string pattern for the wind speed.
    Convention: C-style, named placeholders: 'kmh', 'mph'
    """

    wind_speed_pattern: str = field(default=DEFAULT_WIND_SPEED_PATTERN)
    """
    Formated string pattern for the wind speed.
    Convention: C-style, named placeholders: 'kmh', 'mph'
    """

    DEFAULT_TABLE_FORMATTER: ClassVar[str] = 'simple'
    """
    Default value for the table formatter name to be passed 
    to the :func:`tabulate` function as `tablefunc` parameter.
    """

    table_formatter: str = field(default=DEFAULT_TABLE_FORMATTER)
    """
    Table formatter name to be passed to the :func:`tabulate` function as `tablefunc` parameter.
    """

    DEFAULT_COLUMNS_ALIGN: ClassVar[str] = "right"
    """
    Default value for the table columns align to be passed 
    to the :func:`tabulate` function as `stralign` parameter.
    """

    columns_align: str = field(default=DEFAULT_COLUMNS_ALIGN)
    """
    Table columns align to be passed to the :func:`tabulate` function as `stralign` parameter.
    """

    DEFAULT_MISSING_VAL: ClassVar[str] = ""
    """
    Default missing (`None`) values replacement
    """

    missing_val: str = field(default=DEFAULT_MISSING_VAL)
    """
    Missing (`None`) values replacement
    """


class DefaultWeatherRecordsFormatter(ABCWeatherRecordsFormatter, _DefaultWeatherRecordsFmtOpts):
    """
    Default :class:`WeatherRecord` object groups string formatter - implements :class:`ABCWeatherRecordsFormatter`
    abstraction. Provides record groups formating in the form of vertical tables
    using C-driven 'tabulate' module for tables rendering.
    """

    _HEADERS = [

        # Key data rows headers

        "UUID",

        SEPARATING_LINE,

        # -- Record location data rows headers

        "Country",
        "Location",
        "Position",

        SEPARATING_LINE,

        # -- Record time data rows headers

        "Timezone",
        "Local date",
        "Local time",

        SEPARATING_LINE,

        # Measurements data rows headers

        # -- Air temperature & humidity measurements data rows headers

        "Air temperature",
        "Humidity",
        "Apparent temperature",

        SEPARATING_LINE,

        # -- Atmospheric pressure measurements data rows headers

        "Atmospheric pressure",

        SEPARATING_LINE,

        # -- Wind measurements data rows headers

        "Wind speed",
        "Wind gust",
        "Wind direction",

        SEPARATING_LINE,

        # -- Air quality measurements data rows headers

        *(f"Air toxics: {attr.name}" for attr in fields(AirToxics)),

        "AQI (by US EPA scale)",
        "AQI (by UK DEFRA scale)",

        "Air quality acceptable",

        SEPARATING_LINE,

        # Additional data rows headers

        "Textual report"
    ]
    """
    List of records table rows headers to be included 
    into formating results as the first (header) column
    """

    def format_from(self, records: Iterable[WeatherRecord]):

        # Call tu tabulate() to render records group table
        # noinspection PyTypeChecker
        return tabulate(
            tabular_data=list(map(list, zip(*(chain(
                (self._HEADERS if self.show_uuid else self._HEADERS[2:],),
                (
                    # Key data rows

                    ([record.uuid, SEPARATING_LINE] if self.show_uuid else []) + [

                        # -- Record location data rows

                        record.location_country,
                        record.location_name,
                        self.position_pattern % asdict(record.location_position),

                        SEPARATING_LINE,

                        # -- Record time data rows

                        record.local_timezone,
                        record.local_datetime.date().strftime(self.date_format),
                        record.local_datetime.time().strftime(self.time_format),

                        SEPARATING_LINE,

                        # Measurements data rows

                        # -- Air temperature & humidity measurements data rows

                        self.air_temp_pattern % dict(
                            celsius=record.air_temp.celsius,
                            fahrenheit=record.air_temp.fahrenheit
                        )
                        if record.air_temp is not None else None,

                        self.humidity_pattern % record.humidity
                        if record.humidity is not None else None,

                        self.air_temp_pattern % dict(
                            celsius=record.apparent_temp.celsius,
                            fahrenheit=record.apparent_temp.fahrenheit
                        )
                        if record.apparent_temp is not None else None,

                        SEPARATING_LINE,

                        # -- Atmospheric pressure measurements data rows

                        self.pressure_pattern % dict(
                            mbar=record.atm_pressure.mbar,
                            inch=record.atm_pressure.inch
                        )
                        if record.atm_pressure is not None else None,

                        SEPARATING_LINE,

                        # -- Wind measurements data rows

                        self.wind_speed_pattern % dict(
                            kmh=record.wind_speed.kmh,
                            mph=record.wind_speed.mph
                        )
                        if record.wind_speed is not None else None,

                        self.wind_speed_pattern % dict(
                            kmh=record.wind_gust.kmh,
                            mph=record.wind_gust.mph
                        )
                        if record.wind_gust is not None else None,

                        record.wind_direction.name
                        if record.wind_direction is not None else None,

                        SEPARATING_LINE,

                        # -- Air quality measurements data rows

                        *(chain(
                            (self.air_toxic_pattern % val
                             for val in asdict(record.air_quality.toxics).values()
                             if val is not None)
                            if record.air_quality.toxics is not None else tuple(),
                            (
                                record.air_quality.aqi_epa,
                                record.air_quality.aqi_defra,

                                None if record.air_quality.acceptable is None else
                                self.true_literal if record.air_quality.acceptable else self.false_literal
                            )
                        ) if record.air_quality is not None else tuple()),

                        SEPARATING_LINE,

                        # Additional data rows

                        record.conditions_report

                    ] for record in records
                )
            ))))),
            tablefmt=self.table_formatter,
            stralign=self.columns_align,
            missingval=self.missing_val,
            disable_numparse=True,
        )
