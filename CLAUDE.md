# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Simple Python Flask web application that serves "Hello World" at the root endpoint.

## Development Commands

### Local Development
```bash
pip install -r requirements.txt
python app.py
```

Application runs on `http://localhost:5000/`.

### Docker

Build and run using Chainguard Python images:
```bash
docker build -t flask-hello .
docker run -p 5000:5000 flask-hello
```

## Architecture

Single-file Flask application (app.py) with one route handler serving the root endpoint (/). Uses multi-stage Dockerfile with Chainguard images: `python:latest-dev` for building dependencies in a virtual environment, and `python:latest` for the minimal production runtime.
