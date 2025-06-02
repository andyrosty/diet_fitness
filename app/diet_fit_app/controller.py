"""
controller.py: Defines API endpoints for the Diet Fit application.
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.diet_fit_app.models import UserInput, CoachResult
from app.diet_fit_app.service import run_fitness_pipeline
from app.db.database import get_db
from app.db.models import User, UserPlan, WorkoutPlan, DietPlan
from app.auth.dependencies import get_current_user


# Router for nutrition and fitness analysis endpoints
router = APIRouter()

@router.post("/fitness-plan", response_model=CoachResult)
async def analyze_fitness(
    input_data: UserInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    POST endpoint to generate a fitness and diet plan.
    Requires authentication.
    """
    try:
        # Invoke the service pipeline to get workout, diet, and estimate
        # Also store the results in the database
        result = await run_fitness_pipeline(input_data, db, current_user.id)
        return result
    except Exception as e:
        # Log error and return HTTP 500
        print("Error in analyze_fitness:", e)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.get("/my-plans", response_model=list[CoachResult])
async def get_user_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    GET endpoint to retrieve all fitness plans for the current user.
    """
    try:
        # Get all plans for the current user
        user_plans = db.query(UserPlan).filter(UserPlan.user_id == current_user.id).all()

        # Convert database models to Pydantic models
        results = []
        for plan in user_plans:
            # Get workout plans for this user plan
            workout_plans = []
            for wp in plan.workout_plans:
                workout_plans.append({
                    "day": wp.day,
                    "activity": wp.activity
                })

            # Get diet plans for this user plan
            diet_plans = []
            for dp in plan.diet_plans:
                diet_plans.append({
                    "day": dp.day,
                    "meals": dp.meals
                })

            # Create CoachResult object
            result = CoachResult(
                workout_plan=workout_plans,
                diet_plan=diet_plans,
                estimated_days_to_goal=plan.estimated_days_to_goal
            )
            results.append(result)

        return results
    except Exception as e:
        # Log error and return HTTP 500
        print("Error in get_user_plans:", e)
        raise HTTPException(status_code=500, detail=f"Error retrieving plans: {str(e)}")
