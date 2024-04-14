from sqlalchemy import MetaData


# Define publicly visible members
__all__ = ['create_metadata_obj', 'CK_NAMING_CONVENTION']


CK_NAMING_CONVENTION = {
    "ix": "%(table_name)s__ix__%(constraint_name)s",
    "uq": "%(table_name)s__uq__%(constraint_name)s",
    "ck": "%(table_name)s__ck__%(constraint_name)s",
    "fk": "%(table_name)s__fk__%(referred_table_name)s__%(column_0_name)s",
    "pk": "%(table_name)s__pk"
}
"""
Database constraints naming convention 
for SQLAlchemy :class:`MetaData` objects configuration  
"""


def create_metadata_obj() -> MetaData:
    """
    Creates and configures new SQLAlchemy :class:`MetaData` object
    specifically for the WWWeather data model
    """

    return MetaData(naming_convention=CK_NAMING_CONVENTION)
