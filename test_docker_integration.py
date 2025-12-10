"""Integration tests for the Docker image."""
import subprocess
import time
import requests
import pytest


@pytest.fixture(scope="module")
def docker_container():
    """Build and run the Docker container for testing."""
    # Build the image
    print("\nBuilding Docker image...")
    build_result = subprocess.run(
        ["docker", "build", "-t", "flask-hello:test", "."],
        capture_output=True,
        text=True
    )
    assert build_result.returncode == 0, f"Docker build failed: {build_result.stderr}"

    # Start the container
    print("Starting Docker container...")
    run_result = subprocess.run(
        ["docker", "run", "-d", "-p", "5002:5000", "--name", "flask-hello-integration-test", "flask-hello:test"],
        capture_output=True,
        text=True
    )
    assert run_result.returncode == 0, f"Docker run failed: {run_result.stderr}"
    container_id = run_result.stdout.strip()

    # Wait for container to be ready
    time.sleep(2)

    # Verify container is running
    ps_result = subprocess.run(
        ["docker", "ps", "--filter", f"id={container_id}", "--format", "{{.Status}}"],
        capture_output=True,
        text=True
    )
    assert "Up" in ps_result.stdout, "Container is not running"

    yield container_id

    # Cleanup
    print("\nCleaning up Docker container...")
    subprocess.run(["docker", "stop", container_id], capture_output=True)
    subprocess.run(["docker", "rm", container_id], capture_output=True)


def test_docker_container_responds(docker_container):
    """Test that the Docker container responds to HTTP requests."""
    response = requests.get("http://localhost:5002/", timeout=5)
    assert response.status_code == 200
    assert response.text == "Hello World"


def test_docker_container_health(docker_container):
    """Test that the container is healthy and running."""
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.State.Status}}", docker_container],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "running"


def test_docker_image_uses_chainguard(docker_container):
    """Verify the image is based on Chainguard Python."""
    result = subprocess.run(
        ["docker", "inspect", "--format", "{{.Config.Image}}", "flask-hello:test"],
        capture_output=True,
        text=True
    )
    # Check build history for Chainguard base
    history_result = subprocess.run(
        ["docker", "history", "flask-hello:test", "--no-trunc"],
        capture_output=True,
        text=True
    )
    assert "chainguard" in history_result.stdout.lower()


def test_docker_container_404(docker_container):
    """Test that non-existent routes return 404."""
    response = requests.get("http://localhost:5002/nonexistent", timeout=5)
    assert response.status_code == 404
