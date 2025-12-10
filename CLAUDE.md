# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simple Python Flask web application that serves "Hello World" at the root endpoint.

## Development Commands

### Local Development Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### Run Application Locally
```bash
python app.py
```
Application runs on `http://localhost:5000/`.

### Testing

Run unit tests:
```bash
pytest test_app.py -v
```

Run integration tests (requires Docker):
```bash
pytest test_docker_integration.py -v
```

Run all tests:
```bash
pytest -v
```

### Docker

Build and run using Chainguard Python images:
```bash
docker build -t flask-hello .
docker run -p 5000:5000 flask-hello
```

## Release Process

This project uses semantic versioning (v1.2.3) with automated releases via GitHub Actions.

### Creating a Release

1. Ensure all changes are committed and pushed to main
2. Create and push a version tag:
```bash
git tag v1.0.0
git push origin v1.0.0
```

3. GitHub Actions automatically:
   - Runs unit tests
   - Builds Docker image for linux/amd64
   - Runs integration tests on amd64 image
   - Builds multi-platform images (linux/amd64, linux/arm64)
   - Pushes images to GitHub Container Registry (ghcr.io)
   - Creates GitHub Release with notes

### Docker Image Tags

Each release creates multiple tags:
- `ghcr.io/bjorn/gh-actions-test:v1.2.3` - Exact version
- `ghcr.io/bjorn/gh-actions-test:v1.2` - Major.minor
- `ghcr.io/bjorn/gh-actions-test:v1` - Major version
- `ghcr.io/bjorn/gh-actions-test:latest` - Latest release
- `ghcr.io/bjorn/gh-actions-test:abc1234` - Git commit SHA

### Using Released Images

All images support both linux/amd64 and linux/arm64:

```bash
docker pull ghcr.io/bjorn/gh-actions-test:latest
docker run -p 5000:5000 ghcr.io/bjorn/gh-actions-test:latest
```

Docker automatically pulls the correct architecture for your platform.

## Architecture

Single-file Flask application (app.py) with one route handler serving the root endpoint (/).

**Testing:**
- Unit tests (test_app.py) - Test Flask routes and responses using pytest
- Integration tests (test_docker_integration.py) - Build and test full Docker image

**Docker:**
Multi-stage Dockerfile with Chainguard images: `python:latest-dev` for building dependencies in a virtual environment, and `python:latest` for the minimal production runtime.

**CI/CD:**
- `.github/workflows/ci.yml` - Runs tests on PRs and main branch pushes
- `.github/workflows/release.yml` - Builds and publishes on version tags
