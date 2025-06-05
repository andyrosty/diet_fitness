"""
models.py: Defines Pydantic models for request input (UserInput) and response output (WorkoutPlan, DietPlan, CoachResult).
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


class UserInput(BaseModel):
    # Input schema capturing the user's dietary preferences and fitness goals
    typical_breakfast: str = Field(..., example="Oatmeal with fruits, eggs and toast, or cereal with milk")
    typical_lunch: str = Field(..., example="Jollof rice with chicken, sandwiches, or salads")
    typical_dinner: str = Field(..., example="Waakye with stew, fufu with soup, or pasta dishes")
    typical_snacks: str = Field(..., example="Fruits, nuts, yogurt, or biscuits")
    dietary_restrictions: str = Field(..., example="Lactose intolerant, vegetarian, or no specific restrictions")
    favorite_meals: str = Field(..., example="Banku with tilapia, fried rice with chicken, fufu with light soup")
    comfort_foods: str = Field(..., example="Chocolate, ice cream, kelewele, or jollof rice")
    eating_out_frequency: str = Field(..., example="Once a week, twice a month")
    eating_out_choices: str = Field(..., example="Fast food, local restaurants serving traditional dishes, or cafes")
    current_weight: str = Field(..., example="190 lbs")
    weight_goal: str = Field(..., example="Lose 10 lbs (target: 180 lbs)")
    workout_frequency: str = Field(..., example="Workout 2 times per week")

    class Config:
        schema_extra = {
            "example": {
                "typical_breakfast": "Hausa koko with koose, tea with bread and eggs, or Choco Milo with bread",
                "typical_lunch": "Jollof rice with fried chicken, Banku with okra stew, or Kenkey with fried fish and pepper",
                "typical_dinner": "Waakye with gari and spaghetti, Yam with palava sauce, or Light soup with fufu",
                "typical_snacks": "Fruits, nuts, kelewele, or bofrot",
                "dietary_restrictions": "No specific restrictions",
                "favorite_meals": "Jollof rice with chicken, Banku with tilapia, Fufu with light soup",
                "comfort_foods": "Kelewele, Waakye, Fufu with palm nut soup",
                "eating_out_frequency": "Once a week",
                "eating_out_choices": "Local restaurants serving traditional Ghanaian dishes, occasionally fast food",
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
    diet_plan: List[DietPlan] = Field(..., description="7-day culturally sensitive diet plan")
    estimated_days_to_goal: int = Field(..., example=45, description="Projected days to reach target weight")


class UserPlanUpdate(BaseModel):
    # Model for updating an existing user plan
    current_weight: Optional[str] = Field(None, example="185 lbs")
    weight_goal: Optional[str] = Field(None, example="Lose 5 lbs (target: 180 lbs)")
    workout_frequency: Optional[str] = Field(None, example="Workout 3 times per week")

    class Config:
        schema_extra = {
            "example": {
                "current_weight": "185 lbs",
                "weight_goal": "Lose 5 lbs (target: 180 lbs)",
                "workout_frequency": "Workout 3 times per week"
            }
        }
