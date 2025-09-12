import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  timeout: 10000,
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`Making request to: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const movieService = {
  // Get trending movies
  getTrending: async (page = 1) => {
    try {
      const response = await apiClient.get(`/movies/trending?page=${page}`);
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching trending movies:', error);
      return [];
    }
  },

  // Get popular movies
  getPopular: async (page = 1) => {
    try {
      const response = await apiClient.get(`/movies/popular?page=${page}`);
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching popular movies:', error);
      return [];
    }
  },

  // Get movies by category
  getByCategory: async (category, page = 1) => {
    try {
      const response = await apiClient.get(`/movies/category/${category}?page=${page}`);
      return response.data.data || [];
    } catch (error) {
      console.error(`Error fetching ${category} movies:`, error);
      return [];
    }
  },

  // Search movies
  search: async (query, page = 1) => {
    try {
      const response = await apiClient.get(`/movies/search?q=${encodeURIComponent(query)}&page=${page}`);
      return response.data.data || [];
    } catch (error) {
      console.error('Error searching movies:', error);
      return [];
    }
  },

  // Get movie trailer
  getTrailer: async (movieId, mediaType = 'movie') => {
    try {
      const response = await apiClient.get(`/movies/${movieId}/trailer?media_type=${mediaType}`);
      return response.data.trailer_url || null;
    } catch (error) {
      console.error('Error fetching trailer:', error);
      return null;
    }
  },

  // Get all Netflix-style categories at once
  getNetflixStyleData: async () => {
    try {
      const response = await apiClient.get('/movies/netflix-style');
      return response.data.categories || {};
    } catch (error) {
      console.error('Error fetching Netflix-style data:', error);
      return {};
    }
  }
};

export default apiClient;