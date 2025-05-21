"""service.py: Core pipeline for generating fitness and diet plans and estimating progress using AI agents."""
import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers.openai import OpenAIProvider
from app.diet_fit_app.models import UserInput, CoachResult

# Load OpenAI API key for AI providers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# GPT-4o Agent – generates workout and diet plans based on user input
gpt4o_agent = Agent(
    model="gpt-4o",
    deps_type=UserInput,
    result_type=CoachResult,
    providers=[OpenAIProvider(api_key=OPENAI_API_KEY)],
    system_prompt=(
        "You are a fitness and nutrition AI coach. Based on the user's weekly meals, "
        "current weight, weight goal, and workout frequency, provide:\n"
        "1. A 7-day workout plan\n"
        "2. A 7-day culturally sensitive diet plan\n"
        "Do not estimate the number of days to reach the goal."
    )
)


@gpt4o_agent.system_prompt
async def gpt4o_context(ctx: RunContext[UserInput]):
    # Inject dynamic user context into the system prompt
    user = ctx.deps
    return f"The user weighs {user.current_weight}, wants to {user.weight_goal}, and works out {user.workout_frequency}."


"""Estimator Agent – predicts days to goal from the generated CoachResult"""
estimator_agent = Agent(
    model="gpt-4o",
    deps_type=CoachResult,
    result_type=int,
    providers=[OpenAIProvider(api_key=OPENAI_API_KEY)],
    system_prompt=(
        "You are a health progress analyst AI. Given a workout and diet plan, estimate how many days "
        "it will take the user to reach their weight goal. Consider the user's consistency, frequency, "
        "and intensity of the routine when making the prediction."
    )
)


@estimator_agent.tool
async def estimate_days_to_goal(ctx: RunContext[CoachResult],result: CoachResult) -> int:
    """
    Estimate how many days it will take for the user to reach their weight goal
    based on their workout and diet plan.
    """
    return 0  # Estimator will generate this dynamically


async def run_fitness_pipeline(user_input: UserInput) -> CoachResult:
    """
    Orchestrates the fitness and diet planning pipeline:
    1. Generate a 7-day workout plan and 7-day diet plan via gpt4o_agent
    2. Estimate days to reach weight goal via estimator_agent
    3. Attach estimate and return CoachResult
    """
    # Step 1: Generate workout and diet recommendations
    coach_run = await gpt4o_agent.run(deps=user_input)
    coach_result = coach_run.output

    # Step 2: Predict how many days until the user reaches their goal
    estimated_run = await estimator_agent.run(deps=coach_result)
    estimated_days = estimated_run.output

    # Step 3: Combine recommendations with progress estimate
    coach_result.estimated_days_to_goal = estimated_days
    return coach_result
