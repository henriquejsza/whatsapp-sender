# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir .

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY aplicacao/ ./aplicacao/
COPY principal.py ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Default command (can be overridden)
ENTRYPOINT ["python", "principal.py"]
CMD ["--teste"]
