# syntax=docker/dockerfile:1

# Builder stage: Install dependencies using the -dev variant
FROM cgr.dev/chainguard/python:latest-dev as builder

WORKDIR /app

# Create virtual environment
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Install dependencies
COPY --chown=nonroot:nonroot requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage: Use minimal runtime image
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

# Copy application code
COPY --chown=nonroot:nonroot app.py .

# Copy virtual environment from builder
COPY --from=builder /app/venv /app/venv

# Set PATH to use virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Expose Flask default port
EXPOSE 5000

# Run the application
ENTRYPOINT ["python", "app.py"]
