
# Implementation Plan for User Authentication and Database Integration

## Overview
This plan outlines the steps to add user authentication (login/signup with JWT) and PostgreSQL database integration to the Fitness And Diet App. The implementation will allow storing generated diet plans, workout plans, and estimated completion days.

## 1. Database Setup

### Task 1.1: Configure PostgreSQL
- Install PostgreSQL if not already installed
- Create a new database named `diet_fitness_db`
- Add database connection string to `.env` file:
  ```
  DATABASE_URL=postgresql://username:password@localhost/diet_fitness_db
  ```

### Task 1.2: Set Up SQLAlchemy ORM
- Install required packages:
  ```
  pip install sqlalchemy psycopg2-binary alembic
  ```
- Update `requirements.txt` with new dependencies
- Create database connection module in `app/db/database.py`:
  ```python
  from sqlalchemy import create_engine
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import sessionmaker
  import os
  
  DATABASE_URL = os.getenv("DATABASE_URL")
  
  engine = create_engine(DATABASE_URL)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  Base = declarative_base()
  
  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
  ```

### Task 1.3: Initialize Alembic for Migrations
- Set up Alembic for database migrations:
  ```
  alembic init migrations
  ```
- Configure Alembic to use SQLAlchemy models

## 2. Database Models

### Task 2.1: Create User Model
- Create `app/db/models.py` with User model:
  ```python
  from sqlalchemy import Column, Integer, String, Boolean, DateTime
  from sqlalchemy.sql import func
  from app.db.database import Base
  
  class User(Base):
      __tablename__ = "users"
      
      id = Column(Integer, primary_key=True, index=True)
      username = Column(String, unique=True, index=True)
      email = Column(String, unique=True, index=True)
      hashed_password = Column(String)
      is_active = Column(Boolean, default=True)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
  ```

### Task 2.2: Create Plan Storage Models
- Add models for storing generated plans:
  ```python
  from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
  from sqlalchemy.orm import relationship
  from sqlalchemy.sql import func
  
  class UserPlan(Base):
      __tablename__ = "user_plans"
      
      id = Column(Integer, primary_key=True, index=True)
      user_id = Column(Integer, ForeignKey("users.id"))
      current_weight = Column(String)
      weight_goal = Column(String)
      workout_frequency = Column(String)
      estimated_days_to_goal = Column(Integer)
      created_at = Column(DateTime(timezone=True), server_default=func.now())
      
      user = relationship("User", back_populates="plans")
      workout_plans = relationship("WorkoutPlan", back_populates="user_plan", cascade="all, delete-orphan")
      diet_plans = relationship("DietPlan", back_populates="user_plan", cascade="all, delete-orphan")
  
  class WorkoutPlan(Base):
      __tablename__ = "workout_plans"
      
      id = Column(Integer, primary_key=True, index=True)
      user_plan_id = Column(Integer, ForeignKey("user_plans.id"))
      day = Column(String)
      activity = Column(Text)
      
      user_plan = relationship("UserPlan", back_populates="workout_plans")
  
  class DietPlan(Base):
      __tablename__ = "diet_plans"
      
      id = Column(Integer, primary_key=True, index=True)
      user_plan_id = Column(Integer, ForeignKey("user_plans.id"))
      day = Column(String)
      meals = Column(Text)
      
      user_plan = relationship("UserPlan", back_populates="diet_plans")
  ```

### Task 2.3: Update User Model with Relationships
- Add relationship to User model:
  ```python
  # Add to User class
  plans = relationship("UserPlan", back_populates="user", cascade="all, delete-orphan")
  ```

## 3. Authentication Implementation

### Task 3.1: Password Hashing Utilities
- Create `app/auth/utils.py`:
  ```python
  from passlib.context import CryptContext
  
  pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  def verify_password(plain_password, hashed_password):
      return pwd_context.verify(plain_password, hashed_password)
  
  def get_password_hash(password):
      return pwd_context.hash(password)
  ```

### Task 3.2: JWT Token Handling
- Create `app/auth/token.py`:
  ```python
  from datetime import datetime, timedelta
  from jose import JWTError, jwt
  from fastapi import Depends, HTTPException, status
  from fastapi.security import OAuth2PasswordBearer
  import os
  
  # Configuration
  SECRET_KEY = os.getenv("JWT_SECRET_KEY")
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
  
  def create_access_token(data: dict):
      to_encode = data.copy()
      expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt
  
  def verify_token(token: str):
      try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          username: str = payload.get("sub")
          if username is None:
              return None
          return username
      except JWTError:
          return None
  ```

### Task 3.3: Authentication Schemas
- Create `app/auth/schemas.py`:
  ```python
  from pydantic import BaseModel, EmailStr
  
  class UserCreate(BaseModel):
      username: str
      email: EmailStr
      password: str
  
  class UserLogin(BaseModel):
      username: str
      password: str
  
  class Token(BaseModel):
      access_token: str
      token_type: str
  
  class UserResponse(BaseModel):
      id: int
      username: str
      email: EmailStr
      
      class Config:
          orm_mode = True
  ```

### Task 3.4: Authentication Controller
- Create `app/auth/controller.py`:
  ```python
  from fastapi import APIRouter, Depends, HTTPException, status
  from fastapi.security import OAuth2PasswordRequestForm
  from sqlalchemy.orm import Session
  
  from app.db.database import get_db
  from app.db.models import User
  from app.auth.schemas import UserCreate, Token, UserResponse
  from app.auth.utils import get_password_hash, verify_password
  from app.auth.token import create_access_token
  
  router = APIRouter(tags=["Authentication"])
  
  @router.post("/signup", response_model=UserResponse)
  def signup(user: UserCreate, db: Session = Depends(get_db)):
      # Check if username exists
      db_user = db.query(User).filter(User.username == user.username).first()
      if db_user:
          raise HTTPException(status_code=400, detail="Username already registered")
      
      # Check if email exists
      db_user = db.query(User).filter(User.email == user.email).first()
      if db_user:
          raise HTTPException(status_code=400, detail="Email already registered")
      
      # Create new user
      hashed_password = get_password_hash(user.password)
      db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
      db.add(db_user)
      db.commit()
      db.refresh(db_user)
      return db_user
  
  @router.post("/login", response_model=Token)
  def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
      user = db.query(User).filter(User.username == form_data.username).first()
      if not user or not verify_password(form_data.password, user.hashed_password):
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Incorrect username or password",
              headers={"WWW-Authenticate": "Bearer"},
          )
      
      access_token = create_access_token(data={"sub": user.username})
      return {"access_token": access_token, "token_type": "bearer"}
  ```

### Task 3.5: Authentication Middleware
- Create `app/auth/dependencies.py`:
  ```python
  from fastapi import Depends, HTTPException, status
  from fastapi.security import OAuth2PasswordBearer
  from sqlalchemy.orm import Session
  
  from app.db.database import get_db
  from app.db.models import User
  from app.auth.token import verify_token
  
  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
  
  def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
      username = verify_token(token)
      if username is None:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid authentication credentials",
              headers={"WWW-Authenticate": "Bearer"},
          )
      
      user = db.query(User).filter(User.username == username).first()
      if user is None:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="User not found",
              headers={"WWW-Authenticate": "Bearer"},
          )
      
      return user
  ```

## 4. Service Layer Updates

### Task 4.1: Update Service to Store Plans
- Modify `app/diet_fit_app/service.py` to store generated plans:
  ```python
  # Add to imports
  from sqlalchemy.orm import Session
  from app.db.models import UserPlan, WorkoutPlan as DBWorkoutPlan, DietPlan as DBDietPlan
  
  # Update run_fitness_pipeline function
  async def run_fitness_pipeline(user_input: UserInput, db: Session = None, user_id: int = None):
      """
      Orchestrates the fitness and diet planning pipeline and stores results if db is provided
      """
      # Generate plans (existing code)
      coach_run = await gpt03_agent.run(deps=user_input)
      coach_result = coach_run.output
      
      estimated_run = await estimator_agent.run(deps=coach_result)
      estimated_days = estimated_run.output
      
      coach_result.estimated_days_to_goal = estimated_days
      
      # Store in database if db session is provided
      if db and user_id:
          # Create user plan record
          db_plan = UserPlan(
              user_id=user_id,
              current_weight=user_input.current_weight,
              weight_goal=user_input.weight_goal,
              workout_frequency=user_input.workout_frequency,
              estimated_days_to_goal=estimated_days
          )
          db.add(db_plan)
          db.flush()  # Get ID without committing
          
          # Store workout plans
          for workout in coach_result.workout_plan:
              db_workout = DBWorkoutPlan(
                  user_plan_id=db_plan.id,
                  day=workout.day,
                  activity=workout.activity
              )
              db.add(db_workout)
          
          # Store diet plans
          for diet in coach_result.diet_plan:
              db_diet = DBDietPlan(
                  user_plan_id=db_plan.id,
                  day=diet.day,
                  meals=diet.meals
              )
              db.add(db_diet)
          
          db.commit()
      
      return coach_result
  ```

## 5. Controller Updates

### Task 5.1: Update Controller to Use Authentication
- Modify `app/diet_fit_app/controller.py`:
  ```python
  from fastapi import APIRouter, HTTPException, Depends
  from sqlalchemy.orm import Session
  
  from app.diet_fit_app.models import UserInput, CoachResult
  from app.diet_fit_app.service import run_fitness_pipeline
  from app.db.database import get_db
  from app.db.models import User
  from app.auth.dependencies import get_current_user
  
  # Router for nutrition and fitness analysis endpoints
  router = APIRouter()
  
  @router.post("/fitness-plan", response_model=CoachResult)
  async def analyze_fitness(
      input_data: UserInput,
      db: Session = Depends(get_db),
      current_user: User = Depends(get_current_user)
  ):
      """
      POST endpoint to generate a fitness and diet plan.
      Requires authentication.
      """
      try:
          # Invoke the service pipeline to get workout, diet, and estimate
          # Also store the results in the database
          result = await run_fitness_pipeline(input_data, db, current_user.id)
          return result
      except Exception as e:
          # Log error and return HTTP 500
          print("Error in analyze_fitness:", e)
          raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
  
  @router.get("/my-plans", response_model=list[CoachResult])
  async def get_user_plans(
      db: Session = Depends(get_db),
      current_user: User = Depends(get_current_user)
  ):
      """
      GET endpoint to retrieve all fitness plans for the current user.
      """
      # Implementation to retrieve and format user plans from the database
      # ...
  ```

### Task 5.2: Add User Plans Endpoint
- Implement the `get_user_plans` function to retrieve stored plans

## 6. Main App Integration

### Task 6.1: Update Main App
- Modify `app/main.py` to include authentication routes:
  ```python
  from fastapi import FastAPI
  from dotenv import load_dotenv
  
  from app.diet_fit_app.controller import router as diet_router
  from app.auth.controller import router as auth_router
  from app.db.database import engine
  from app.db import models
  
  load_dotenv()  # Load environment variables from .env file
  
  # Create database tables
  models.Base.metadata.create_all(bind=engine)
  
  # Initialize FastAPI application
  app = FastAPI(title="Fitness And Diet App")
  
  # Mount API routes
  app.include_router(auth_router, prefix="/auth")
  app.include_router(diet_router, prefix="/api")
  ```

### Task 6.2: Update Environment Variables.
- Add required environment variables to `.env`:
  ```
  OPENAI_API_KEY=your_openai_api_key
  DATABASE_URL=postgresql://username:password@localhost/diet_fitness_db
  JWT_SECRET_KEY=your_secret_key_here
  ```

## 7. Testing

### Task 7.1: Test Authentication
- Test user signup and login endpoints
- Verify JWT token generation and validation

### Task 7.2: Test Plan Storage
- Test storing and retrieving fitness plans
- Verify relationship between users and their plans

## 8. Documentation

### Task 8.1: Update API Documentation
- Update Swagger documentation with new endpoints
- Document authentication requirements

### Task 8.2: Update README
- Update README with new features and setup instructions
- Include information about database setup and authentication

## Required Packages
- SQLAlchemy: ORM for database operations
- Psycopg2: PostgreSQL adapter for Python
- Alembic: Database migration tool
- Passlib: Password hashing library
- Python-jose: JWT token handling
- FastAPI-security: OAuth2 implementation for FastAPI
- Email-validator: Email validation for Pydantic models