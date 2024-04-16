"""
Revision message:   ${message}
Revision ID:        ${up_revision}
Revises:            ${down_revision if down_revision else "(nothing - base revision)"}

Created:            ${create_date}
"""


from typing import Sequence

import sqlalchemy as sa
from alembic import op
\
${'\n' + imports + '\n' if imports else ""}
\

# Revision identifiers, used by Alembic.

revision: str = ${repr(up_revision)}

down_revision: str | None = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}

depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    """
    Applies necessary operations for the DB forward migration,
    upgrading it's state to the version of the current revision
    (revision ${up_revision})
    """

    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """
    Applies necessary operations for the DB backward migration,
    downgrading its state back to ${"the version of the previous revision\n    " + \
    f"(revision {down_revision})" if down_revision else "empty"}
    """

    ${downgrades if downgrades else "pass"}
