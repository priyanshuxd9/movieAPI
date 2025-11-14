from sqlalchemy import Column, String, Numeric
from .database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    # 1. Changed to String(50) and marked as primary_key.
    #    SQLAlchemy requires a primary key, so we'll make this it.
    id = Column(String(50), primary_key=True, index=True)
    
    # 2. Matched your DB's length of 24
    title = Column(String(24))
    
    # 3. This one was already correct
    genre = Column(String(50))
    
    # 4. Used Numeric for exact precision, matching your DECIMAL(3,1)
    rating = Column(Numeric(3,1))
    
    # 5. This one was correct
    hashed_pass = Column(String(50))