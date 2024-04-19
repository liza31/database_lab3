from abc import ABCMeta, abstractmethod
from collections.abc import Iterable

from wwweather.data.model import WeatherRecord


class ABCWeatherRecordsFormatter(metaclass=ABCMeta):
    """
    :class:`WeatherRecord` object groups string formatter abstraction
    """

    @abstractmethod
    def format_from(self, records: Iterable[WeatherRecord]):
        """
        Format group of :class:`WeatherRecord` objects from the given :class:`Iterable` into a string for display.

        :param records: :class:`Iterable` of :class:`WeatherRecord` objects to format

        :return: formated string table of passed records data
        """

    def format(self, *records: WeatherRecord):
        """
        Format given group of :class:`WeatherRecord` objects into a string for display.

        :param records: :class:`WeatherRecord` objects to format

        :return: formated string table of passed records data
        """

        # Forward call to the tabulate_records_from()
        return self.format_from(records)
