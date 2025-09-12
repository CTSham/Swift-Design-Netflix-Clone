import requests
import os
import logging
from typing import List, Dict, Optional, Union
from models.movie import Movie
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)

class TMDBService:
    def __init__(self):
        # Load environment variables
        ROOT_DIR = Path(__file__).parent.parent
        load_dotenv(ROOT_DIR / '.env')
        
        self.api_keys = [
            os.environ.get('TMDB_API_KEY'),
            os.environ.get('TMDB_API_KEY_2')
        ]
        self.base_url = os.environ.get('TMDB_BASE_URL', 'https://api.themoviedb.org/3')
        self.image_base_url = os.environ.get('TMDB_IMAGE_BASE_URL', 'https://image.tmdb.org/t/p/w500')
        self.backdrop_base_url = os.environ.get('TMDB_BACKDROP_BASE_URL', 'https://image.tmdb.org/t/p/original')
        self.current_key_index = 0

    def _get_current_api_key(self) -> str:
        return self.api_keys[self.current_key_index]

    def _rotate_api_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        logger.info(f"Rotated to API key index: {self.current_key_index}")

    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make request to TMDB API with key rotation on rate limit"""
        if params is None:
            params = {}
        
        params['api_key'] = self._get_current_api_key()
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 429:  # Rate limited
                logger.warning("Rate limited, rotating API key...")
                self._rotate_api_key()
                params['api_key'] = self._get_current_api_key()
                response = requests.get(url, params=params, timeout=10)
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"TMDB API request failed: {e}")
            return None

    def _transform_movie(self, item: Dict) -> Movie:
        """Transform TMDB API response to Movie model"""
        media_type = item.get('media_type', 'movie')
        
        # Handle both movie and TV show data
        title = item.get('title') or item.get('name', 'Unknown Title')
        release_date = item.get('release_date') or item.get('first_air_date', '')
        year = release_date.split('-')[0] if release_date else 'Unknown'
        
        # Get poster and backdrop images
        poster_path = item.get('poster_path', '')
        backdrop_path = item.get('backdrop_path', '')
        
        image_url = f"{self.image_base_url}{poster_path}" if poster_path else "https://via.placeholder.com/500x750/333/fff?text=No+Image"
        backdrop_url = f"{self.backdrop_base_url}{backdrop_path}" if backdrop_path else "https://via.placeholder.com/1920x1080/333/fff?text=No+Image"
        
        # Generate duration based on media type
        if media_type == 'tv':
            duration = f"{item.get('episode_run_time', [45])[0] if item.get('episode_run_time') else 45} min"
        else:
            duration = f"{item.get('runtime', 120)} min"
        
        # Generate rating from vote_average
        vote_average = item.get('vote_average', 0)
        if vote_average >= 8.0:
            rating = "TV-MA" if media_type == 'tv' else "R"
        elif vote_average >= 6.0:
            rating = "TV-14" if media_type == 'tv' else "PG-13"
        else:
            rating = "TV-PG" if media_type == 'tv' else "PG"
        
        return Movie(
            id=item['id'],
            title=title,
            image=image_url,
            backdrop_image=backdrop_url,
            description=item.get('overview', 'No description available.'),
            year=year,
            duration=duration,
            rating=rating,
            genre=self._get_first_genre(item.get('genre_ids', [])),
            tmdb_id=item['id'],
            media_type=media_type
        )

    def _get_first_genre(self, genre_ids: List[int]) -> str:
        """Convert genre IDs to genre names"""
        genre_map = {
            28: "Action", 35: "Comedy", 18: "Drama", 27: "Horror",
            878: "Sci-Fi", 53: "Thriller", 10749: "Romance", 99: "Documentary",
            16: "Animation", 14: "Fantasy", 80: "Crime", 9648: "Mystery",
            10751: "Family", 36: "History", 10402: "Music", 37: "Western"
        }
        
        if not genre_ids:
            return "General"
        
        return genre_map.get(genre_ids[0], "General")

    def get_trending_movies(self, page: int = 1) -> List[Movie]:
        """Get trending movies and TV shows"""
        data = self._make_request('/trending/all/day', {'page': page})
        if not data:
            return []
        
        return [self._transform_movie(item) for item in data.get('results', [])]

    def get_popular_movies(self, page: int = 1) -> List[Movie]:
        """Get popular movies"""
        data = self._make_request('/movie/popular', {'page': page})
        if not data:
            return []
        
        movies = [dict(item, media_type='movie') for item in data.get('results', [])]
        return [self._transform_movie(item) for item in movies]

    def get_popular_tv_shows(self, page: int = 1) -> List[Movie]:
        """Get popular TV shows"""
        data = self._make_request('/tv/popular', {'page': page})
        if not data:
            return []
        
        tv_shows = [dict(item, media_type='tv') for item in data.get('results', [])]
        return [self._transform_movie(item) for item in tv_shows]

    def get_movies_by_genre(self, genre_id: int, media_type: str = 'movie', page: int = 1) -> List[Movie]:
        """Get movies or TV shows by genre"""
        endpoint = f'/{media_type}/popular' if media_type in ['movie', 'tv'] else '/movie/popular'
        params = {'page': page, 'with_genres': genre_id}
        
        if media_type == 'movie':
            endpoint = '/discover/movie'
        elif media_type == 'tv':
            endpoint = '/discover/tv'
        
        data = self._make_request(endpoint, params)
        if not data:
            return []
        
        items = [dict(item, media_type=media_type) for item in data.get('results', [])]
        return [self._transform_movie(item) for item in items]

    def search_movies(self, query: str, page: int = 1) -> List[Movie]:
        """Search for movies and TV shows"""
        data = self._make_request('/search/multi', {'query': query, 'page': page})
        if not data:
            return []
        
        # Filter only movie and TV results
        results = [item for item in data.get('results', []) if item.get('media_type') in ['movie', 'tv']]
        return [self._transform_movie(item) for item in results]

    def get_movie_trailer(self, movie_id: int, media_type: str = 'movie') -> Optional[str]:
        """Get YouTube trailer URL for a movie or TV show"""
        endpoint = f'/{media_type}/{movie_id}/videos'
        data = self._make_request(endpoint)
        
        if not data:
            return None
        
        # Look for YouTube trailers
        videos = data.get('results', [])
        for video in videos:
            if video.get('site') == 'YouTube' and video.get('type') in ['Trailer', 'Teaser']:
                return f"https://www.youtube.com/watch?v={video['key']}"
        
        return None

    def get_genre_movies(self, category: str) -> List[Movie]:
        """Get movies by category name"""
        category_genre_map = {
            'action': 28,
            'comedy': 35,
            'horror': 27,
            'documentaries': 99,
            'romance': 10749,
            'thriller': 53,
            'sci-fi': 878,
            'drama': 18
        }
        
        genre_id = category_genre_map.get(category.lower())
        if not genre_id:
            return []
        
        # Mix of movies and TV shows for variety
        movies = self.get_movies_by_genre(genre_id, 'movie')[:10]
        tv_shows = self.get_movies_by_genre(genre_id, 'tv')[:5]
        
        return movies + tv_shows