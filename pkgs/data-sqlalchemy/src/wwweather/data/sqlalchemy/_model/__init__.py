# Import service stuff

from sqlalchemy.orm import registry

from ._meta_factory import *


# Declare package-global SQLAlchemy MetaData & registry instances for further model objects mapping

model_metadata = create_metadata_obj()
"""
SQLAlchemy MetaData instance, contains metadata for the mapped WWWeather model
"""

model_mapper_registry = registry(metadata=model_metadata)
"""
Package-global SQLAlchemy registry instance to be used for all model objects mapping.
"""


# Trigger model objects mapping onto db using package-global SQLAlchemy MetaData & registry instances

# -- Import model objects modifiers for SQLAlchemy CompositeAPI compatibility and invoke modifications

from ._composites import *

# -- Import model objects mappers and invoke mapping using package-global registry

from ._tables import *
model_mapper.map_registered(model_mapper_registry)
