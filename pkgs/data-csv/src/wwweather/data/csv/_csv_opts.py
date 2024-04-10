from typing import Any, ClassVar
from collections.abc import Mapping
from dataclasses import dataclass

# noinspection PyUnresolvedReferences
import time
# noinspection PyUnresolvedReferences
import csv


@dataclass(frozen=True)
class CSVOpts:
    """
    Dataclass for the weather records CSV files load/dump options
    """

    DEFAULT_DATETIME_FORMAT: ClassVar[str] = '%Y-%m-%d %H:%M'
    """
    Default datetime formatting pattern in :func:`time.strftime()` / :func:`time.strptime()` format
    """

    datetime_format: str
    """
    Datetime formatting pattern in :func:`time.strftime` / :func:`time.strptime` format
    """

    DEFAULT_CSV_DIALECT: ClassVar[str | csv.Dialect] = "excel"
    """
    Default CSV dialect name (from :func:`csv.list_dialects`) or :class:`csv.Dialect` instance
    """

    csv_dialect: str | csv.Dialect | None
    """
    CSV dialect name (from :func:`csv.list_dialects`) or :class:`csv.Dialect` instance
    """

    DEFAULT_FORMATTING_PARAMS: ClassVar[Mapping[str, Any]] = dict(delimiter=',')
    """
    Default CSV formatting parameters to be used with :class:`csv.reader`/:class:`csv.writer`
    """

    formatting_params: Mapping[str, Any]
    """
    CSV formatting parameters to be used with :class:`csv.reader`/:class:`csv.writer` 
    """

    def __init__(self,
                 *,
                 datetime_format: str = DEFAULT_DATETIME_FORMAT,
                 csv_dialect: str | csv.Dialect = DEFAULT_CSV_DIALECT,
                 default_formatting_params: bool = True,
                 **formatting_params: Any):
        """
        Initialize new :class:`CSVOpts` instance

        :param datetime_format: datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
                                (defaults to the :attr:`DEFAULT_DATETIME_FORMAT`)

        :param csv_dialect: CSV dialect name or :class:`csv.Dialect` instance to be used
                            with :class:`csv.reader`/:class:`csv.writer` (defaults to the :attr:`DEFAULT_CSV_DIALECT`)

        :param formatting_params: CSV formatting parameters to be used with :class:`csv.reader`/:class:`csv.writer`
        :param default_formatting_params: whether to take default values for CSV formatting params from the
                                          :attr:`DEFAULT_FORMATTING_PARAMS` (if `formatting_params` specifies
                                          the same options, default values will be overridden, defaults to `True`)
        """

        # Update formatting params with default values if needed
        if default_formatting_params:
            formatting_params.update(self.DEFAULT_FORMATTING_PARAMS)

        # Store given parameters
        object.__setattr__(self, 'datetime_format', datetime_format)
        object.__setattr__(self, 'csv_dialect', csv_dialect)
        object.__setattr__(self, 'formatting_params', formatting_params)
