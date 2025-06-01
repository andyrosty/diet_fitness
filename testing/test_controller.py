"""test_controller.py: Tests for the /fitness-plan endpoint behavior."""

import pytest
from app.diet_fit_app.models import CoachResult, WorkoutPlan, DietPlan, Weekday

def generate_dummy_coach_result():
    """Generate a dummy CoachResult with 7-day workout and diet plans."""
    workout = [WorkoutPlan(day=day, activity="Test activity") for day in Weekday]
    diet = [DietPlan(day=day, meals="Test meals") for day in Weekday]
    return CoachResult(workout_plan=workout, diet_plan=diet, estimated_days_to_goal=7)

@pytest.fixture(autouse=True)
def dummy_pipeline(monkeypatch):
    """Automatically mock run_fitness_pipeline to return dummy results."""
    async def dummy_run(input_data):
        return generate_dummy_coach_result()
    monkeypatch.setattr(
        "app.diet_fit_app.controller.run_fitness_pipeline",
        dummy_run
    )

def test_fitness_plan_success(client):
    """Test that POST /fitness-plan returns the mocked CoachResult successfully."""
    payload = {
        "typical_breakfast": "Oatmeal",
        "typical_lunch": "Salad",
        "typical_dinner": "Soup",
        "typical_snacks": "Fruits",
        "dietary_restrictions": "None",
        "favorite_meals": "Oatmeal",
        "comfort_foods": "Ice cream",
        "eating_out_frequency": "Once a week",
        "eating_out_choices": "Cafes",
        "current_weight": "150 lbs",
        "weight_goal": "Lose 5 lbs",
        "workout_frequency": "Workout 3 times per week"
    }
    response = client.post("/fitness-plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["estimated_days_to_goal"] == 7
    assert len(data["workout_plan"]) == 7
    assert len(data["diet_plan"]) == 7

def test_fitness_plan_error(client, monkeypatch):
    """Test that POST /fitness-plan returns a 500 error when the pipeline raises."""
    async def error_run(input_data):
        raise RuntimeError("Test error")
    monkeypatch.setattr(
        "app.diet_fit_app.controller.run_fitness_pipeline",
        error_run
    )
    payload = {
        "typical_breakfast": "Oatmeal",
        "typical_lunch": "Salad",
        "typical_dinner": "Soup",
        "typical_snacks": "Fruits",
        "dietary_restrictions": "None",
        "favorite_meals": "Oatmeal",
        "comfort_foods": "Ice cream",
        "eating_out_frequency": "Once a week",
        "eating_out_choices": "Cafes",
        "current_weight": "150 lbs",
        "weight_goal": "Lose 5 lbs",
        "workout_frequency": "Workout 3 times per week"
    }
    response = client.post("/fitness-plan", json=payload)
    assert response.status_code == 500
    assert "Error processing request" in response.json().get("detail", "")