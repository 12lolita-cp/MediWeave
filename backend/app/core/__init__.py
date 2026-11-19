#Marks the directory as a Python package.
#.env	Stores database credentials and environment-specific settings
'''Our FastAPI backend receives this information.

Eventually, we need to store it in our PostgreSQL database.

But how does Python communicate with PostgreSQL?

Through a database driver such as Psycopg.'''
'''| Component | Responsibility |
|---|---|
| FastAPI | Handles HTTP requests and API endpoints |
| SQLAlchemy | Provides ORM and database interaction tools |
| Psycopg | Python driver that communicates with PostgreSQL |
| PostgreSQL | Stores and manages the data |'''