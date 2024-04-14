from typing import Any, Literal
from collections.abc import Iterable, Sequence, Mapping, Callable
from dataclasses import dataclass, fields

from itertools import islice

from datetime import datetime

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError

from sqlalchemy import Select, BooleanClauseList, BinaryExpression
from sqlalchemy import select, insert, and_

from wwweather.data.utils import IterResultsPage, Paginated

# noinspection PyUnresolvedReferences
from wwweather.data.storage import ReleasableResourceMixin, ABCRecordsRepositoryManager, RecordsSearchParams

from wwweather.data.model import WeatherRecord


class SQLAlchemyRecordsRepositoryManager(ABCRecordsRepositoryManager):
    """
    :class:`ABCRecordsRepositoryManager` implementation on top of the SQLAlchemy orm.
    Allows to manage weather records storage in any of SQLAlchemy-supported relation database.

    **NOTE:** This class encapsulates a releasable resource, supports :class:`ReleasableResourceMixin` abstraction
    and requires proper resource realising through using class as a context management or `release()` method invocation
    """
    
    @classmethod
    def _model_asdict(cls, instance: dataclass, *, drop_none: bool = False) -> Mapping[str, Any]:
        """
        Unpack model object to an attributes key-value :class:`Mapping`

        :param instance: model object to be unpacked
        :param drop_none: whether to drop attributes with `None` values from the resulting mapping (`False` by default)

        :return: unpacked attributes key-value :class:`Mapping`
        """

        # Extract key-value pairs iterable from the given instance
        kv_iter = ((attr.name, getattr(instance, attr.name)) for attr in fields(instance))

        # Apply None filtering if needed
        if drop_none:
            kv_iter = filter(lambda item: item[1] is not None, kv_iter)

        # Create and return unpacked attributes mapping
        return dict(kv_iter)

    @classmethod
    def _generate_search_statement(cls, params: RecordsSearchParams) -> BinaryExpression | BooleanClauseList | None:
        """
        Generate a weather search condition statement to be used in "WHERE" clause within a SQLAlchemy "SELECT" query
        from the given :class:`RecordsSearchParams` instance

        :return: `None` if `params` are empty, otherwise conditional statement,
                  suitable to be used in "WHERE" clause within a SQLAlchemy "SELECT" query
        """

        # Build up all specified conditions as an SQLAlchemy statements

        conditions = list()

        # -- Build-up conditions on record location

        if params.location_country is not None:
            conditions.append(WeatherRecord.location_country == params.location_country)

        if params.location_name is not None:
            conditions.append(WeatherRecord.location_name == params.location_name)

        if params.location_position is not None:
            conditions.append(WeatherRecord.location_position == params.location_position)

        # -- Build-up conditions on record time

        if params.local_timezone is not None:
            conditions.append(WeatherRecord.local_timezone == params.local_timezone)

        # -- -- Build-up conditions on record time range

        local_start_date, local_end_date = \
            (params.local_date, params.local_date) \
            if params.local_date is not None \
            else (params.local_start_date, params.local_end_date)

        if local_start_date is not None:
            conditions.append(WeatherRecord.local_datetime >= datetime.combine(local_start_date, datetime.min.time()))

        if local_end_date is not None:
            conditions.append(WeatherRecord.local_datetime <= datetime.combine(local_end_date, datetime.max.time()))

        # Dispatch, form and return final combined statement
        return None if len(conditions) == 0 else conditions[0] if len(conditions) == 1 else and_(*conditions)

    _session: Session   # SQLAlchemy ORM Session to be used for all DB operations within a class

    def __init__(self, session_factory: Callable[[], Session] | sessionmaker):
        """
        Initializes new :class:`SQLAlchemyRecordsRepositoryManager` instance

        :param session_factory: SQLAlchemy :class:`sessionmaker` or other :class:`Session` factory
                                with the signature of `() -> Session`
        """

        # Connect to the database and store Session object
        self._session = session_factory()

    def import_all(self,
                   records: Iterable[WeatherRecord],
                   *,
                   block_size: int = None,
                   on_duplicate: Literal['raise', 'update', 'ignore'] = 'raise') -> int:

        # Ensure passed on_duplicate option is supported
        if on_duplicate not in ['raise', 'ignore']:
            raise NotImplementedError(
                f"Records duplication handling option {repr(on_duplicate)} "
                f"is not supported by {self.__class__.__name__}"
            )

        # Dispatch on_duplicate mode
        ignore_duplicates = on_duplicate == 'ignore'

        # Declare successfully inserted records counter
        records_inserted = 0

        def import_block(block_records: Iterable[WeatherRecord]):
            """
            Imports given block of weather records into a database through one commit
            """

            nonlocal ignore_duplicates, records_inserted

            # Extract insertion values from the given records
            block_vals = [self._model_asdict(record, drop_none=True) for record in block_records]

            try:

                # Use bulk insert within a session transaction to import given block
                with self._session.begin():
                    self._session.execute(insert(WeatherRecord), block_vals)

            except IntegrityError as dup_err:

                # Handle occurred records duplication in accordance with on_duplicate value
                if not ignore_duplicates:
                    raise RuntimeError(
                        "Records duplication detected" +
                        (f"in block {records_inserted // block_size}" if block_size is not None else "")
                    ) from dup_err

            else:

                # Increase inserted records counter on success
                records_inserted += len(block_vals)

        try:

            # Dispatch import mode
            if block_size is not None:

                # Create record instances iterator
                records_iter = iter(records)

                # Run loop to insert all data blocks in a block mode
                while True:

                    # Accumulate current block bulk values
                    records_block = list(islice(records_iter, block_size))

                    # Check exit
                    if len(records_block) == 0:
                        break

                    # Call import_block()
                    import_block(records_block)

            else:

                # Import all records at once in a continuous mode
                import_block(records)

        except SQLAlchemyError as err:

            if isinstance(err, DBAPIError):

                # -- Raise detailed error if server-side database error occurred
                raise RuntimeError("Data insertion failed due to the server-side database error") from err

            else:

                # -- Raise detailed error if data model handling error occurred
                raise RuntimeError("Data insertion failed") from err

        # Return successfully inserted records count
        return records_inserted

    def _select_by(self,
                   query: Select,
                   *,
                   limit: int | None,
                   offset: int,
                   page_size: int | None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:
        """
        Executes given select `query` with default additional options in paginated or instant mode.

        Mode dispatch depends on the `page_size` parameter value:
        if `page_size` is `None`, then instant mode will be used, returning :class:`Sequence` of all records at once,
        otherwise paginated query with the `page_size` page size will be initialized
        and first page :class:`ABCResultsPage` object will be returned

        :param limit: maximum number of records to select (last records are truncated if exceeded)
                      or `None` for unlimited (defaults to `None`)
        :param offset: number of first result records to skip (defaults to 0)
        :param page_size: page size for paginated mode or `None` for instant mode (default)

        :return: :class:`Sequence` of :class:`WeatherRecord` instances in instant mode
                 or first page :class:`ABCResultsPage` contains sequence of :class:`WeatherRecord` instances
                 of corresponding results block in paginated mode

        :raise RuntimeError: if any error occurs during records querying
        """

        # Form final query statement

        stmt = query

        # -- Add offset if needed
        if limit is not None:
            stmt = stmt.limit(limit)

        # -- Add limit if needed
        if offset is not None:
            stmt = stmt.offset(offset)

        # Dispatch export mode and try to query results in an appropriate way
        try:

            if page_size is not None:

                # -- Paginate query fetching in pagination mode
                return IterResultsPage(
                    self._session.scalars(stmt.execution_options(yield_per=page_size)),
                    page_size=page_size
                )

            else:

                # -- Fetch and return all results in instant mode
                return list(self._session.scalars(stmt))

        except SQLAlchemyError as err:

            if isinstance(err, DBAPIError):

                # -- Raise detailed error if server-side database error occurred
                raise RuntimeError("Data querying failed due to the server-side database error") from err

            else:

                # -- Raise detailed error if data model handling error occurred
                raise RuntimeError("Data querying failed") from err

    def export_all(self,
                   *,
                   limit: int = None,
                   offset: int = 0,
                   page_size: int = None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:

        # Form base query and forward call to the _select_by()
        return self._select_by(
            select(WeatherRecord),
            limit=limit,
            offset=offset,
            page_size=page_size
        )

    def search_all(self,
                   params: RecordsSearchParams,
                   *,
                   limit: int = None,
                   offset: int = 0,
                   page_size: int = None) -> Sequence[WeatherRecord] | Paginated[Sequence[WeatherRecord]]:

        # Build-up search statement from the given parameters
        search_stmt = self._generate_search_statement(params)

        # Form base statement
        base_stmt = select(WeatherRecord)

        # Apply search condition and forward call to the _select_by()
        return self._select_by(
            base_stmt if search_stmt is None else base_stmt.where(search_stmt),
            limit=limit,
            offset=offset,
            page_size=page_size
        )

    def release(self):

        # Close Session object
        self._session.close()
