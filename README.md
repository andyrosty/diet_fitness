# Fitness And Diet App

A FastAPI application that generates personalized fitness and diet plans using AI. The app analyzes a user's current eating habits, weight goals, and workout preferences to create customized 7-day workout and diet plans, along with an estimate of how long it will take to reach their weight goal.

## Features

- **Personalized Workout Plans**: Generate 7-day workout schedules based on user preferences
- **Culturally Sensitive Diet Plans**: Create 7-day meal plans that respect the user's current eating habits
- **Progress Estimation**: Predict how many days it will take to reach weight goals
- **AI-Powered**: Utilizes OpenAI's GPT-4o model for intelligent recommendations

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd diet_fitness
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the API documentation at `http://localhost:8000/docs`

3. Use the `/fitness-plan` endpoint to submit your information and receive a personalized plan:
   - Weekly meals for each day
   - Current weight
   - Weight goal
   - Workout frequency

## API Endpoints

- **POST /fitness-plan**: Submit user information and receive a personalized fitness and diet plan

## Project Structure

```
diet_fitness/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   └── diet_fit_app/
│       ├── __init__.py
│       ├── controller.py        # API endpoints definition
│       ├── models.py            # Pydantic data models
│       └── service.py           # Business logic and AI integration
├── requirements.txt             # Project dependencies
├── test_app.py                  # Basic app import test
└── README.md                    # Project documentation
```

## Dependencies

- FastAPI: Web framework for building APIs
- Uvicorn: ASGI server for running FastAPI
- Pydantic: Data validation and settings management
- Pydantic-AI: Extension for AI model integration
- Python-dotenv: Environment variable management
- OpenAI: AI model provider
- HTTPX: HTTP client for async requests

## Example Request(Ghanian Diet)

```json
{
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
```

