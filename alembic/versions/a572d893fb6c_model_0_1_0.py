"""
Revision message:   model-0.1.0
Revision ID:        a572d893fb6c
Revises:            (nothing - base revision)

Created:            2024-04-16 18:15:05.870799
"""


from typing import Sequence

import sqlalchemy as sa
from alembic import op


# Revision identifiers, used by Alembic.

revision: str = 'a572d893fb6c'

down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None

depends_on: str | Sequence[str] | None = None


def _get_rosedirection() -> sa.Enum:
    """
    Create '`rosedirection`' enum type 'SQLAlchemy' class:`sa.Enum` object
    """

    return sa.Enum(
        'N', 'NNE', 'NE', 'ENE',
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW',
        name='rosedirection'
    )


def upgrade() -> None:
    """
    Applies necessary operations for the DB forward migration,
    upgrading it's state to the version of the current revision
    (revision a572d893fb6c)
    """

    # Declare types

    # -- Declare 'rosedirection' enum type

    # noinspection PyPep8Naming
    ROSEDIRECTION = _get_rosedirection()

    # Create new tables

    # -- Create `weather_records` table

    op.create_table(

        # -- -- Table name

        'weather_records',

        # -- -- Table columns

        # -- -- -- Key data columns

        sa.Column('uuid', sa.Uuid(), nullable=False),

        # -- -- -- -- Record location columns

        sa.Column('location_country', sa.String(length=128), nullable=False),
        sa.Column('location_name', sa.String(length=128), nullable=False),

        sa.Column('location_latitude', sa.Float(precision=9), nullable=False),
        sa.Column('location_longitude', sa.Float(precision=9), nullable=False),

        # -- -- -- -- Record time columns

        sa.Column('local_datetime', sa.DateTime(), nullable=False),
        sa.Column('local_timezone', sa.String(length=256), nullable=False),

        # -- -- -- Measurements data columns

        # -- -- -- -- Air temperature & humidity measurements data columns

        sa.Column('air_temp_celsius', sa.Float(precision=4), nullable=True),

        sa.Column('humidity', sa.SmallInteger(), nullable=True),

        sa.Column('apparent_temp_celsius', sa.Float(precision=4), nullable=True),

        # -- -- -- -- Atmospheric pressure measurements data columns

        sa.Column('atm_pressure_mbar', sa.Float(precision=5), nullable=True),

        # -- -- -- -- Wind speed measurements data columns

        sa.Column('wind_speed_kmh', sa.Float(precision=4), nullable=True),
        sa.Column('wind_gust_kmh', sa.Float(precision=4), nullable=True),
        sa.Column('wind_direction', ROSEDIRECTION, nullable=True),

        # -- -- -- -- Air quality data columns

        sa.Column('air_toxic_co', sa.Float(precision=9), nullable=True),
        sa.Column('air_toxic_o3', sa.Float(precision=5), nullable=True),
        sa.Column('air_toxic_no2', sa.Float(precision=5), nullable=True),
        sa.Column('air_toxic_so2', sa.Float(precision=5), nullable=True),
        sa.Column('air_toxic_pm25', sa.Float(precision=6), nullable=True),
        sa.Column('air_toxic_pm10', sa.Float(precision=6), nullable=True),

        sa.Column('aqi_epa', sa.SmallInteger(), nullable=True),
        sa.Column('aqi_defra', sa.SmallInteger(), nullable=True),

        # -- -- -- Additional data columns

        sa.Column('conditions_report', sa.String(length=256), nullable=True),

        # -- -- Table constraints

        sa.PrimaryKeyConstraint(
            'uuid',
            name=op.f('weather_records__pk')
        ),

        sa.UniqueConstraint(
            'location_country', 'location_name',
            'location_latitude', 'location_longitude',
            'local_datetime', 'local_timezone',
            name=op.f('weather_records__uq__key_columns')
        ),

        # -- -- Table creation options

        keep_existing=True
    )

    # -- -- Table search indexes

    # -- -- -- Record location columns search indexes

    op.create_index(
        op.f('weather_records__ix__local_datetime'),
        table_name='weather_records',
        columns=['local_datetime'],
        unique=False
    )
    op.create_index(
        op.f('weather_records__ix__local_timezone'),
        table_name='weather_records',
        columns=['local_timezone'],
        unique=False
    )

    op.create_index(
        op.f('weather_records__ix__location_country'),
        table_name='weather_records',
        columns=['location_country'],
        unique=False
    )

    # -- -- -- Record time columns search indexes

    op.create_index(
        op.f('weather_records__ix__location_name'),
        table_name='weather_records',
        columns=['location_name'],
        unique=False
    )
    op.create_index(
        op.f('weather_records__ix__location_position'),
        table_name='weather_records',
        columns=['location_latitude', 'location_longitude'],
        unique=False
    )


def downgrade() -> None:
    """
    Applies necessary operations for the DB backward migration,
    downgrading its state back to empty
    """

    # Drop new tables

    # -- Drop 'weather_records' table

    # -- -- Drop table search indexes

    op.drop_index(op.f('weather_records__ix__location_position'), table_name='weather_records')
    op.drop_index(op.f('weather_records__ix__location_name'), table_name='weather_records')
    op.drop_index(op.f('weather_records__ix__location_country'), table_name='weather_records')

    op.drop_index(op.f('weather_records__ix__local_timezone'), table_name='weather_records')
    op.drop_index(op.f('weather_records__ix__local_datetime'), table_name='weather_records')

    # -- -- Drop table itself

    op.drop_table('weather_records')

    # Drop new types

    # -- Drop 'rosedirection' enum type

    # noinspection PyPep8Naming
    ROSEDIRECTION = _get_rosedirection()
    ROSEDIRECTION.drop(bind=op.get_bind(), checkfirst=True)
