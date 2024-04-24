from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import SmallInteger, Float, Uuid

from sqlalchemy.orm import registry, composite

from wwweather.data.model import AirToxics
from wwweather.data.model import DataAirQuality

from . import model_mapper


# noinspection PyPep8Naming
@model_mapper.register_mapper
def map__DataAirQuality(reg: registry):
    """
    Maps :class:`WeatherRecord` model class onto database `weather_records` table
    using passed :class:`registry` instance.
    """

    reg.map_imperatively(

        DataAirQuality,

        local_table=Table(

            # Table name & metadata

            "air_quality_records",

            reg.metadata,


            # Table columns

            # -- Record UUID column

            Column('uuid', Uuid, ForeignKey('weather_records.uuid', ondelete="CASCADE"), primary_key=True),

            # -- Air toxics concentration measurements data columns

            Column('toxic_co', Float(precision=9), nullable=True),
            Column('toxic_o3', Float(precision=5), nullable=True),
            Column('toxic_no2', Float(precision=5), nullable=True),
            Column('toxic_so2', Float(precision=5), nullable=True),
            Column('toxic_pm25', Float(precision=6), nullable=True),
            Column('toxic_pm10', Float(precision=6), nullable=True),

            # -- Air quality indexes data columns

            Column('aqi_epa', SmallInteger, nullable=True),
            Column('aqi_defra', SmallInteger, nullable=True)
        ),

        properties={

            # Composite columns

            'toxics': composite(
                AirToxics,
                'toxic_co', 'toxic_o3',
                'toxic_no2', 'toxic_so2',
                'toxic_pm25', 'toxic_pm10'
            )
        }
    )
