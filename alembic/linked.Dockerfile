# Declare primary build arguments

# -- Required packages distribution image references

# -- -- ARG: 'WWWeather.Core' package required version dists image
ARG DISTS__CORE=wwweather/dists/core:0.1.0

# -- -- ARG: 'WWWeather.Data-SQLAlchemy' package required version dists image
ARG DISTS__DATA_SQLALCHEMY=wwweather/dists/data-sqlalchemy:0.1.0


# Alias images specified by arguments

FROM ${DISTS__CORE} AS dists__core
FROM ${DISTS__DATA_SQLALCHEMY} AS dists__data_sqlalchemy


# [INTERMEDIATE] STAGE "dists"
# Collect required packages distributions from distribution images in one place

FROM scratch AS dists

# -- Copy `dists` folders contents from distribution images into single folder

WORKDIR /wwweather/dists

COPY --from=dists__core /wwweather/dists .
COPY --from=dists__data_sqlalchemy /wwweather/dists .


# [FINAL] STAGE
# Install additional packages acquired from distribution images to supply 'Alembic'
# with 'SQLAlchemy' metadata for the `WWWeather` db model,
# reconfigure image workdir & entrypoint

FROM wwweather/exts/alembic_unlinked

# -- Install 'Alembic' and required packages

# -- -- Set 'wwweather' folder root as workdir
WORKDIR /wwweather

# -- -- Install 'Alembic' and required packages from a requirements file
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.model.txt,target=alembic/requirements.model.txt \
    --mount=type=bind,from=dists,source=/wwweather/dists,target=dists \
    python -m pip install -r alembic/requirements.model.txt -f dists

# -- Reconfigure image workdir & entrypoint

# -- -- Set 'Alembic' migration environment folder root as workdir
WORKDIR /wwweather/alembic

# -- -- Set entrypoint to an 'alembic' invocation
ENTRYPOINT ["python", "-m", "alembic"]
