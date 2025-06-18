"""
FastAPI application import test script.

This script verifies that the FastAPI application can be imported correctly,
which helps diagnose import errors, path issues, or other initialization problems.
It's a simple diagnostic tool to ensure the application is properly configured.
"""
import pytest
from fastapi import FastAPI

def test_app_import():
    """Test that the FastAPI app can be imported correctly"""
    from app.main import app
    assert isinstance(app, FastAPI)
    assert app.title == "Fitness And Diet App"

def test_app_routes():
    """Test that the app has the expected routes"""
    from app.main import app
    route_paths = [route.path for route in app.routes]
    assert "/auth/signup" in route_paths
    assert "/auth/login" in route_paths
    assert "/auth/users/me" in route_paths
