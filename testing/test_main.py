"""test_main.py: Tests for main FastAPI app import and OpenAPI schema."""

def test_import_app():
    """Test that the FastAPI app can be imported with the correct title."""
    from app.main import app
    assert app.title == "Fitness And Diet App"

def test_openapi_schema_contains_fitness_plan(client):
    """Test that the OpenAPI schema includes the /fitness-plan POST endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "/fitness-plan" in schema.get("paths", {})
    assert "post" in schema["paths"]["/fitness-plan"]