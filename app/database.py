from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. We're still pointing to the same SQLite file
DATABASE_URL = "sqlite:///./app/movie_database.db"

# 2. Create the SQLAlchemy "engine"
engine = create_engine(
    DATABASE_URL, 
    # This line is required *only* for SQLite to work with FastAPI
    connect_args={"check_same_thread": False} 
)

# 3. Create a SessionLocal class. Each instance of this
#    class will be a new database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a "Base" class. Our database models
#    (in models.py) will inherit from this class.
Base = declarative_base()

# 5. A helper function (a "dependency") that our API endpoints
#    will use to get a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()