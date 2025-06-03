"""
Alembic migrations environment configuration.

This module configures the Alembic migration environment for the Diet Fitness application.
It handles:
1. Loading database connection details from environment variables
2. Setting up the SQLAlchemy models for migration generation
3. Providing functions for running migrations in both online and offline modes

This configuration ensures that database schema changes can be applied consistently
across different environments (development, testing, production).
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
# Import Base and all models to ensure they're included in Base.metadata
# This is essential for Alembic to detect model changes for migrations
from app.db.models import Base, User, UserPlan, WorkoutPlan, DietPlan
from app.db.database import engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows database configuration to be stored securely outside of code
load_dotenv()

# Load Alembic configuration from alembic.ini
config = context.config

# Override sqlalchemy.url from alembic.ini with the value from environment variables
# This allows different database URLs for different environments without changing the config file
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set or is empty")
config.set_main_option("sqlalchemy.url", database_url)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
