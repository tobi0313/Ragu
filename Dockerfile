# ---- builder: build wheels / install deps ----
FROM python:3.11-slim AS builder
WORKDIR /build

# Install build deps only in builder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements for wheel building
COPY requirements.txt .

# Build wheels for requirements AND their dependencies (no --no-deps)
# This ensures transitive dependencies like starlette are also built and available in /wheels.
RUN python -m pip install --upgrade pip wheel \
    && pip wheel --wheel-dir /wheels -r requirements.txt

# ---- runtime: smaller final image ----
FROM python:3.11-slim AS runtime
WORKDIR /app

# Create non-root user
RUN useradd -m appuser

# Copy wheels and install from them (no build tools needed at runtime)
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-index --find-links=/wheels -r requirements.txt \
    && rm -rf /wheels

# Copy app source (omit tests)
COPY src/ ./src

ENV PYTHONPATH=/app/src
USER appuser
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
