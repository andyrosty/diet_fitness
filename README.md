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
   git clone https://github.com/yourusername/diet_fitness.git
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

## How It Works

The application uses a two-stage AI pipeline to generate personalized fitness and diet plans:

1. **Plan Generation**: The first stage uses OpenAI's GPT-4o model to analyze the user's dietary preferences, current weight, weight goal, and workout frequency to create a 7-day workout plan and a 7-day culturally sensitive diet plan.

2. **Progress Estimation**: The second stage uses another GPT-4o model to analyze the generated plans and estimate how many days it will take for the user to reach their weight goal, considering the user's consistency, frequency, and intensity of the routine.

The AI models are integrated using the Pydantic-AI library, which provides a structured way to define AI agents and their inputs/outputs.

## Dependencies

- FastAPI: Web framework for building APIs
- Uvicorn: ASGI server for running FastAPI
- Pydantic: Data validation and settings management
- Pydantic-AI: Extension for AI model integration
- Python-dotenv: Environment variable management
- OpenAI: AI model provider
- Google Generative AI: Alternative AI model provider
- HTTPX: HTTP client for async requests

## Example Request

```json
{
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
```


## Screenshots

The application includes a user-friendly interface for submitting information and viewing personalized plans:

![Screenshot 1](Screenshots/screenshot1.png)
![Screenshot 2](Screenshots/screenshot2.png)
![Screenshot 3](Screenshots/screenshot3.png)

## License

MIT License

Copyright (c) 2025 Diet Fitness App

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
