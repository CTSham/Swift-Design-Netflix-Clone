import React from "react";
import { Play, Info } from "lucide-react";
import { Button } from "./ui/button";

const Hero = ({ movie, onPlayTrailer }) => {
  if (!movie) return null;

  return (
    <div className="relative h-screen flex items-center">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url(${movie.backdropImage})`,
        }}
      >
        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-black via-black/70 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black to-transparent" />
      </div>

      {/* Content */}
      <div className="relative z-10 px-6 md:px-16 max-w-2xl">
        <h1 className="text-white text-4xl md:text-6xl font-bold mb-4 leading-tight">
          {movie.title}
        </h1>
        <p className="text-white text-lg md:text-xl mb-6 leading-relaxed">
          {movie.description}
        </p>
        <div className="flex items-center space-x-4">
          <Button 
            onClick={() => onPlayTrailer(movie)}
            className="bg-white hover:bg-gray-200 text-black font-semibold px-8 py-3 text-lg flex items-center gap-2 transition-all transform hover:scale-105"
          >
            <Play className="w-6 h-6 fill-current" />
            Play
          </Button>
          <Button 
            variant="secondary"
            className="bg-gray-600 bg-opacity-70 hover:bg-gray-500 text-white font-semibold px-8 py-3 text-lg flex items-center gap-2 transition-all transform hover:scale-105"
          >
            <Info className="w-6 h-6" />
            More Info
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Hero;