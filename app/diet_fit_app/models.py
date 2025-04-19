"""
models.py: Defines Pydantic models for request input (UserInput, DailyMeal) and response output (WorkoutPlan, DietPlan, CoachResult).
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Weekday(str, Enum):
    # Enum of days of the week used for scheduling plans
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class DailyMeal(BaseModel):
    # Represents a day's meals input by the user
    day: Weekday
    meals: str = Field(..., example="Breakfast: Oatmeal and banana. Lunch: Jollof rice with chicken. Dinner: Waakye with stew.")


class UserInput(BaseModel):
    # Input schema capturing the user's weekly meal log and fitness goals
    weekly_meals: List[DailyMeal]
    current_weight: str = Field(..., example="190 lbs")
    weight_goal: str = Field(..., example="Lose 10 lbs (target: 180 lbs)")
    workout_frequency: str = Field(..., example="Workout 2 times per week")

    class Config:
        schema_extra = {
            "example": {
                "weekly_meals": [
                    {
                        "day": "monday",
                        "meals": "Breakfast: Hausa koko with koose. Lunch: Jollof rice with fried chicken. Dinner: Waakye with gari, spaghetti, and boiled egg."
                    },
                    {
                        "day": "tuesday",
                        "meals": "Breakfast: Tea with bread and eggs. Lunch: Banku with okra stew. Dinner: Yam with palava sauce."
                    },
                    {
                        "day": "wednesday",
                        "meals": "Breakfast: Choco Milo with bread. Lunch: Kenkey with fried fish and pepper. Dinner: Light soup with fufu."
                    },
                    {
                        "day": "thursday",
                        "meals": "Breakfast: Tom brown. Lunch: Rice balls with groundnut soup. Dinner: Beans stew with plantain (red red)."
                    },
                    {
                        "day": "friday",
                        "meals": "Breakfast: Rice water with sugar and milk. Lunch: TZ with ayoyo soup. Dinner: Yam porridge with smoked fish."
                    },
                    {
                        "day": "saturday",
                        "meals": "Breakfast: Koko with bofrot. Lunch: Fried rice with kelewele. Dinner: Banku with tilapia and hot pepper."
                    },
                    {
                        "day": "sunday",
                        "meals": "Breakfast: Angwamo with fried egg. Lunch: Jollof with goat meat. Dinner: Fufu with palm nut soup."
                    }
                ],
                "current_weight": "190 lbs",
                "weight_goal": "Lose 15 lbs (target: 175 lbs)",
                "workout_frequency": "Workout 3 times per week"
            }
        }


class WorkoutPlan(BaseModel):
    # Output model for a day's workout recommendation
    day: Weekday
    activity: str = Field(..., example="30 mins of cardio and core workouts")


class DietPlan(BaseModel):
    # Output model for a day's diet recommendation
    day: Weekday
    meals: str = Field(..., example="Breakfast: Avocado toast. Lunch: Couscous with grilled fish. Dinner: Plantain with beans.")


class CoachResult(BaseModel):
    # Composite result including the generated workout and diet plans plus progress estimate
    workout_plan: List[WorkoutPlan] = Field(..., description="7-day custom workout schedule")
    diet_plan: List[DietPlan] = Field(..., description="3-day culturally sensitive diet plan")
    estimated_days_to_goal: int = Field(..., example=45, description="Projected days to reach target weight")
