from pydantic import BaseModel, condecimal
from decimal import Decimal # Import Decimal for precision

# --- Movie Schemas ---

class MovieBase(BaseModel):
    title: str
    genre: str
    # Use condecimal to match the (3,1) precision
    rating: condecimal(max_digits=3, decimal_places=1)

# This model is used when you CREATE a movie.
# Because id is a String, the user *must* provide it.
class MovieCreate(MovieBase):
    id: str  # <-- This is new!
    hashed_pass: str

# This model is used when you READ a movie.
class MovieRead(MovieBase):
    id: str  # <-- This is now a string, not an int
    
    # This special class tells Pydantic to read data
    # from an SQLAlchemy model object (not just a dict).
    class Config:
        from_attributes = True