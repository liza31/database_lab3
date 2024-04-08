from abc import ABCMeta, abstractmethod
from collections.abc import Sequence

from wwweather.data.utils import Paginated

from wwweather.data.model import WeatherRecord


class ABCRecordsLoader(metaclass=ABCMeta):
    """
    Weather records loader abstraction.

    Typically used for records stream reading and deserialization.
    """

    @abstractmethod
    def load(self,
             *,
             limit: int = None,
             offset: int = 0,
             page_size: int = None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:
        """
        Loads all (or all up to `limit`) weather records from the feed.

        Can be used in both paginated and instant modes, depending on the `page_size` parameter value:
        if `page_size` is `None`, then instant mode will be used, returning :class:`Sequence` of all records at once,
        otherwise paginated loader with the `page_size` page size will be initialized
        and first page :class:`ABCResultsPage` object will be returned

        :param limit: maximum number of records to load (last records are truncated if exceeded)
                      or `None` for unlimited (defaults to `None`)
        :param offset: number of first stored records to skip (defaults to 0)
        :param page_size: page size for paginated mode or `None` for instant mode (default)

        :return: :class:`Sequence` of :class:`WeatherRecord` instances in instant mode
                 or first page :class:`ABCResultsPage` contains sequence of :class:`WeatherRecord` instances
                 of corresponding results block in paginated mode

        :raise RuntimeError: if any error occurs during records loading
        """
