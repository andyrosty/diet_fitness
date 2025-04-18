import os
from pydantic_ai import Agent, RunContext
from pydantic_ai.providers import GoogleGLAProvider
from app.diet_fit_app.models import UserInput, CoachResult

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# GPT-4o Agent – Handles workout + diet generation
gpt4o_agent = Agent(
    model="gpt-4o",
    deps_type=UserInput,
    result_type=CoachResult,
    system_prompt=(
        "You are a fitness and nutrition AI coach. Based on the user's weekly meals, "
        "current weight, weight goal, and workout frequency, provide:\n"
        "1. A 7-day workout plan\n"
        "2. A 3-day culturally sensitive diet plan\n"
        "Do not estimate the number of days to reach the goal."
    )
)


@gpt4o_agent.system_prompt
async def gpt4o_context(ctx: RunContext[UserInput]):
    user = ctx.input
    return f"The user weighs {user.current_weight}, wants to {user.weight_goal}, and works out {user.workout_frequency}."


# Gemini Agent – Tool to estimate time-to-goal from the result of GPT-4o
gemini_agent = Agent(
    model="gemini-2.0-flash",
    deps_type=CoachResult,
    result_type=int,
    system_prompt=(
        "You are a health progress analyst AI. Given a workout and diet plan, estimate how many days "
        "it will take the user to reach their weight goal. Consider the user's consistency, frequency, "
        "and intensity of the routine when making the prediction."
    )
)


@gemini_agent.tool
async def estimate_days_to_goal(ctx: RunContext[CoachResult],result: CoachResult) -> int:
    """
    Estimate how many days it will take for the user to reach their weight goal
    based on their workout and diet plan.
    """
    return 0  # Gemini will generate this dynamically


# Pipeline function – Connect GPT-4o → Gemini → Final response
async def run_fitness_pipeline(user_input: UserInput) -> CoachResult:
    # Step 1: Get workout + diet plan from GPT-4o
    coach_result = await gpt4o_agent.run(user_input)

    # Step 2: Estimate days to reach goal using Gemini
    estimated_days = await estimate_days_to_goal(coach_result)

    # Step 3: Attach Gemini's result and return full package
    coach_result.estimated_days_to_goal = estimated_days
    return coach_result

