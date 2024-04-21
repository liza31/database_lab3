# Declare primary build arguments

# -- ARG: Python version to run 'Alembic' under
ARG PYTHON_VERSION=3.10.14


# [FINAL] STAGE
# Confgiure Python & os users, copy migration environment files,
# install 'Alembic' with required db drivers and other packages,
# configure image workdir & entrypoint

FROM python:${PYTHON_VERSION}-slim AS base

# -- Configure Python interpreter via environment variables

# -- -- Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# -- -- Keeps Python from buffering stdout and stderr to avoid situations where
#       the application crashes without emitting any logs due to buffering
ENV PYTHONUNBUFFERED=1

# -- Create a non-privileged primary user 'Alembic' will run under

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

# -- Set 'Alembic' migration environment folder root as workdir
WORKDIR /wwweather/alembic

# -- Copy migration environment files
COPY migrations migrations

# -- Install required db drivers from the 'requirements.requirements.db_drivers.txt' requirements file
#       and `Alembic` with required packages from the 'requirements.txt' requirements file
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.db_drivers.txt,target=requirements.db_drivers.txt \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.db_drivers.txt -r requirements.txt

# -- Set entrypoint to an 'Alembic' invocation
ENTRYPOINT ["python", "-m", "alembic"]
