from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Movie(BaseModel):
    id: int
    title: str
    image: str  # Poster URL
    backdrop_image: str  # Backdrop URL
    description: str
    year: str
    duration: str
    rating: str
    genre: str
    trailer_url: Optional[str] = None
    tmdb_id: int
    media_type: str  # "movie" or "tv"

class MovieResponse(BaseModel):
    success: bool
    data: List[Movie]
    total: int

class TrailerResponse(BaseModel):
    success: bool
    trailer_url: Optional[str] = None
    message: Optional[str] = None