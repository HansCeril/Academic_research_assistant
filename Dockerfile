# Both stages must use the same Python version and Debian release:
# the virtual environment built in the first stage is copied as-is.
FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS base

WORKDIR /app

# UV_COMPILE_BYTECODE for generating .pyc files -> faster application startup.
# UV_LINK_MODE=copy to silence warnings about not being able to use hard links
# since the cache and sync target are on separate file systems.
# UV_PYTHON_DOWNLOADS=0 to use the image's Python instead of downloading one.
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Install dependencies only (the project itself is not a package)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project


FROM python:3.14-slim-trixie AS final

# Apply Debian security fixes published since the base image was built.
# Remove pip: unused at runtime (dependencies come from the venv) and it
# vendors its own urllib3/msgpack/setuptools, flagged by scanners.
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip uninstall -y pip \
    && rm -rf /usr/local/lib/python3.14/ensurepip/_bundled

# Run as an unprivileged user instead of root
RUN groupadd --system app && useradd --system --gid app --no-create-home app

EXPOSE 8000

# PYTHONUNBUFFERED=1 to disable output buffering
ENV PYTHONUNBUFFERED=1
ARG VERSION=0.1.0
ENV APP_VERSION=$VERSION

WORKDIR /app

# Copy only the virtual environment and the source code
COPY --from=base /app/.venv /app/.venv
COPY src /app/src

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

USER app

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
