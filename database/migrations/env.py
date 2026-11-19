import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context

# Add backend directory to Python's import path
#Our env.py is inside database/migrations, whereas our Python application is inside backend.
#This makes the backend directory available for Python imports
BACKEND_DIR = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import settings
from app.core.database import Base, engine
from app.models import Pharmacy


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Register SQLAlchemy models with Alembic
target_metadata = Base.metadata


def run_migrations_offline():

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():

    with engine.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
            #It tells Alembic to detect changes in column data types when comparing SQLAlchemy models with the existing database schema.
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
    #Does not require a live database connection. It generates SQL migration scripts that can be executed later.
    #context.is_offline_mode() checks if Alembic is running in offline mode, which means it will generate SQL migration scripts without connecting to the database. If it's not in offline mode, it will run migrations online, applying them directly to the database.
    #Creating a migration script in offline mode is useful when you want to review or modify the SQL statements before applying them to the database, or when you don't have direct access to the database at the time of migration.
    
else:
    run_migrations_online()
    #Requires a live database connection. It applies the migrations directly to the database.