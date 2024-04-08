from abc import ABCMeta, abstractmethod
from collections.abc import Iterable

from wwweather.data.model import WeatherRecord


class ABCRecordsDumper(metaclass=ABCMeta):
    """
    Weather records dumper abstraction.

    Typically used for records serialization and stream writing.
    """

    @abstractmethod
    def dump(self, records: Iterable[WeatherRecord]):
        """
        Dumps given weather records to the destination.

        :raise RuntimeError: if any error occurs during records dumping
        """

    def dump_one(self, record: WeatherRecord):
        """
        Dumps the only given weather record to the destination.

        :raise RuntimeError: if any error occurs during record dumping
        """

        self.dump((record,))
