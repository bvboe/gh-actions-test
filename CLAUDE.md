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

### Kubernetes Deployment

Deploy to Kubernetes using Helm:

```bash
# Install the chart
helm install flask-hello ./helm/flask-hello

# Or with custom values
helm install flask-hello ./helm/flask-hello \
  --set image.tag=v1.0.0 \
  --set replicaCount=3

# Upgrade existing deployment
helm upgrade flask-hello ./helm/flask-hello

# Uninstall
helm uninstall flask-hello
```

**Access the application:**
```bash
# Port-forward to access locally
kubectl port-forward svc/flask-hello 8080:80
# Visit http://localhost:8080
```

**Enable Ingress (optional):**
```bash
helm install flask-hello ./helm/flask-hello \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=flask-hello.example.com \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix
```

**Enable autoscaling (optional):**
```bash
helm install flask-hello ./helm/flask-hello \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=10
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
   - Runs Docker integration tests
   - Deploys to Kubernetes (kind) and runs end-to-end tests
   - Builds multi-platform images (linux/amd64, linux/arm64)
   - Pushes Docker images to GitHub Container Registry (ghcr.io)
   - Packages and pushes Helm chart as OCI artifact
   - Creates GitHub Release with notes

### Docker Image Tags

Each release creates multiple tags:
- `ghcr.io/bjorn/gh-actions-test:v1.2.3` - Exact version
- `ghcr.io/bjorn/gh-actions-test:v1.2` - Major.minor
- `ghcr.io/bjorn/gh-actions-test:v1` - Major version
- `ghcr.io/bjorn/gh-actions-test:latest` - Latest release
- `ghcr.io/bjorn/gh-actions-test:abc1234` - Git commit SHA

### Helm Chart

Each release publishes the Helm chart as an OCI artifact:

**Install from OCI registry:**
```bash
helm install flask-hello oci://ghcr.io/bvboe/charts/flask-hello --version 1.0.0
```

**Or install from repository with specific image version:**
```bash
helm install flask-hello ./helm/flask-hello --set image.tag=v1.0.0
```

### Using Released Images

All images support both linux/amd64 and linux/arm64:

```bash
docker pull ghcr.io/bvboe/gh-actions-test:latest
docker run -p 5000:5000 ghcr.io/bvboe/gh-actions-test:latest
```

Docker automatically pulls the correct architecture for your platform.

## Architecture

Single-file Flask application (app.py) with one route handler serving the root endpoint (/).

**Testing:**
- Unit tests (test_app.py) - Test Flask routes and responses using pytest
- Docker integration tests (test_docker_integration.py) - Build and test full Docker image
- Kubernetes integration tests (CI workflow) - Deploy to kind cluster and verify end-to-end functionality

**Docker:**
Multi-stage Dockerfile with Chainguard images: `python:latest-dev` for building dependencies in a virtual environment, and `python:latest` for the minimal production runtime.

**Kubernetes:**
Helm chart (helm/flask-hello/) for Kubernetes deployment with:
- Deployment with configurable replicas and security context
- ClusterIP Service exposing port 80 → 5000
- Optional Ingress for external access
- Optional HorizontalPodAutoscaler for scaling
- ServiceAccount with minimal permissions
- Liveness and readiness probes

**CI/CD:**
- `.github/workflows/test-and-build.yml` - Reusable workflow with 3 jobs:
  - Unit tests (pytest)
  - Docker integration tests
  - Kubernetes integration tests (kind cluster deployment and E2E testing)
- `.github/workflows/ci.yml` - Runs test-and-build workflow on PRs and main pushes
- `.github/workflows/release.yml` - On version tags:
  - Runs test-and-build workflow
  - Builds multi-platform Docker images
  - Packages and pushes Helm chart as OCI artifact
  - Creates GitHub Release
- `.github/dependabot.yml` - Automated dependency updates:
  - Python dependencies (weekly)
  - GitHub Actions (weekly)
  - Docker base images (weekly)
