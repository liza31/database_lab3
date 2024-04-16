from collections.abc import Mapping
from pathlib import Path
from typing import Any

from importlib import import_module

from sqlalchemy import URL, engine_from_config, pool

import logging.config

from alembic import context


# Declare script-level settings variables

# -- Sensitive options from-file loading path prefix characters
OPTIONS_FROMFILE_PREFIXES: str = \
    context.config.get_main_option('options.fromfile_prefixes', '%').replace(' ', "")


def get_custom_section(*section_alias, from_cfg: bool = True, from_cmd: bool = True) -> Mapping[str, Any]:
    """
    Return all the configuration options from an .ini file section and/or prefixed -x cmd arguments as a dictionary.

    Multiple names can be specified as an aliases for the same section name.

    **.ini / cmd syntax**

    * .ini file section to be recognized must have name matches on of the specified aliases.
    * -x cmd argument to be recognized must be written in a key-value form, where the key is prepended with
      prefix, matches one of the specified section name aliases and divided from the rest of the key by period.

    **Loading priority**

    Values acquired from the -x cmd arguments always take precedence over ones acquired from an .ini file

    **From-file value loading**

    To ensure Docker secrets support, there is also an ability to indirectly load any of these options
    from a text file instead of passing value as it is.

    To do so, pass a path to the corresponding text file instead of value and prepend it
    with one of the special prefix characters, specified by the 'options.fromfile_prefixes' option
    from the config's main section (defaults to '`%`').

    :param section_alias: aliases for the target section name

    :param from_cmd: whether to include options acquired from -x cmd arguments
    :param from_cfg: whether to include options acquired from an .ini file section

    :return: key-value :class:`Mapping[str, Any]` of configuration options from the given section

    :raise ValueError: on any issues with the options acquiring
    """

    # Collect options from requested sources

    opts = dict()

    # -- Acquire options from .ini file if necessary
    if from_cfg:
        for section_key in section_alias:
            section_opts = context.config.get_section(section_key)
            if section_opts is not None:
                opts.update(section_opts)

    # -- Acquire options from -x cmd arguments if necessary
    if from_cmd:
        opts.update(
            (key[key.index('.') + 1:], val)
            for key, val in context.get_x_argument(as_dictionary=True).items()
            if any(key.startswith(f"{section_key}.") for section_key in section_alias)
        )

    # Iterate over options and extract values from file where needed
    for key, path in ((key, val[1:]) for key, val in opts.items()
                      if type(val) is str and len(val) > 1
                      and val[0] in OPTIONS_FROMFILE_PREFIXES):

        try:

            # Try to read option value from file
            opts[key] = Path(path).read_text()

        except OSError as err:

            # -- Raise detailed error if file reading failed
            raise ValueError(f"Unable to read '{key}' option value from {path}") from err

    return opts


def get_sqlalchemy_url() -> str:
    """
    Extract SQLAlchemy connection URL (as :class:`str`) from the custom '`database`' / '`db`' config section
    (and/or -x cmd arguments - see :func:`get_custom_section` docs for more details about custom config options).

    **Options list**

    * `sqlalchemy.url` - SQLAlchemy connection URL (if provided - other options will be ignored)

    * `sqlalchemy.dialect` - SQLAlchemy database dialect name (required, if `sqlalchemy_url` is not provided)
    * `sqlalchemy.driver` - SQLAlchemy database driver name (required, if `sqlalchemy_url` is not provided)

    * `server.host` - dbms server host name (required, if `sqlalchemy_url` is not provided)
    * `server.port` - dbms server port number (required, if `sqlalchemy_url` is not provided)

    * `dbname` - target database name (required, if `sqlalchemy_url` is not provided)

    * `user` - target database user login (required, if `sqlalchemy_url` is not provided)
    * `pass` - target database user password (required, if `sqlalchemy_url` is not provided)

    :return: extracted SQLAlchemy URL :class:`str`

    :raise ValueError: on any issues with the options or their acquiring
                       (missed credentials options, validation fails, etc.)
    """

    # Acquire database credentials options through the get_custom_section()
    creds = get_custom_section('db', 'database', from_cfg=True, from_cmd=True)

    # If collected options contains `sqlalchemy.url` key, just return it's value
    if 'sqlalchemy.url' in creds:
        return creds['sqlalchemy.url']

    try:

        # Try to form SQLAlchemy connection URL using URL.create()
        return URL.create(
            f"{creds['sqlalchemy.dialect']}+{creds['sqlalchemy.driver']}",
            host=creds['server.host'],
            port=int(creds['server.port']),
            database=creds['dbname'],
            username=creds['user'],
            password=creds['pass']
        ).render_as_string(hide_password=False)

    except ValueError:

        # -- Raise a detailed error if 'server.port' validation failed
        raise ValueError(f"Value of the 'server.port' option must be an integer")

    except KeyError as err:

        # -- Raise a detailed error if URL creation failed because of some credentials are missed
        raise ValueError(f"Missed '{err.args[0]}' option is required for the SQLAlchemy connection URL")


def run_migrations_offline(**opts):
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation,
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output

    :param opts: options to be passed to the `connection.configure()`
    """

    # Declare default params for migration environment configuration
    params = dict(
        url=context.config.get_main_option('sqlalchemy.url'),
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'}
    )

    # Update default configuration params with opts and run context.configure()
    params.update(opts)
    context.configure(**params)

    # Invoke migration function within a transactional context
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(**opts):
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context

    :param opts: options to be passed to the `connection.configure()`
    """

    # Build-up SQLAlchemy Engine from the context configuration
    connectable = engine_from_config(
        context.config.get_section(
            context.config.config_ini_section,
            default={}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Establish dbms connection
    with connectable.connect() as connection:

        # Run context.configure() with passed opts and active dbms connection
        context.configure(connection=connection, **opts)

        # Invoke migration function within a transactional context
        with context.begin_transaction():
            context.run_migrations()


# On import, handle migration environment setup & run migrations

# -- Handle custom dbms connection configs & initialize logging configuration

# -- -- Extract SQLAlchemy connection URL from custom config section and/or cmd args
#    and push to the default config property
context.config.set_main_option('sqlalchemy.url', get_sqlalchemy_url())

# -- -- Configure logging through the config file
if context.config.config_file_name is not None:
    logging.config.fileConfig(context.config.config_file_name)

# -- Setup custom options for the migration environment & run migrations

# -- -- Declare custom migration environment settings map
migration_opts = dict(
    compare_type=False
)

# -- -- Try to acquire db model metadata for migrations autogenerate feature
try:
    migration_opts.update(target_metadata=getattr(import_module('wwweather.data.sqlalchemy'), 'model_metadata'))
except (ImportError, AttributeError):
    pass

# -- -- Dispatch migration mode and call appropriate handler function
if context.is_offline_mode():
    run_migrations_offline(**migration_opts)
else:
    run_migrations_online(**migration_opts)
