import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import Hero from "./Hero";
import MovieRow from "./MovieRow";
import TrailerModal from "./TrailerModal";
import { mockData } from "../data/mock";

const Browse = () => {
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [showTrailer, setShowTrailer] = useState(false);
  const [heroMovie, setHeroMovie] = useState(null);

  useEffect(() => {
    // Set random hero movie from trending
    const randomHero = mockData.categories.trending[
      Math.floor(Math.random() * mockData.categories.trending.length)
    ];
    setHeroMovie(randomHero);
  }, []);

  const handlePlayTrailer = (movie) => {
    setSelectedMovie(movie);
    setShowTrailer(true);
  };

  const closeTrailer = () => {
    setShowTrailer(false);
    setSelectedMovie(null);
  };

  return (
    <div className="bg-black min-h-screen">
      <Navbar />
      {heroMovie && <Hero movie={heroMovie} onPlayTrailer={handlePlayTrailer} />}
      
      <div className="relative z-10 -mt-32 space-y-12 pb-20">
        <MovieRow 
          title="Trending Now" 
          movies={mockData.categories.trending} 
          onPlayTrailer={handlePlayTrailer}
        />
        <MovieRow 
          title="Popular on Netflix" 
          movies={mockData.categories.popular} 
          onPlayTrailer={handlePlayTrailer}
        />
        <MovieRow 
          title="Action Movies" 
          movies={mockData.categories.action} 
          onPlayTrailer={handlePlayTrailer}
        />
        <MovieRow 
          title="Comedy Movies" 
          movies={mockData.categories.comedy} 
          onPlayTrailer={handlePlayTrailer}
        />
        <MovieRow 
          title="Horror Movies" 
          movies={mockData.categories.horror} 
          onPlayTrailer={handlePlayTrailer}
        />
        <MovieRow 
          title="Documentaries" 
          movies={mockData.categories.documentaries} 
          onPlayTrailer={handlePlayTrailer}
        />
      </div>

      {showTrailer && selectedMovie && (
        <TrailerModal movie={selectedMovie} onClose={closeTrailer} />
      )}
    </div>
  );
};

export default Browse;