from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

# Database models for the Diet and Fitness application

class User(Base):
    """
    User model representing application users.

    Stores user authentication information and links to their fitness plans.
    """
    __tablename__ = "users"

    # Primary user identification and authentication fields
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Unique username for login
    email = Column(String, unique=True, index=True)     # Unique email for communication
    hashed_password = Column(String)                    # Securely stored password (hashed)
    is_active = Column(Boolean, default=True)           # Flag to indicate if account is active
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Account creation timestamp

    # Relationship to user's fitness plans
    plans = relationship("UserPlan", back_populates="user", cascade="all, delete-orphan")

class UserPlan(Base):
    """
    UserPlan model representing a user's fitness plan.

    Contains weight goals, workout frequency, and links to specific workout and diet plans.
    """
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))           # Link to the user who owns this plan
    current_weight = Column(String)                             # User's current weight
    weight_goal = Column(String)                                # User's target weight
    workout_frequency = Column(String)                          # How often user plans to workout
    estimated_days_to_goal = Column(Integer)                    # Estimated time to reach weight goal
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Plan creation timestamp

    # Relationships to related models
    user = relationship("User", back_populates="plans")         # Link back to user
    workout_plans = relationship("WorkoutPlan", back_populates="user_plan", cascade="all, delete-orphan")  # Workout schedule
    diet_plans = relationship("DietPlan", back_populates="user_plan", cascade="all, delete-orphan")        # Diet schedule

class WorkoutPlan(Base):
    """
    WorkoutPlan model representing daily workout activities.

    Contains specific workout activities for each day of the week.
    """
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_plan_id = Column(Integer, ForeignKey("user_plans.id"))  # Link to the parent user plan
    day = Column(String)                                         # Day of the week for this workout
    activity = Column(Text)                                      # Detailed workout description

    # Relationship back to the parent plan
    user_plan = relationship("UserPlan", back_populates="workout_plans")

class DietPlan(Base):
    """
    DietPlan model representing daily meal plans.

    Contains specific meal recommendations for each day of the week.
    """
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_plan_id = Column(Integer, ForeignKey("user_plans.id"))  # Link to the parent user plan
    day = Column(String)                                         # Day of the week for this meal plan
    meals = Column(Text)                                         # Detailed meal descriptions

    # Relationship back to the parent plan
    user_plan = relationship("UserPlan", back_populates="diet_plans")
