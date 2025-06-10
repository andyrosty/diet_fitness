# AI Integration Documentation

This document explains how AI is integrated into the Fitness And Diet App to generate personalized fitness and diet plans.

## Overview

The Fitness And Diet App uses OpenAI's models to power its AI features. The application implements a two-stage AI pipeline:

1. **Plan Generation (GPT-3.5 Model)**: Generates personalized workout and diet plans based on user input
2. **Progress Estimation (GPT-4o Model)**: Analyzes the generated plans and estimates how long it will take to reach the weight goal

## AI Components

### 1. Fitness Coach Agent (GPT-3.5)

The primary AI agent that generates personalized workout and diet plans based on user preferences and goals.

**Input**: User's fitness data and dietary preferences, including:
- Current weight and weight goal
- Workout frequency preferences
- Typical meals (breakfast, lunch, dinner, snacks)
- Dietary restrictions and preferences
- Favorite meals and comfort foods
- Eating out habits

**Output**: Structured workout and diet plans:
- 7-day workout plan with specific activities for each day
- 7-day culturally sensitive diet plan that respects the user's existing eating habits

**Model**: OpenAI's GPT-3.5 (o3)

### 2. Estimator Agent (GPT-4o)

A secondary AI agent that analyzes the generated fitness plan and predicts how long it will take to reach the weight goal.

**Input**: The generated workout and diet plans

**Output**: Estimated number of days to reach the weight goal

**Model**: OpenAI's GPT-4o

## Implementation Details

The AI integration is implemented in `app/diet_fit_app/service.py` using the Pydantic-AI library, which provides a structured way to define AI agents and their inputs/outputs.

### Agent Definitions

```python
# GPT-03 Agent – Primary AI coach that generates workout and diet plans
gpt03_agent = Agent(
    model="o3",                     # Using OpenAI's o3 model
    deps_type=UserInput,            # Input type: User's fitness data
    result_type=CoachResult,        # Output type: Structured plans
    providers=[OpenAIProvider(api_key=OPENAI_API_KEY)],
    system_prompt=(
        "You are a fitness and nutrition AI coach. Based on the user's dietary preferences "
        "(typical meals, restrictions, favorites, and eating habits), "
        "current weight, weight goal, and workout frequency, provide:\n"
        "1. A 7-day workout plan\n"
        "2. A 7-day culturally sensitive diet plan\n"
        "Do not estimate the number of days to reach the goal."
    )
)

# Estimator Agent – Secondary AI that predicts days to goal
estimator_agent = Agent(
    model="gpt-4o",                 # Using GPT-4o for more accurate estimation
    deps_type=CoachResult,          # Input type: The generated fitness plan
    result_type=int,                # Output type: Number of days to reach goal
    providers=[OpenAIProvider(api_key=OPENAI_API_KEY)],
    system_prompt=(
        "You are a health progress analyst AI. Given a workout and diet plan, estimate how many days "
        "it will take the user to reach their weight goal. Consider the user's consistency, frequency, "
        "and intensity of the routine when making the prediction."
    )
)
```

### Pipeline Orchestration

The `run_fitness_pipeline` function orchestrates the complete AI pipeline:

1. Calls the fitness coach agent to generate workout and diet plans
2. Calls the estimator agent to predict days to goal
3. Combines the results into a complete fitness plan
4. Stores the plan in the database (if a database session is provided)

```python
async def run_fitness_pipeline(user_input: UserInput, db: Session = None, user_id: int = None) -> CoachResult:
    # Step 1: Generate workout and diet recommendations
    coach_run = await gpt03_agent.run(deps=user_input)
    coach_result = coach_run.output

    # Step 2: Predict how many days until the user reaches their goal
    estimated_run = await estimator_agent.run(deps=coach_result)
    estimated_days = estimated_run.output

    # Step 3: Combine recommendations with progress estimate
    coach_result.estimated_days_to_goal = estimated_days

    # Step 4: Store the generated plan in the database if needed
    if db and user_id:
        # Database storage logic...

    return coach_result
```

## Data Models

The AI integration uses Pydantic models to ensure type safety and consistent data handling:

- `UserInput`: Represents the user's fitness data and dietary preferences
- `CoachResult`: Represents the generated workout and diet plans, along with the estimated days to goal

## Environment Configuration

The AI integration requires an OpenAI API key, which should be set in the `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Error Handling

The AI pipeline includes error handling to manage potential issues with the OpenAI API, such as rate limiting or service unavailability. Errors are caught and appropriate HTTP exceptions are raised with descriptive messages.

## Extending the AI Integration

To extend the AI integration with new features:

1. Define new Pydantic models for the input and output data
2. Create a new Agent with appropriate model, dependencies, and system prompt
3. Implement any necessary context generators or tool functions
4. Update the pipeline orchestration function to include the new agent

## Performance Considerations

- The AI pipeline makes asynchronous calls to the OpenAI API, allowing for non-blocking operation
- The GPT-3.5 model is used for plan generation to balance quality and cost
- The GPT-4o model is used for progress estimation to provide more accurate predictions