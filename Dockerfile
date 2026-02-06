ARG PYTHON_VERSION=3.14-slim

FROM python:${PYTHON_VERSION} AS builder
ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1

# Tools required to build wheels and run tests during image build
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Copy minimal metadata first to maximize build cache for dependencies
COPY pyproject.toml README.md /src/

# Upgrade pip and install build tooling
RUN python -m pip install --upgrade pip setuptools wheel build

# Copy the full source and build a wheel
COPY . /src
RUN python -m build -w /wheels

# Optionally run test suite during build. Set --build-arg RUN_TESTS=false to skip.
ARG RUN_TESTS=true
RUN if [ "$RUN_TESTS" = "true" ]; then python -m pip install --no-cache-dir pytest && pytest -q; fi

### Final runtime image (minimal, non-root)
FROM python:${PYTHON_VERSION} AS runtime
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create a non-root user for safer runtime
RUN useradd --create-home appuser && chown appuser /app

# Copy built wheel(s) from builder and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl

USER appuser

# No implicit entrypoint provided by default. Override CMD when running the container.
CMD ["python", "-c", "print('No default entrypoint defined; override CMD')"]
