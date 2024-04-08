from typing import Literal
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence, Iterable

from . import ReleasableResourceMixin

# noinspection PyUnresolvedReferences
from wwweather.data.utils import ABCResultsPage, Paginated

from wwweather.data.model import WeatherRecord
from . import RecordsSearchParams


class ABCRecordsRepositoryManager(ReleasableResourceMixin, metaclass=ABCMeta):
    """
    Weather records repository manager abstraction.

    **NOTE:** This class encapsulates a releasable resource, supports :class:`ReleasableResourceMixin` abstraction
    and requires proper resource realising through using class as a context manager or `release()` method invocation
    """

    @abstractmethod
    def import_all(self,
                   records: Iterable[WeatherRecord],
                   *,
                   block_size: int = None,
                   on_duplicate: Literal['raise', 'update', 'ignore'] = 'raise') -> int:
        """
        Import given weather records into the repository.

        Can be used in both block and continuous modes, depending on the `block_size` parameter value:
        if `block_size` is `None`, then continuous mode will be used, importing all records at once,
        otherwise import process will be split into separate import tasks by blocks of `block_size` records each.

        **NOTE:** Block mode usage does not provide any safety guarantees by default,
        by they can be provided by specific repository implementations.

        **NOTE:** If repository implementation does not provide safety guarantees for the block mode,
        it is allowed for such implementation to ignore it, using continuous mode, regardless of the given parameters

        **Duplication handling**

        Records are considered as duplicates if they have the same UUID or all other key attributes values at once,
        where key attributes are (except :attr:`WeatherRecord.uuid`):

        * :attr:`WeatherRecord.location_name`
        * :attr:`WeatherRecord.location_country`
        * :attr:`WeatherRecord.location_latitude`
        * :attr:`WeatherRecord.location_longitude`
        * :attr:`WeatherRecord.local_timezone`
        * :attr:`WeatherRecord.local_time`

        In case if repository implementation supports duplication detection,
        it will handle duplicate records in accordance with the given `on_duplicate` option.

        Possible `on_duplicate` options are next:

        * '`raise`' - raise a :class:`RuntimeError` (default)
        * '`update`' - update existing record
        * '`ignore`' - skip duplicate record

        **NOTE:** If repository implementation does not support duplication detection, it must NOT raise any errors.

        **NOTE:** If repository implementation supports duplication detection, but not support some of the
        `on_duplicate` options, it must raise :class:`NotImplementedError` in case an unsupported option was passed

        :param records: :class:`Iterable` of :class:`WeatherRecord` instances to dump into the storage
        :param block_size: block size for size mode or `None` for continuous mode (default)
        :param on_duplicate: records duplication handling option (defaults to '`raise`')

        :return: number of successfully imported records

        :raise RuntimeError: if any error occurs during records import
                             (including records duplication if `on_duplicate` is '`raise`')
        :raise NotImplementedError: if passed `on_conflict` is not supported by repository implementation
        """

    @abstractmethod
    def export_all(self,
                   *,
                   limit: int = None,
                   offset: int = 0,
                   page_size: int = None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:
        """
        Exports all (or all up to `limit`) records from the repository.

        Can be used in both paginated and instant modes, depending on the `page_size` parameter value:
        if `page_size` is `None`, then instant mode will be used, returning :class:`Sequence` of all records at once,
        otherwise paginated query with the `page_size` page size will be initialized
        and first page :class:`ABCResultsPage` object will be returned

        :param limit: maximum number of records to export (last records are truncated if exceeded)
                      or `None` for unlimited (defaults to `None`)
        :param offset: number of first stored records to skip (defaults to 0)
        :param page_size: page size for paginated mode or `None` for instant mode (default)

        :return: :class:`Sequence` of :class:`WeatherRecord` instances in instant mode
                 or first page :class:`ABCResultsPage` contains sequence of :class:`WeatherRecord` instances
                 of corresponding results block in paginated mode

        :raise RuntimeError: if any error occurs during records export
        """

    @abstractmethod
    def search_all(self,
                   params: RecordsSearchParams,
                   *,
                   limit: int = None,
                   offset: int = 0,
                   page_size: int = None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:
        """
        Search for weather records by the given parameters, passed by :class:`RecordsSearchParams` instance.

        Can be used in both paginated and instant modes, depending on the `page_size` parameter value:
        if `page_size` is `None`, then instant mode will be used, returning :class:`Sequence` of all results at once,
        otherwise paginated query with the `page_size` page size will be initialized
        and first page :class:`ABCResultsPage` object will be returned

        :param params: search parameters as :class:`RecordsSearchParams` instance
        :param limit: maximum resulting number of records (last results are truncated if exceeded)
                      or `None` for unlimited (defaults to `None`)
        :param offset: number of first found records to skip (defaults to 0)
        :param page_size: page size for paginated mode or `None` for instant mode (default)

        :return: :class:`Sequence` of :class:`WeatherRecord` instances in instant mode
                 or first page :class:`ABCResultsPage` contains sequence of :class:`WeatherRecord` instances
                 of corresponding results block in paginated mode

        :raise RuntimeError: if any error occurs during search querying
        """

    def search_one(self, params: RecordsSearchParams, *, offset: int = 0) -> WeatherRecord | None:
        """
        Search for only weather record by the given parameters, passed by :class:`RecordsSearchParams` instance.

        If more than one record is found, the first one will be returned

        :param params: search parameters as :class:`RecordsSearchParams` instance
        :param offset: number of first found records to skip (defaults to 0)

        :return: :class:`WeatherRecord` instance if any record found, otherwise `None`

        :raise RuntimeError: if any error occurs during search querying
        """

        result = self.search_all(params, limit=1, offset=offset, page_size=None)

        return None if len(result) == 0 else result[0]
