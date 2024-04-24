from typing import Any
from collections.abc import Iterable, Sequence, Mapping, Callable

from functools import partial
from itertools import islice

from uuid import UUID
from datetime import datetime

import csv

from wwweather.data.utils import IterResultsPage, Paginated

from wwweather.data.io import ABCRecordsLoader

from wwweather.data.model import GeoPosition, AirTemp, AtmPressure, WindSpeed, RoseDirection, AirToxics
from wwweather.data.model import DataAirQuality, WeatherRecord

from . import CSVOpts


class CSVRecordsLoader(ABCRecordsLoader):
    """
    Weather records CSV loader - implementation of :class:`ABCRecordsLoader`,
    provides functionality to read and deserialize records from CSV format
    """

    _csv_opts: CSVOpts                                              # Loading CSV options

    _feed_iter: Iterable[str]                                       # Feed rows iterable iterator

    _reader_factory: Callable[[Iterable[str]], csv.DictReader]      # Configured csv.DictReader CSV readers factory

    def __init__(self, feed: Iterable[str], csv_opts: CSVOpts = None):
        """
        Initializes new :class:`CSVRecordsLoader` instance

        :param feed: :class:`Iterable` of :class:`str` represents CSV-formatted rows

        :param csv_opts: loading CSV options as a :class:`CSVOpts` instance (defaults to new :class:`CSVOpts` object
                         instantiated with default parameters only)

        :raise RuntimeError: if the given CSV feed does not contain header row
        """

        # Handle and store loading CSV options
        self._csv_opts = csv_opts or CSVOpts()

        # Create and store CSV feed object iterator
        self._feed_iter = iter(feed)

        # Create and store csv.DictReader CSV readers factory

        # -- Read CSV feed headers sequence
        headers = next(csv.reader(
            self._feed_iter,
            dialect=self._csv_opts.csv_dialect,
            **self._csv_opts.formatting_params
        ), None)

        # -- -- Raise an error if feed is empty
        if headers is None:
            raise RuntimeError("CSV feed does not contain headers row")

        # -- Build and store readers factory callable
        self._reader_factory = partial(
            csv.DictReader,
            fieldnames=headers,
            restkey=None, restval=None,
            dialect=self._csv_opts.csv_dialect,
            **self._csv_opts.formatting_params
        )

    def _generate_record(self, data: Mapping[str, Any]) -> WeatherRecord:
        """
        Generates :class:`WeatherRecord` object from data mapping acquired from CSV feed

        :raise KeyError: if a required option is missed in the `data` mapping
        :raise ValueError: on option value parsing failure
        """

        # Collect WeatherRecord mandatory initialization kwargs

        record_mandatory_kwargs = dict(

            # Key data kwargs

            # -- Record location data kwargs

            location_country=data['country'],
            location_name=data['location_name'],
            location_position=GeoPosition(float(data['latitude']), float(data['longitude'])),

            # -- Record time data kwargs

            local_datetime=datetime.strptime(data['last_updated'], self._csv_opts.datetime_format),
            local_timezone=data['timezone']
        )

        # -- Check mandatory kwargs has no missing values
        for key, val in record_mandatory_kwargs.items():
            if val is None:
                raise KeyError(key)

        # Collect WeatherRecord.air_quality DataAirQuality initialization kwargs

        # -- Collect nested WeatherRecord.air_quality.toxics AirToxics initialization kwargs
        toxics_kwargs = {
            key: float(val) for key, val in [
                ('co', data.get('air_quality_Carbon_Monoxide')),
                ('o3', data.get('air_quality_Ozone')),
                ('no2', data.get('air_quality_Nitrogen_dioxide')),
                ('so2', data.get('air_quality_Sulphur_dioxide')),
                ('pm25', data.get('air_quality_PM2.5')),
                ('pm10', data.get('air_quality_PM10'))
            ] if val is not None
        }

        air_quality_kwargs = {
            key: val for key, val in [

                # Air toxics concentration measurements data kwargs

                ('toxics',
                 None if len(toxics_kwargs) == 0 else AirToxics(**toxics_kwargs)),

                # -- Air quality indexes data kwargs

                ('aqi_epa',
                 None if data.get('air_quality_us-epa-index') is None else int(data['air_quality_us-epa-index'])),
                ('aqi_defra',
                 None if data.get('air_quality_gb-defra-index') is None else int(data['air_quality_gb-defra-index'])),

            ] if val is not None
        }

        # Assemble and return WeatherRecord object
        return WeatherRecord(
            **record_mandatory_kwargs,
            **{key: val for key, val in [

                # Key data kwargs

                ('uuid',
                 None if data.get('uuid') is None else UUID(data['uuid'])),

                # Measurements data kwargs

                # -- Air temperature & humidity measurements data kwargs

                ('air_temp',
                 None if data.get('temperature_celsius') is None
                 else AirTemp(celsius=float(data['temperature_celsius']))),

                ('humidity',
                 None if data.get('humidity') is None else int(data['humidity'])),

                ('apparent_temp',
                 None if data.get('feels_like_celsius') is None
                 else AirTemp(celsius=float(data['feels_like_celsius']))),

                # -- Atmospheric pressure measurements data attributes

                ('atm_pressure',
                 None if data.get('pressure_mb') is None else AtmPressure(mbar=float(data['pressure_mb']))),

                # -- Wind measurements data attributes

                ('wind_speed',
                 None if data.get('wind_kph') is None else WindSpeed(kmh=float(data['wind_kph']))),
                ('wind_gust',
                 None if data.get('gust_kph') is None else WindSpeed(kmh=float(data['gust_kph']))),
                ('wind_direction',
                 None if data.get('wind_direction') is None else RoseDirection[data['wind_direction']]),

                # -- Air quality measurements data attributes

                ('air_quality',
                 None if len(air_quality_kwargs) == 0 else DataAirQuality(**air_quality_kwargs)),

                # Additional data attributes

                ('conditions_report', data.get('condition_text'))

            ] if val is not None}
        )

    def read(self, *, offset: int = 0) -> Iterable[WeatherRecord]:
        """
        Read weather records from the feed continuously.

        :param offset: number of first stored records to skip (defaults to 0)

        :return: :class:`Iterable` of :class:`WeatherRecord` instances

        :raise RuntimeError: if any error occurs during records reading
        """

        # Define lines counter
        line_number = offset

        try:

            # Create reader, read CSV feed and generate records row by row
            for row_data in self._reader_factory(islice(self._feed_iter, offset, None)):
                line_number += 1
                yield self._generate_record(row_data)

        except Exception as err:

            # -- Generate base error message
            base_err_message = f"Records reading failed: line {line_number}"

            if isinstance(err, KeyError):

                # -- Raise detailed error if a required column value is missed
                raise RuntimeError(f"{base_err_message}: column {repr(err.args[0])} value is required but missed")

            if isinstance(err, ValueError):

                # -- Raise detailed error on option value parsing failure
                raise RuntimeError(f"{base_err_message}: due to a column value parsing failure") from err

            else:

                # -- Raise detailed error if record data reading failed
                raise RuntimeError(base_err_message) from err

    def load(self,
             *,
             limit: int = None,
             offset: int = 0,
             page_size: int = None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:

        # Acquire continuous records reader from the read() method
        records_iter = self.read(offset=offset)
        records_iter = records_iter if limit is None else islice(records_iter, limit)

        # Handle continuous reader data in accordance with the loading mode and return results
        return list(records_iter) if page_size is None else IterResultsPage(records_iter, page_size=page_size)
