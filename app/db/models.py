from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
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
    
    plans = relationship("UserPlan", back_populates="user", cascade="all, delete-orphan")

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