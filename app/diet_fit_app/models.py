from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class Weekday(str, Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"


class DailyMeal(BaseModel):
    day: Weekday
    meals: str = Field(..., example="Breakfast: Oatmeal and banana. Lunch: Jollof rice with chicken. Dinner: Waakye with stew.")


class UserInput(BaseModel):
    weekly_meals: List[DailyMeal]
    current_weight: str = Field(..., example="190 lbs")
    weight_goal: str = Field(..., example="Lose 10 lbs (target: 180 lbs)")
    workout_frequency: str = Field(..., example="Workout 2 times per week")


class WorkoutPlan(BaseModel):
    day: Weekday
    activity: str = Field(..., example="30 mins of cardio and core workouts")


class DietPlan(BaseModel):
    day: Weekday
    meals: str = Field(..., example="Breakfast: Avocado toast. Lunch: Couscous with grilled fish. Dinner: Plantain with beans.")


class CoachResult(BaseModel):
    workout_plan: List[WorkoutPlan] = Field(..., description="7-day custom workout schedule")
    diet_plan: List[DietPlan] = Field(..., description="3-day culturally sensitive diet plan")
    estimated_days_to_goal: int = Field(..., example=45, description="Projected days to reach target weight")
