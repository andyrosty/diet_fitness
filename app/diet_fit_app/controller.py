"""
controller.py: Defines API endpoints for the Diet Fit application.
"""
from fastapi import APIRouter, HTTPException
from diet_fit_app.models import UserInput,CoachResult
from diet_fit_app.service import run_fitness_pipeline


# Router for nutrition and fitness analysis endpoints
router = APIRouter()

@router.post("/fitness-plan", response_model=CoachResult)
async def analyze_fitness(input_data: UserInput):
    """
    POST endpoint to generate a fitness and diet plan.
    Accepts UserInput JSON and returns a structured CoachResult.
    """
    try:
        # Invoke the service pipeline to get workout, diet, and estimate
        result = await run_fitness_pipeline(input_data)
        return result
    except Exception as e:
        # Log error and return HTTP 500
        print("Error in analyze_fitness:", e)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
