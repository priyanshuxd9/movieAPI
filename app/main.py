from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List # Make sure to import List

# Import all our pieces from the other files in the 'app' folder
from . import models, schemas
from .database import engine, get_db, Base

# This line will now create the table with the correct schema
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()


# --- THIS FUNCTION IS NOW DIFFERENT ---
@app.post("/movies/", response_model=schemas.MovieRead)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie in the database.
    The ID is provided by the user.
    """
    # Check if a movie with this ID already exists
    db_movie_check = db.query(models.Movie).filter(models.Movie.id == movie.id).first()
    if db_movie_check:
        raise HTTPException(status_code=400, detail="Movie with this ID already exists")

    # 1. Convert the Pydantic schema (movie) to an SQLAlchemy model
    #    We now get the 'id' from the user's request
    db_movie = models.Movie(
        id=movie.id,
        title=movie.title,
        genre=movie.genre,
        rating=movie.rating,
        hashed_pass=movie.hashed_pass 
    )
    
    # 2. Add the new movie to the session and commit it
    db.add(db_movie)
    db.commit()
    
    # 3. Refresh the object
    db.refresh(db_movie)
    
    return db_movie

# --- This function also needs the List import ---
@app.get("/movies/", response_model=List[schemas.MovieRead])
def get_all_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of all movies.
    """
    movies = db.query(models.Movie).offset(skip).limit(limit).all()
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.MovieRead)
def get_movie(movie_id: str, db: Session = Depends(get_db)): # <-- id is now a str
    """
    Get a single movie by its ID.
    """
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    # If the movie doesn't exist, return a 404 error
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
        
    return movie

# A welcome endpoint for the root URL
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API! Go to /docs to see the interactive documentation."}