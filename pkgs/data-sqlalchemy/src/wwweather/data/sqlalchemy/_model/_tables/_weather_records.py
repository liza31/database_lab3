from uuid import uuid4

from sqlalchemy import Table, Column, UniqueConstraint, Index
from sqlalchemy import SmallInteger, Float, Uuid, String, Enum, DateTime

from sqlalchemy.orm import registry
from sqlalchemy.orm import composite

from wwweather.data.model import GeoPosition, AirTemp, AtmPressure, WindSpeed, RoseDirection, AirToxics
from wwweather.data.model import WeatherRecord

from . import model_mapper


# noinspection PyPep8Naming
@model_mapper.register_mapper
def map__WeatherRecord(reg: registry):
    """
    Maps :class:`WeatherRecord` model class onto database `weather_records` table
    using passed :class:`registry` instance.
    """

    # noinspection PyUnresolvedReferences
    reg.map_imperatively(

        WeatherRecord,

        local_table=Table(

            # Table name & metadata

            "weather_records",

            reg.metadata,


            # Table columns

            # -- Key data columns
            
            Column('uuid', Uuid, primary_key=True, default=uuid4),

            # -- -- Record location columns

            Column('location_country', String(128), nullable=False),
            Column('location_name', String(128), nullable=False),

            Column('location_latitude', Float(precision=9), nullable=False),
            Column('location_longitude', Float(precision=9), nullable=False),

            # -- -- Record time columns

            Column('local_datetime', DateTime(timezone=False), nullable=False),
            Column('local_timezone', String(256), nullable=False),

            # -- Measurements data columns

            # -- -- Air temperature & humidity measurements data columns

            Column('air_temp_celsius', Float(precision=4), nullable=True),

            Column('humidity', SmallInteger, nullable=True),

            Column('apparent_temp_celsius', Float(precision=4), nullable=True),

            # -- -- Atmospheric pressure data columns

            Column('atm_pressure_mbar', Float(precision=5), nullable=True),

            # -- -- Wind speed measurements data columns
            
            Column('wind_speed_kmh', Float(precision=4), nullable=True),
            Column('wind_gust_kmh', Float(precision=4), nullable=True),
            Column('wind_direction', Enum(RoseDirection), nullable=True),

            # -- -- Air quality data columns
            
            Column('air_toxic_co', Float(precision=9), nullable=True),
            Column('air_toxic_o3', Float(precision=5), nullable=True),
            Column('air_toxic_no2', Float(precision=5), nullable=True),
            Column('air_toxic_so2', Float(precision=5), nullable=True),
            Column('air_toxic_pm25', Float(precision=6), nullable=True),
            Column('air_toxic_pm10', Float(precision=6), nullable=True),
            
            Column('aqi_epa', SmallInteger, nullable=True),
            Column('aqi_defra', SmallInteger, nullable=True),

            # -- Additional data columns

            Column('conditions_report', String(256), nullable=True),


            # Table constraints & indexes

            # -- Uniqueness constraints
            
            UniqueConstraint(
                'location_country', 'location_name',
                'location_latitude', 'location_longitude',
                'local_datetime', 'local_timezone',
                name='key_columns'
            ),

            # -- Search indexes

            # -- -- Record location columns search indexes

            Index('location_country', 'location_country'),
            Index('location_name', 'location_name'),

            Index('location_position', 'location_latitude', 'location_longitude'),

            # -- -- Record time columns search indexes

            Index('local_datetime', 'local_datetime'),
            Index('local_timezone', 'local_timezone')
        ),

        properties={

            # Composite columns

            # -- Key data composite columns

            # -- -- Record location composite columns
            
            'location_position': composite(GeoPosition, 'location_latitude', 'location_longitude'),

            # -- Measurements data composite columns

            # -- -- Air temperature & humidity measurements data composite columns

            'air_temp': composite(AirTemp.__composite_generate__, 'air_temp_celsius'),
            'apparent_temp': composite(AirTemp.__composite_generate__, 'apparent_temp_celsius'),

            # -- -- Atmospheric pressure measurements data composite columns

            'atm_pressure': composite(AtmPressure.__composite_generate__, 'atm_pressure_mbar'),

            # -- -- Wind measurements data composite columns

            'wind_speed': composite(WindSpeed.__composite_generate__, 'wind_speed_kmh'),
            'wind_gust': composite(WindSpeed.__composite_generate__, 'wind_gust_kmh'),

            # -- -- Air quality measurements data composite columns

            'air_toxics': composite(
                AirToxics,
                'air_toxic_co', 'air_toxic_o3',
                'air_toxic_no2', 'air_toxic_so2',
                'air_toxic_pm25', 'air_toxic_pm10'
            )
        }
    )
