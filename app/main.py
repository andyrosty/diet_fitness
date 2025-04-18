from fastapi import FastAPI
from dotenv import load_dotenv
from app.diet_fit_app.controller import router #Links to the controller

load_dotenv() #Load environment variables

import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") #Get the OpenAI API key from the environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") #Get the Gemini API key from the environment variables

#Title of API app
app = FastAPI(title="Fitness And Diet App")
app.include_router(router)
