# Official lightweight Python image
FROM python:3.10-slim

# Do not write .pyc files and run in unbuffered mode (useful for logging)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# Set working directory
WORKDIR /app

# Install system dependencies needed to build some Python packages
# adjust packages (libpq-dev, build-essential, gcc) based on your project's needs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      gcc \
      libpq-dev \
      curl && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency specification first for Docker layer caching.
# Make sure your repo contains a requirements.txt (or adapt this to pyproject.toml / poetry).
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python dependencies
RUN python -m pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy project source code
COPY . /app

# Create a non-root user and give ownership of the app directory
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose the default port (override with PORT env var if needed)
EXPOSE 8000

# Basic healthcheck - adjust path if your app serves at a different endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT} || exit 1

# Allow the runtime command to be overridden via START_CMD environment variable.
# Default assumes your application package/module is runnable as "python -m src".
# If your entrypoint is different (e.g. src.main, app.py, or uvicorn), override START_CMD at runtime:
# docker run -e "START_CMD=uvicorn src.app:app --host 0.0.0.0 --port ${PORT}" ...
ENTRYPOINT ["sh", "-c"]
CMD ["exec ${START_CMD:-python -m src}"]
