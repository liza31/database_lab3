# Declare primary build arguments

# -- ARG: Python version to run 'WWWeather.CLI' under
ARG PYTHON_VERSION=3.10.14

# -- Required packages distribution image references

# -- -- ARG: 'WWWeather.Core' package required version dists image
ARG DISTS__CORE=wwweather/dists/core:0.1.0

# -- -- ARG: 'WWWeather.Data-CSV' package required version dists image
ARG DISTS__DATA_CSV=wwweather/dists/data-csv:0.1.0

# -- -- ARG: 'WWWeather.Data-SQLAlchemy' package required version dists image
ARG DISTS__DATA_SQLALCHEMY=wwweather/dists/data-sqlalchemy:0.1.0

# -- -- ARG: 'WWWeather.CLI' package required version dists image
ARG DISTS__CLI=wwweather/dists/cli:0.1.0


# [BASE] STAGE "base"
# Prepare base image: confgiure Python & os users,
# intall required db drivers

FROM python:${PYTHON_VERSION}-slim AS base

# -- Configure Python interpreter via environment variables

# -- -- Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# -- -- Keeps Python from buffering stdout and stderr to avoid situations where
#       the application crashes without emitting any logs due to buffering
ENV PYTHONUNBUFFERED=1

# -- Create a non-privileged primary user 'WWWeather.CLI' will run under

# -- -- ARG: Uername of primary user
ARG USERNAME=liza31

# -- -- ARG: UID of primary user
ARG USER_UID=10001

RUN adduser                   \
    --disabled-password       \
    --gecos ""                \
    --home "/nonexistent"     \
    --shell "/sbin/nologin"   \
    --no-create-home          \
    --uid "${USER_UID}"       \
    ${USERNAME}

# -- Set 'wwweather/cli' folder root as workdir
WORKDIR /wwweather/cli

# -- Install required db drivers from the 'requirements.db_drivers.txt' requirements file
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.db_drivers.txt,target=requirements.db_drivers.txt \
    python -m pip install -r requirements.db_drivers.txt


# Alias images specified by arguments

FROM ${DISTS__CORE} AS dists__core
FROM ${DISTS__DATA_CSV} AS dists__data_csv
FROM ${DISTS__DATA_SQLALCHEMY} AS dists__data_sqlalchemy
FROM ${DISTS__CLI} AS dists__cli


# [INTERMEDIATE] STAGE "dists"
# Collect required packages distributions from distribution images in one place

FROM scratch AS dists

# -- Copy `dists` folders contents from distribution images into single folder

WORKDIR /wwweather/dists

COPY --from=dists__core /wwweather/dists .
COPY --from=dists__data_csv /wwweather/dists .
COPY --from=dists__data_sqlalchemy /wwweather/dists .
COPY --from=dists__cli /wwweather/dists .


# [FINAL] STAGE
# Install 'WWWeather.CLI' and its dependencies (including acquired from distribution images),
# configure image workdir & entrypoint

FROM base

# -- Set 'wwweather' folder root as workdir
WORKDIR /wwweather

# -- Install 'WWWeather.CLI' and its dependencies packages
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,from=dists,source=/wwweather/dists,target=dists \
    python -m pip install WWWeather.CLI -f dists

# -- Set entrypoint to a 'WWWeather.CLI' invocation
ENTRYPOINT ["python", "-m", "wwweather.cli"]
