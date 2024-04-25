"""
Revision message:   model-0.3.0
Revision ID:        5dbe4bf358a5
Revises:            9b869fad9542

Created:            2024-04-25 15:34:44.621583
"""


from typing import Sequence

import sqlalchemy as sa
from alembic import op


# Revision identifiers, used by Alembic.

revision: str = '5dbe4bf358a5'

down_revision: str | None = '9b869fad9542'
branch_labels: str | Sequence[str] | None = None

depends_on: str | Sequence[str] | None = None


def _get_air_quality_records() -> sa.TableClause:
    """
    Create '`air_quality_records`' table 'SQLAlchemy' :class:`TableClause` object,
    includes columns affected by the current revision
    """

    return sa.TableClause(

        # Table name

        'air_quality_records',

        # Table columns

        # -- Air quality indexes data columns

        sa.ColumnClause('aqi_epa'),
        sa.ColumnClause('aqi_defra'),

        # -- Additional data columns

        sa.ColumnClause('acceptable')

    )


def upgrade() -> None:
    """
    Applies necessary operations for the DB forward migration,
    upgrading it's state to the version of the current revision
    (revision 5dbe4bf358a5)
    """

    # Alter/drop existed tables

    # -- Alter 'air_quality_records' table

    # -- -- Add new columns

    op.add_column('air_quality_records', sa.Column('acceptable', sa.Boolean(), nullable=True))

    # Migrate data the new schema version

    # -- Generate values for new 'acceptable' column in the modified 'air_quality_records' table

    # -- -- Acquire SQLAlchemy table object for 'air_quality_records' table
    air_quality_records = _get_air_quality_records()

    # -- -- Execute data migration query
    op.execute(sa.update(air_quality_records).values(
        acceptable=sa.not_(sa.or_(
            air_quality_records.c.aqi_epa > 3,
            air_quality_records.c.aqi_defra >= 7
        ))
    ))


def downgrade() -> None:
    """
    Applies necessary operations for the DB backward migration,
    downgrading its state back to the version of the previous revision
    (revision 9b869fad9542)
    """

    # Alter/recreate modified/dropped tables

    # -- Alter 'air_quality_records' table

    # -- -- Drop new columns

    op.drop_column('air_quality_records', 'acceptable')
