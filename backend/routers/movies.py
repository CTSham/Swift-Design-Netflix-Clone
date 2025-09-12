from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.tmdb_service import TMDBService
from models.movie import Movie, MovieResponse, TrailerResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
tmdb_service = TMDBService()

@router.get("/movies/trending", response_model=MovieResponse)
async def get_trending_movies(page: int = Query(1, ge=1, le=500)):
    """Get trending movies and TV shows"""
    try:
        movies = tmdb_service.get_trending_movies(page)
        return MovieResponse(success=True, data=movies, total=len(movies))
    except Exception as e:
        logger.error(f"Error fetching trending movies: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch trending movies")

@router.get("/movies/popular", response_model=MovieResponse)
async def get_popular_movies(page: int = Query(1, ge=1, le=500)):
    """Get popular movies"""
    try:
        movies = tmdb_service.get_popular_movies(page)
        return MovieResponse(success=True, data=movies, total=len(movies))
    except Exception as e:
        logger.error(f"Error fetching popular movies: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch popular movies")

@router.get("/movies/popular-tv", response_model=MovieResponse)
async def get_popular_tv_shows(page: int = Query(1, ge=1, le=500)):
    """Get popular TV shows"""
    try:
        movies = tmdb_service.get_popular_tv_shows(page)
        return MovieResponse(success=True, data=movies, total=len(movies))
    except Exception as e:
        logger.error(f"Error fetching popular TV shows: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch popular TV shows")

@router.get("/movies/category/{category}", response_model=MovieResponse)
async def get_movies_by_category(
    category: str,
    page: int = Query(1, ge=1, le=500)
):
    """Get movies by category (action, comedy, horror, documentaries, etc.)"""
    try:
        movies = tmdb_service.get_genre_movies(category)
        return MovieResponse(success=True, data=movies, total=len(movies))
    except Exception as e:
        logger.error(f"Error fetching movies for category {category}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch {category} movies")

@router.get("/movies/search", response_model=MovieResponse)
async def search_movies(
    q: str = Query(..., min_length=1, description="Search query"),
    page: int = Query(1, ge=1, le=500)
):
    """Search for movies and TV shows"""
    try:
        movies = tmdb_service.search_movies(q, page)
        return MovieResponse(success=True, data=movies, total=len(movies))
    except Exception as e:
        logger.error(f"Error searching movies with query '{q}': {e}")
        raise HTTPException(status_code=500, detail="Failed to search movies")

@router.get("/movies/{movie_id}/trailer", response_model=TrailerResponse)
async def get_movie_trailer(
    movie_id: int,
    media_type: str = Query("movie", description="Media type: movie or tv")
):
    """Get trailer URL for a specific movie or TV show"""
    try:
        trailer_url = tmdb_service.get_movie_trailer(movie_id, media_type)
        
        if trailer_url:
            return TrailerResponse(success=True, trailer_url=trailer_url)
        else:
            return TrailerResponse(
                success=False, 
                message="No trailer available for this title"
            )
            
    except Exception as e:
        logger.error(f"Error fetching trailer for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch movie trailer")

# Additional endpoint for Netflix-style mixed categories
@router.get("/movies/netflix-style", response_model=dict)
async def get_netflix_style_data():
    """Get all categories in Netflix-style format"""
    try:
        result = {
            "trending": tmdb_service.get_trending_movies()[:20],
            "popular": tmdb_service.get_popular_movies()[:20],
            "action": tmdb_service.get_genre_movies('action')[:20],
            "comedy": tmdb_service.get_genre_movies('comedy')[:20],
            "horror": tmdb_service.get_genre_movies('horror')[:20],
            "documentaries": tmdb_service.get_genre_movies('documentaries')[:20],
        }
        
        return {
            "success": True,
            "categories": result
        }
        
    except Exception as e:
        logger.error(f"Error fetching Netflix-style data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch movie categories")