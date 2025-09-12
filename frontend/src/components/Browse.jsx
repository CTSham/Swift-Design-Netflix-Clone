import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import Hero from "./Hero";
import MovieRow from "./MovieRow";
import TrailerModal from "./TrailerModal";
import LoadingSpinner from "./LoadingSpinner";
import { movieService } from "../services/api";

const Browse = () => {
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [showTrailer, setShowTrailer] = useState(false);
  const [heroMovie, setHeroMovie] = useState(null);
  const [categories, setCategories] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadMovieData();
  }, []);

  const loadMovieData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch all categories
      const [trending, popular, action, comedy, horror, documentaries] = await Promise.all([
        movieService.getTrending(),
        movieService.getPopular(),
        movieService.getByCategory('action'),
        movieService.getByCategory('comedy'),
        movieService.getByCategory('horror'),
        movieService.getByCategory('documentaries')
      ]);

      const categoriesData = {
        trending,
        popular,
        action,
        comedy,
        horror,
        documentaries
      };

      setCategories(categoriesData);

      // Set random hero movie from trending
      if (trending.length > 0) {
        const randomHero = trending[Math.floor(Math.random() * trending.length)];
        setHeroMovie(randomHero);
      }

    } catch (err) {
      console.error('Error loading movie data:', err);
      setError('Failed to load movies. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handlePlayTrailer = async (movie) => {
    try {
      // Fetch the actual trailer URL from TMDB
      const trailerUrl = await movieService.getTrailer(movie.tmdb_id, movie.media_type);
      
      setSelectedMovie({
        ...movie,
        trailerUrl: trailerUrl
      });
      setShowTrailer(true);
    } catch (error) {
      console.error('Error fetching trailer:', error);
      // Still show modal even without trailer
      setSelectedMovie(movie);
      setShowTrailer(true);
    }
  };

  const closeTrailer = () => {
    setShowTrailer(false);
    setSelectedMovie(null);
  };

  if (loading) {
    return (
      <div className="bg-black min-h-screen">
        <Navbar />
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-black min-h-screen">
        <Navbar />
        <div className="flex items-center justify-center h-screen">
          <div className="text-center">
            <h2 className="text-white text-2xl mb-4">Oops! Something went wrong</h2>
            <p className="text-gray-400 mb-6">{error}</p>
            <button 
              onClick={loadMovieData}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
  <div className="bg-black min-h-screen flex flex-col justify-between">
      <Navbar />
      {heroMovie && <Hero movie={heroMovie} onPlayTrailer={handlePlayTrailer} />}
      
      <div className="relative z-10 -mt-32 space-y-12 pb-20">
        {categories.trending?.length > 0 && (
          <MovieRow 
            title="Trending Now" 
            movies={categories.trending} 
            onPlayTrailer={handlePlayTrailer}
          />
        )}
        
        {categories.popular?.length > 0 && (
          <MovieRow 
            title="Popular on Netflix" 
            movies={categories.popular} 
            onPlayTrailer={handlePlayTrailer}
          />
        )}
        
        {categories.action?.length > 0 && (
          <MovieRow 
            title="Action Movies" 
            movies={categories.action} 
            onPlayTrailer={handlePlayTrailer}
          />
        )}
        
        {categories.comedy?.length > 0 && (
          <MovieRow 
            title="Comedy Movies" 
            movies={categories.comedy} 
            onPlayTrailer={handlePlayTrailer}
          />
        )}
        
        {categories.horror?.length > 0 && (
          <MovieRow 
            title="Horror Movies" 
            movies={categories.horror} 
            onPlayTrailer={handlePlayTrailer}
          />
        )}
        
        {categories.documentaries?.length > 0 && (
          <MovieRow 
            title="Documentaries" 
            movies={categories.documentaries} 
            onPlayTrailer={handlePlayTrailer}
          />
        )}
      </div>

      {showTrailer && selectedMovie && (
        <TrailerModal movie={selectedMovie} onClose={closeTrailer} />
      )}
      {/* Footer */}
      <footer className="relative z-10 w-full text-center py-6 bg-black bg-opacity-80 text-gray-400 text-sm mt-auto">
        © 2025 Swift Design. All rights reserved.
      </footer>
    </div>
  );
};

export default Browse;