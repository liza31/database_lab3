from typing import Any, ClassVar
from collections.abc import Iterable, Sequence, Mapping

import csv

from wwweather.data.io import ABCRecordsDumper

from wwweather.data.model import WeatherRecord

from . import CSVOpts


class CSVRecordsDumper(ABCRecordsDumper):
    """
    Weather records CSV dumper - implementation of :class:`ABCRecordsDumper`,
    provides functionality to serialize and write records in CSV format
    """

    _CSV_DUMP_COLUMNS: ClassVar[Sequence[str]] = [

        # Key data columns

        'uuid',

        # -- Record location columns

        'country',
        'location_name',

        'latitude',
        'longitude',

        # -- Record time columns

        'last_updated',
        'timezone',

        # Measurements data columns

        # -- Air temperature & humidity measurements data columns

        'temperature_celsius',

        'humidity',

        'feels_like_celsius',

        # -- Atmospheric pressure data columns

        'pressure_mb',

        # -- Wind speed measurements data columns

        'wind_kph',
        'gust_kph',
        'wind_direction',

        # -- Air quality data columns

        'air_quality_Carbon_Monoxide',
        'air_quality_Ozone',
        'air_quality_Nitrogen_dioxide',
        'air_quality_Sulphur_dioxide',
        'air_quality_PM2.5',
        'air_quality_PM10',

        'air_quality_us-epa-index',
        'air_quality_gb-defra-index',

        # Additional data columns

        'condition_text'
    ]
    """
    Dumping CSV column names sequence
    """

    _csv_ops: CSVOpts               # Dumping CSV options

    _dest_writer: csv.DictWriter    # Configured csv.DictWriter CSV writer

    def __init__(self, dest, csv_opts: CSVOpts = None, dump_header: bool = True):
        """
        Initializes new :class:`CSVRecordsDumper` instance

        :param dest: any object, supports `write(str)` method to write CSV data

        :param csv_opts: dumping CSV options as a :class:`CSVOpts` instance (defaults to new :class:`CSVOpts` object
                         instantiated with default parameters only)
        :param dump_header: instantly dump header to the destination
        """

        # Handle and store loading CSV options
        self._csv_opts = csv_opts or CSVOpts()

        # Create and store csv.DictWriter CSV writer
        self._dest_writer = csv.DictWriter(
            dest, fieldnames=self._CSV_DUMP_COLUMNS,
            restval=None, extrasaction='ignore',
            dialect=self._csv_opts.csv_dialect,
            **self._csv_opts.formatting_params
        )

        # Instantly dump header if needed
        if dump_header:
            self.dump_header()

    def _record_values(self, record: WeatherRecord) -> Mapping[str, Any]:
        """
        Unpacks :class:`WeatherRecord` object into the column-value mapping
        for further dumping to the CSV destination
        """

        # Unpack record individual attributes
        data = {

            # Key data columns

            'uuid': record.uuid,

            # -- Record location columns

            'country': record.location_country,
            'location_name': record.location_name,

            'latitude': record.location_position.lat,
            'longitude': record.location_position.lng,

            # -- Record time columns

            'last_updated': record.local_datetime.strftime(self._csv_opts.datetime_format),
            'timezone': record.local_timezone,

            # Measurements data columns

            # -- Air temperature & humidity measurements data columns

            'temperature_celsius': record.air_temp.celsius if record.air_temp is not None else None,

            'humidity': record.humidity,

            'feels_like_celsius': record.apparent_temp.celsius if record.apparent_temp is not None else None,

            # -- Atmospheric pressure measurements data columns

            'pressure_mb': record.atm_pressure.mbar if record.atm_pressure is not None else None,

            # -- Wind speed measurements data columns

            'wind_kph': record.wind_speed.kph if record.wind_speed is not None else None,
            'gust_kph': record.wind_gust.kph if record.wind_gust is not None else None,
            'wind_direction': record.wind_direction.name if record.wind_direction is not None else None,

            # -- Air quality data columns

            'air_quality_us-epa-index': record.aqi_epa,
            'air_quality_gb-defra-index': record.aqi_defra,

            # Additional data columns

            'condition_text': record.conditions_report
        }

        # Unpack record.air_toxics attribute
        if record.air_toxics is not None:

            air_toxics = record.air_toxics

            data.update([
                ('air_quality_Carbon_Monoxide', air_toxics.co),
                ('air_quality_Ozone', air_toxics.o3),
                ('air_quality_Nitrogen_dioxide', air_toxics.no2),
                ('air_quality_Sulphur_dioxide', air_toxics.so2),
                ('air_quality_PM2.5', air_toxics.pm25),
                ('air_quality_PM10', air_toxics.pm10),
            ])

        # Return unpacked data
        return data

    def dump_header(self):
        """
        Dumps CSV column headers to the destination

        :raise RuntimeError: if any error occurs during records dumping
        """

        try:
            # Write header row to the destination
            self._dest_writer.writeheader()

        except OSError as err:

            # -- Raise detailed error if header row dumping failed
            raise RuntimeError("Header dumping failed") from err

    def dump(self, records: Iterable[WeatherRecord]):

        try:

            # Write records to the destination one by one
            self._dest_writer.writerows(self._record_values(record) for record in records)

        except OSError as err:

            # -- Raise detailed error if records dumping failed
            raise RuntimeError("Records dumping failed") from err
