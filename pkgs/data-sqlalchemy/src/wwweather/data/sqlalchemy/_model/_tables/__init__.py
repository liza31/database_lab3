# Declare package-global `ModelsMapper` instance for all model mappers

from .._helpers import ModelsMapper
model_mapper = ModelsMapper()
"""
Package-global :class:`ModelsMapper` instance to register all individual models objects mapping methods in. 
"""


# Import all mapping methods, invoking their registration

from ._weather_records import map__WeatherRecord
