import React, { useRef, useState } from "react";
import { ChevronLeft, ChevronRight, Play, Plus, ThumbsUp } from "lucide-react";
import { Button } from "./ui/button";

const MovieRow = ({ title, movies, onPlayTrailer }) => {
  const rowRef = useRef(null);
  const [hoveredMovie, setHoveredMovie] = useState(null);

  const scroll = (direction) => {
    const { current } = rowRef;
    if (current) {
      const scrollAmount = current.clientWidth * 0.8;
      current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="px-6 md:px-16 group">
      <h2 className="text-white text-xl md:text-2xl font-semibold mb-4">
        {title}
      </h2>
      <div className="relative">
        {/* Left Arrow */}
        <button
          className="absolute left-0 top-0 bottom-0 z-30 w-12 bg-black bg-opacity-50 text-white opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-opacity-75"
          onClick={() => scroll("left")}
        >
          <ChevronLeft className="w-8 h-8" />
        </button>

        {/* Movies Container */}
        <div
          ref={rowRef}
          className="flex space-x-2 overflow-x-scroll scrollbar-hide scroll-smooth"
        >
          {movies.map((movie) => (
            <div
              key={movie.id}
              className="relative min-w-[200px] md:min-w-[280px] cursor-pointer transform transition-all duration-300 hover:scale-110 hover:z-20"
              onMouseEnter={() => setHoveredMovie(movie.id)}
              onMouseLeave={() => setHoveredMovie(null)}
            >
              <img
                src={movie.image}
                alt={movie.title}
                className="w-full h-32 md:h-40 object-cover rounded-md"
                onError={(e) => {
                  e.target.src = `https://via.placeholder.com/280x160/333/fff?text=${encodeURIComponent(movie.title)}`;
                }}
              />
              
              {/* Hover Overlay */}
              {hoveredMovie === movie.id && (
                <div className="absolute inset-0 bg-black bg-opacity-80 rounded-md flex flex-col justify-end p-4 transition-all duration-200">
                  <h3 className="text-white font-semibold text-sm mb-2 line-clamp-2">
                    {movie.title}
                  </h3>
                  <div className="flex items-center space-x-2">
                    <Button
                      size="sm"
                      onClick={() => onPlayTrailer(movie)}
                      className="bg-white hover:bg-gray-200 text-black p-2 h-8 w-8"
                    >
                      <Play className="w-3 h-3 fill-current" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      className="text-white hover:text-gray-300 p-2 h-8 w-8"
                    >
                      <Plus className="w-3 h-3" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      className="text-white hover:text-gray-300 p-2 h-8 w-8"
                    >
                      <ThumbsUp className="w-3 h-3" />
                    </Button>
                  </div>
                  <div className="flex items-center mt-2 text-xs text-gray-300">
                    <span className="bg-red-600 text-white px-1 rounded text-xs mr-2">
                      {movie.rating}
                    </span>
                    <span>{movie.year}</span>
                    <span className="mx-1">•</span>
                    <span>{movie.duration}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Right Arrow */}
        <button
          className="absolute right-0 top-0 bottom-0 z-30 w-12 bg-black bg-opacity-50 text-white opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-opacity-75"
          onClick={() => scroll("right")}
        >
          <ChevronRight className="w-8 h-8" />
        </button>
      </div>
    </div>
  );
};

export default MovieRow;