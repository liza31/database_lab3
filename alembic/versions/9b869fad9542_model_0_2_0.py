"""
Revision message:   model-0.2.0
Revision ID:        9b869fad9542
Revises:            a572d893fb6c

Created:            2024-04-23 18:35:44.326518
"""


from typing import Sequence

import sqlalchemy as sa
from alembic import op


# Revision identifiers, used by Alembic.

revision: str = '9b869fad9542'

down_revision: str | None = 'a572d893fb6c'
branch_labels: str | Sequence[str] | None = None

depends_on: str | Sequence[str] | None = None


def _get_weather_records() -> sa.TableClause:
    """
    Create '`weather_records`' table 'SQLAlchemy' :class:`TableClause` object,
    includes columns affected by the current revision
    """

    return sa.TableClause(

        # Table name

        'weather_records',

        # Table columns

        # -- Key data columns

        sa.ColumnClause('uuid'),

        # -- Measurements data columns

        # -- -- Air quality data columns

        sa.ColumnClause('air_toxic_co'),
        sa.ColumnClause('air_toxic_o3'),
        sa.ColumnClause('air_toxic_no2'),
        sa.ColumnClause('air_toxic_so2'),
        sa.ColumnClause('air_toxic_pm25'),
        sa.ColumnClause('air_toxic_pm10'),

        sa.ColumnClause('aqi_epa'),
        sa.ColumnClause('aqi_defra')

    )


def _get_air_quality_records() -> sa.TableClause:
    """
    Create '`air_quality_records`' table 'SQLAlchemy' :class:`TableClause` object,
    includes columns affected by the current revision
    """

    return sa.TableClause(

        # Table name

        'air_quality_records',

        # Table columns

        # -- Record UUID column

        sa.ColumnClause('uuid'),

        # -- Air toxics concentration measurements data columns

        sa.ColumnClause('toxic_co'),
        sa.ColumnClause('toxic_o3'),
        sa.ColumnClause('toxic_no2'),
        sa.ColumnClause('toxic_so2'),
        sa.ColumnClause('toxic_pm25'),
        sa.ColumnClause('toxic_pm10'),

        # -- Air quality indexes data columns

        sa.ColumnClause('aqi_epa'),
        sa.ColumnClause('aqi_defra')

    )


def upgrade() -> None:
    """
    Applies necessary operations for the DB forward migration,
    upgrading it's state to the version of the current revision
    (revision 9b869fad9542)
    """

    # Create new tables

    # -- Create 'air_quality_records' table

    air_quality_records = op.create_table(

        # -- -- Table name

        'air_quality_records',

        # -- -- Table columns

        # -- -- -- Record UUID column

        sa.Column('uuid', sa.Uuid(), nullable=False),

        # -- -- -- Air toxics concentration measurements data columns

        sa.Column('toxic_co', sa.Float(precision=9), nullable=True),
        sa.Column('toxic_o3', sa.Float(precision=5), nullable=True),
        sa.Column('toxic_no2', sa.Float(precision=5), nullable=True),
        sa.Column('toxic_so2', sa.Float(precision=5), nullable=True),
        sa.Column('toxic_pm25', sa.Float(precision=6), nullable=True),
        sa.Column('toxic_pm10', sa.Float(precision=6), nullable=True),

        # -- -- -- Air quality indexes data columns

        sa.Column('aqi_epa', sa.SmallInteger(), nullable=True),
        sa.Column('aqi_defra', sa.SmallInteger(), nullable=True),

        # -- -- Table constraints

        sa.PrimaryKeyConstraint(
            'uuid',
            name=op.f('air_quality_records__pk')
        ),

        sa.ForeignKeyConstraint(
            columns=['uuid'],
            refcolumns=['weather_records.uuid'],
            name=op.f('air_quality_records__fk__weather_records__uuid'),
            ondelete='CASCADE'
        )
    )

    # Migrate data the new schema version

    # -- Migrate air quality measurements data from existed 'weather_records' table
    #    to the new 'air_quality_records' table

    # -- -- Acquire SQLAlchemy table object for 'weather_records' table
    weather_records = _get_weather_records()

    # -- -- Execute data migration query
    op.execute(
        sa.insert(air_quality_records).from_select(
            names=[

                'uuid',

                'toxic_co', 'toxic_o3',
                'toxic_no2', 'toxic_so2',
                'toxic_pm25', 'toxic_pm10',

                'aqi_epa', 'aqi_defra'
            ],
            select=sa.select(weather_records.c[

                'uuid',

                'air_toxic_co', 'air_toxic_o3',
                'air_toxic_no2', 'air_toxic_so2',
                'air_toxic_pm25', 'air_toxic_pm10',

                'aqi_epa', 'aqi_defra'
            ])
        )
    )

    # Alter/drop existed tables

    # -- Alter 'weather_records' table

    # -- -- Drop outdated columns

    op.drop_column('weather_records', 'aqi_defra')
    op.drop_column('weather_records', 'aqi_epa')

    op.drop_column('weather_records', 'air_toxic_pm10')
    op.drop_column('weather_records', 'air_toxic_pm25')
    op.drop_column('weather_records', 'air_toxic_so2')
    op.drop_column('weather_records', 'air_toxic_no2')
    op.drop_column('weather_records', 'air_toxic_o3')
    op.drop_column('weather_records', 'air_toxic_co')


def downgrade() -> None:
    """
    Applies necessary operations for the DB backward migration,
    downgrading its state back to the version of the previous revision
    (revision a572d893fb6c)
    """

    # Alter/recreate modified/dropped tables

    # -- Alter 'weather_records' table

    # -- -- Recreate dropped columns

    op.add_column('weather_records', sa.Column('air_toxic_co', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('weather_records', sa.Column('air_toxic_o3', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('weather_records', sa.Column('air_toxic_so2', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('weather_records', sa.Column('air_toxic_no2', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('weather_records', sa.Column('air_toxic_pm25', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('weather_records', sa.Column('air_toxic_pm10', sa.REAL(), autoincrement=False, nullable=True))

    op.add_column('weather_records', sa.Column('aqi_epa', sa.SMALLINT(), autoincrement=False, nullable=True))
    op.add_column('weather_records', sa.Column('aqi_defra', sa.SMALLINT(), autoincrement=False, nullable=True))

    # Migrate data back to the previous schema version

    # -- Migrate air quality measurements data from new 'air_quality_records' table
    #    to the existed 'weather_records' table

    # -- -- Acquire SQLAlchemy table objects for 'weather_records' & 'air_quality_records' tables
    air_quality_records = _get_air_quality_records()
    weather_records = _get_weather_records()

    # -- -- Execute data migration query
    # noinspection PyTypeChecker
    op.execute(
        sa.update(weather_records).values(

            air_toxic_co=air_quality_records.c.toxic_co, air_toxic_o3=air_quality_records.c.toxic_o3,
            air_toxic_no2=air_quality_records.c.toxic_no2, air_toxic_so2=air_quality_records.c.toxic_so2,
            air_toxic_pm25=air_quality_records.c.toxic_pm25, air_toxic_pm10=air_quality_records.c.toxic_pm10,

            aqi_epa=air_quality_records.c.aqi_epa,
            aqi_defra=air_quality_records.c.aqi_defra

        ).where(weather_records.c.uuid == air_quality_records.c.uuid)
    )

    # Drop new tables

    # -- Drop 'air_quality_records' table

    op.drop_table('air_quality_records')
