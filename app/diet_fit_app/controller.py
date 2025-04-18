from fastapi import APIRouter, HTTPException
from app.diet_fit_app.models import UserInput,CoachResult
from app.diet_fit_app.service import run_fitness_pipeline

router = APIRouter()

@router.post("/fitness-plan", response_model=CoachResult)
async def analyze_fitness(input_data: UserInput):
    try:
        result = await run_fitness_pipeline(input_data)
        return result
    except Exception as e:
        print("Error", e)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
