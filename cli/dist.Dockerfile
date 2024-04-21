# Declare build arguments

# -- Python version used for building
ARG PYTHON_VERSION=3.10.14


# [INTERMEDIATE] STAGE "build"
# Build package wheel distribution

FROM python:${PYTHON_VERSION}-slim as build

# -- Install 'build' package for distribution building
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install build

# -- Set package folder as workdir
WORKDIR /wwweather/cli

# -- Copy package sources & project files
COPY . .

# -- Build a wheel (only) distribution for package
RUN python -m build . --outdir dist --wheel


# [FINAL] STAGE
# Store built wheel distribution

FROM scratch

# -- Copy package's `dist` folder contents into `/python-dists`
COPY --from=build /wwweather/cli/dist /wwweather/dists
