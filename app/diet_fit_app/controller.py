"""
controller.py: Defines API endpoints for the Diet Fit application.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.diet_fit_app.models import UserInput, CoachResult, UserPlanUpdate
from app.diet_fit_app.service import run_fitness_pipeline
from app.db.database import get_db
from app.db.models import User, UserPlan, WorkoutPlan, DietPlan
from app.auth.dependencies import get_current_user


# Router  for nutrition and fitness analysis endpoints
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


@router.put("/my-plans/{plan_id}", response_model=CoachResult)
async def update_user_plan(
    plan_id: int,
    update_data: UserPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    PUT endpoint to update an existing fitness plan.
    Requires authentication and plan ownership.
    """
    try:
        # Get the plan and verify ownership
        plan = db.query(UserPlan).filter(
            UserPlan.id == plan_id,
            UserPlan.user_id == current_user.id
        ).first()

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found or you don't have permission to update it"
            )

        # Update the plan with the provided data
        if update_data.current_weight is not None:
            plan.current_weight = update_data.current_weight
        if update_data.weight_goal is not None:
            plan.weight_goal = update_data.weight_goal
        if update_data.workout_frequency is not None:
            plan.workout_frequency = update_data.workout_frequency

        # Save changes to the database
        db.commit()

        # Return the updated plan in the response
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

        # Create CoachResult object with updated data
        result = CoachResult(
            workout_plan=workout_plans,
            diet_plan=diet_plans,
            estimated_days_to_goal=plan.estimated_days_to_goal
        )

        return result
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error and return HTTP 500
        print("Error in update_user_plan:", e)
        raise HTTPException(status_code=500, detail=f"Error updating plan: {str(e)}")


@router.delete("/my-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    DELETE endpoint to remove an existing fitness plan.
    Requires authentication and plan ownership.
    Returns 204 No Content on success.
    """
    try:
        # Get the plan and verify ownership
        plan = db.query(UserPlan).filter(
            UserPlan.id == plan_id,
            UserPlan.user_id == current_user.id
        ).first()

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan not found or you don't have permission to delete it"
            )

        # Delete the plan (cascade will handle related workout and diet plans)
        db.delete(plan)
        db.commit()

        # Return 204 No Content (handled by status_code in the decorator)
        return None
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log error and return HTTP 500
        print("Error in delete_user_plan:", e)
        raise HTTPException(status_code=500, detail=f"Error deleting plan: {str(e)}")
