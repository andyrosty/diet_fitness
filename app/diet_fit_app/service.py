"""
service.py: Core pipeline for generating fitness and diet plans and estimating progress using AI agents.

This module contains the AI-powered service layer for the Diet Fitness application.
It uses two AI agents:
1. A fitness coach agent that generates personalized workout and diet plans
2. An estimator agent that predicts how long it will take to reach fitness goals
"""
import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from sqlalchemy.orm import Session
from app.diet_fit_app.models import UserInput, CoachResult
from app.db.models import UserPlan, WorkoutPlan as DBWorkoutPlan, DietPlan as DBDietPlan

# Load OpenAI API key for AI providers from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# GPT-03 Agent – Primary AI coach that generates workout and diet plans based on user input
# This agent takes user preferences and goals as input and produces a structured fitness plan
gpt03_agent = Agent(
    model="o3",                     # Using OpenAI's o3 model for plan generation
    deps_type=UserInput,            # Input type: User's fitness data and preferences
    result_type=CoachResult,        # Output type: Structured workout and diet plans
    providers=[OpenAIProvider(api_key=OPENAI_API_KEY)],  # Using OpenAI as the AI provider
    system_prompt=(
        "You are a fitness and nutrition AI coach. Based on the user's dietary preferences "
        "(typical meals, restrictions, favorites, and eating habits), "
        "current weight, weight goal, and workout frequency, provide:\n"
        "1. A 7-day workout plan\n"
        "2. A 7-day culturally sensitive diet plan\n"
        "Do not estimate the number of days to reach the goal."
    )
)


@gpt03_agent.system_prompt
async def gpt03_context(ctx: RunContext[UserInput]):
    """
    Dynamic context generator for the fitness coach agent.

    This function extracts user information from the input and formats it
    into a detailed context that helps the AI generate personalized plans.

    Args:
        ctx: Run context containing the user input data

    Returns:
        str: Formatted user context for the AI prompt
    """
    # Inject dynamic user context into the system prompt
    user = ctx.deps
    return (
        f"The user weighs {user.current_weight}, wants to {user.weight_goal}, and works out {user.workout_frequency}.\n"
        f"Dietary information:\n"
        f"- Typical breakfast: {user.typical_breakfast}\n"
        f"- Typical lunch: {user.typical_lunch}\n"
        f"- Typical dinner: {user.typical_dinner}\n"
        f"- Typical snacks: {user.typical_snacks}\n"
        f"- Dietary restrictions: {user.dietary_restrictions}\n"
        f"- Favorite meals: {user.favorite_meals}\n"
        f"- Comfort foods: {user.comfort_foods}\n"
        f"- Eating out frequency: {user.eating_out_frequency}\n"
        f"- Eating out choices: {user.eating_out_choices}"
    )


# Estimator Agent – Secondary AI that predicts days to goal from the generated fitness plan
# This agent analyzes the workout and diet plan to estimate time to reach the weight goal
estimator_agent = Agent(
    model="gpt-4o",                 # Using GPT-4o for more accurate time estimation
    deps_type=CoachResult,          # Input type: The generated fitness plan
    result_type=int,                # Output type: Number of days to reach goal
    providers=[OpenAIProvider(api_key=OPENAI_API_KEY)],  # Using OpenAI as the AI provider
    system_prompt=(
        "You are a health progress analyst AI. Given a workout and diet plan, estimate how many days "
        "it will take the user to reach their weight goal. Consider the user's consistency, frequency, "
        "and intensity of the routine when making the prediction."
    )
)


@estimator_agent.tool
async def estimate_days_to_goal(ctx: RunContext[CoachResult], result: CoachResult) -> int:
    """
    Tool function for the estimator agent to predict goal achievement time.

    This function is called by the estimator agent to analyze the fitness plan
    and predict how many days it will take to reach the weight goal.

    Args:
        ctx: Run context containing the fitness plan
        result: The generated fitness plan (workout and diet)

    Returns:
        int: Estimated number of days to reach the weight goal
    """
    return 0  # Placeholder - Estimator agent will generate this value dynamically


async def run_fitness_pipeline(user_input: UserInput, db: Session = None, user_id: int = None) -> CoachResult:
    """
    Orchestrates the complete fitness and diet planning pipeline.

    This is the main service function that:
    1. Generates a personalized 7-day workout plan and diet plan using the coach agent
    2. Estimates days to reach weight goal using the estimator agent
    3. Combines the results into a complete fitness plan
    4. Optionally stores the plan in the database for the user

    Args:
        user_input: User's fitness data and dietary preferences
        db: Optional database session for storing results
        user_id: Optional user ID for associating plans with a user

    Returns:
        CoachResult: Complete fitness plan with workout schedule, diet plan, and goal estimate
    """
    # Step 1: Generate workout and diet recommendations using the coach agent
    coach_run = await gpt03_agent.run(deps=user_input)
    coach_result = coach_run.output

    # Step 2: Predict how many days until the user reaches their goal using the estimator agent
    estimated_run = await estimator_agent.run(deps=coach_result)
    estimated_days = estimated_run.output

    # Step 3: Combine recommendations with progress estimate to create complete plan
    coach_result.estimated_days_to_goal = estimated_days

    # Step 4: Store the generated plan in the database if db session and user_id are provided
    if db and user_id:
        # Create user plan record with basic information
        db_plan = UserPlan(
            user_id=user_id,                                # Link plan to specific user
            current_weight=user_input.current_weight,       # Store starting weight
            weight_goal=user_input.weight_goal,             # Store target weight
            workout_frequency=user_input.workout_frequency, # Store workout frequency
            estimated_days_to_goal=estimated_days           # Store time estimate
        )
        db.add(db_plan)
        db.flush()  # Get plan ID without committing transaction yet

        # Store each day's workout plan in the database
        for workout in coach_result.workout_plan:
            db_workout = DBWorkoutPlan(
                user_plan_id=db_plan.id,  # Link to parent plan
                day=workout.day,          # Day of the week
                activity=workout.activity # Workout details
            )
            db.add(db_workout)

        # Store each day's diet plan in the database
        for diet in coach_result.diet_plan:
            db_diet = DBDietPlan(
                user_plan_id=db_plan.id,  # Link to parent plan
                day=diet.day,             # Day of the week
                meals=diet.meals          # Meal details
            )
            db.add(db_diet)

        # Commit all changes to the database in a single transaction
        db.commit()

    # Return the complete fitness plan to the caller
    return coach_result
