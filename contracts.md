# Netflix Clone - Backend Integration Contracts

## Current Mock Data Location
- **File**: `/app/frontend/src/data/mock.js`
- **Usage**: Currently provides static movie data for all categories
- **To Replace**: Will be replaced with real TMDB API data

## API Contracts

### 1. Movies Endpoints

#### GET /api/movies/trending
- **Purpose**: Fetch trending movies/shows
- **Response**: Array of movie objects
- **Current Mock**: `mockData.categories.trending`

#### GET /api/movies/popular
- **Purpose**: Fetch popular movies/shows
- **Response**: Array of movie objects
- **Current Mock**: `mockData.categories.popular`

#### GET /api/movies/category/{category}
- **Purpose**: Fetch movies by category (action, comedy, horror, documentaries)
- **Parameters**: category (string)
- **Response**: Array of movie objects
- **Current Mock**: `mockData.categories[category]`

#### GET /api/movies/search?q={query}
- **Purpose**: Search movies by title
- **Parameters**: q (string) - search query
- **Response**: Array of movie objects

#### GET /api/movies/{id}/trailer
- **Purpose**: Get trailer URL for a specific movie
- **Parameters**: id (number) - movie ID
- **Response**: Trailer URL object

### 2. Movie Data Structure
```json
{
  "id": "number",
  "title": "string",
  "image": "string", // Poster URL
  "backdropImage": "string", // Backdrop URL
  "description": "string",
  "year": "string",
  "duration": "string",
  "rating": "string",
  "genre": "string",
  "trailerUrl": "string" // YouTube URL
}
```

## TMDB API Integration Plan

### 1. API Configuration
- **Base URL**: `https://api.themoviedb.org/3`
- **Image Base URL**: `https://image.tmdb.org/t/p/w500` (posters), `https://image.tmdb.org/t/p/original` (backdrops)
- **API Keys**: Use provided keys with rotation for rate limiting
  - `c8dea14dc917687ac631a52620e4f7ad`
  - `3cb41ecea3bf606c56552db3d17adefd`

### 2. TMDB Endpoints to Use
- **Trending**: `/trending/all/day`
- **Popular Movies**: `/movie/popular`
- **Popular TV**: `/tv/popular`
- **Genre Lists**: `/genre/movie/list`, `/genre/tv/list`
- **Movies by Genre**: `/discover/movie?with_genres={genre_id}`
- **Movie Details**: `/movie/{id}`
- **TV Details**: `/tv/{id}`
- **Videos/Trailers**: `/movie/{id}/videos`, `/tv/{id}/videos`
- **Search**: `/search/multi?query={query}`

### 3. Data Transformation
- Convert TMDB response format to our movie data structure
- Handle both movie and TV show data types
- Filter trailers to get YouTube URLs only
- Implement image URL construction with proper sizing

## Frontend Integration Changes

### 1. Replace Mock Data
- Remove static imports from `mock.js`
- Replace with API calls using axios
- Add loading states for movie rows
- Implement error handling for failed requests

### 2. Updated Component Files
- **Browse.jsx**: Add useEffect hooks to fetch data from API endpoints
- **MovieRow.jsx**: Add loading states and error handling
- **TrailerModal.jsx**: No changes needed (already handles YouTube URLs)

### 3. New API Service
- **File**: `/app/frontend/src/services/api.js`
- **Purpose**: Centralized API service for all movie-related requests
- **Features**: Request caching, error handling, loading states

## Backend Implementation Plan

### 1. Dependencies to Add
```
requests>=2.31.0  # For TMDB API calls
python-dotenv>=1.0.1  # Already present
```

### 2. Environment Variables
- `TMDB_API_KEY`: Store in backend/.env
- `TMDB_BASE_URL`: Store base URL configuration

### 3. Backend Files to Create/Update
- **models/movie.py**: Pydantic models for movie data
- **services/tmdb_service.py**: TMDB API integration service
- **routers/movies.py**: Movie-related endpoints
- **server.py**: Include movie router

### 4. Error Handling
- Rate limiting handling with API key rotation
- Fallback to cached data if TMDB is unavailable
- Image URL validation and fallback images
- Proper HTTP status codes and error messages

## Testing Strategy
1. Test all TMDB API endpoints with both API keys
2. Verify trailer URL extraction and YouTube integration
3. Test search functionality with various queries
4. Validate image loading and fallback behavior
5. Test frontend integration with loading states

## Performance Optimizations
1. Implement response caching for popular endpoints
2. Image lazy loading in frontend
3. Pagination for large result sets
4. Rate limiting compliance with TMDB API