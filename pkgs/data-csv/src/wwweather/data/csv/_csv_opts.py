from typing import Any, ClassVar
from collections.abc import Sequence, Mapping
from dataclasses import dataclass

from copy import copy

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

    DEFAULT_TRUE_LITERALS: ClassVar[Sequence[str]] = ['true', 'yes', '1']
    """
    Default boolean `True` literals collection (all lowercase, first is taken for dumping) 
    """

    true_literals: Sequence[str]
    """
    Boolean `True` literals collection (all lowercase, first is taken for dumping)
    """

    DEFAULT_FALSE_LITERALS: ClassVar[Sequence[str]] = ['false', 'no', '0']
    """
    Default boolean `False` literals collection (all lowercase, first is taken for dumping)
    """

    false_literals: Sequence[str]
    """
    Boolean `False` literals collection (all lowercase, first is taken for dumping)
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
                 true_literals: Sequence[str] = None,
                 false_literals: Sequence[str] = None,
                 default_formatting_params: bool = True,
                 **formatting_params: Any):
        """
        Initialize new :class:`CSVOpts` instance

        :param datetime_format: datetime formatting pattern in :func:`time.strftime`/:func:`time.strptime` format
                                (defaults to the :attr:`DEFAULT_DATETIME_FORMAT`)

        :param true_literals: boolean `True` literals collection (all values will be forced to lowercase,
                              first will be taken for dumbing, defaults to :attr:`DEFAULT_TRUE_LITERALS`)
        :param false_literals: boolean `False` literals collection (all values will be forced to lowercase,
                              first will be taken for dumbing, defaults to :attr:`DEFAULT_TRUE_LITERALS`)

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
        object.__setattr__(self, 'true_literals', true_literals or copy(self.DEFAULT_TRUE_LITERALS))
        object.__setattr__(self, 'false_literals', false_literals or copy(self.DEFAULT_FALSE_LITERALS))
        object.__setattr__(self, 'csv_dialect', csv_dialect)
        object.__setattr__(self, 'formatting_params', formatting_params)

    @property
    def true_literal(self):
        """
        Primary boolean `True` literal to be used for dumping
        """

        return self.true_literals[0]

    @property
    def false_literal(self):
        """
        Primary boolean `False` literal to be used for dumping
        """

        return self.false_literals[0]

    def bool_2_str(self, val: bool):
        """
        Get primary (dumping) boolean string literal for the given :class:`bool` value
        """

        return self.true_literal if val else self.false_literal

    def parse_bool(self, bool_str: str) -> bool:
        """
        Parse boolean value from the given string by checking it for matching
        with :attr:`true_literals` or :attr:`false_literals`

        :return: parsed :class:`bool` value

        :raise ValueError: if the given string does not match any of `true_literals` or `false_literals`
        """

        # Cast string to a lowercase
        lower_string = bool_str.lower()

        # Check for True literals matches
        if lower_string in self.true_literals:
            return True

        # Check for False literals matches:
        if lower_string in self.false_literals:
            return False

        # Raise ValueError if nothing matched
        raise ValueError(f"Given string {repr(bool_str)} does not match any of boolean literals")
