# Declare publicly visible settings
__all__ = [
    'ARGPARSE_ROOT_DESCRIPTION',
    'ARGPARSE_FROMFILE_PREFIXES',
    'ARGPARSE_ALLOW_ABBREW'
]


ARGPARSE_ROOT_DESCRIPTION: str = \
    "WWWeather CLI: supports running basic weather records database import/export & search operations."
"""
App root description
"""

ARGPARSE_FROMFILE_PREFIXES: str = '%'
"""
Arguments from-file loading path prefix characters
"""

ARGPARSE_ALLOW_ABBREW: bool = False
"""
Whether to allow long options to be abbreviated automatically
"""
