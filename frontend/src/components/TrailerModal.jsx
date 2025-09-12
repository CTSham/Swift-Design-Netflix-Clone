import React, { useEffect } from "react";
import { X } from "lucide-react";
import { Button } from "./ui/button";

const TrailerModal = ({ movie, onClose }) => {
  useEffect(() => {
    // Prevent scrolling when modal is open
    document.body.style.overflow = 'hidden';
    
    // Handle escape key
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    
    document.addEventListener('keydown', handleEscape);
    
    return () => {
      document.body.style.overflow = 'auto';
      document.removeEventListener('keydown', handleEscape);
    };
  }, [onClose]);

  if (!movie) return null;

  // Extract YouTube video ID from trailer URL
  const getYouTubeEmbedUrl = (url) => {
    if (!url) return null;
    const videoId = url.includes('youtube.com/watch?v=') 
      ? url.split('v=')[1]?.split('&')[0]
      : url.includes('youtu.be/') 
      ? url.split('youtu.be/')[1]?.split('?')[0]
      : null;
    
    return videoId ? `https://www.youtube.com/embed/${videoId}?autoplay=1&controls=1` : null;
  };

  const embedUrl = getYouTubeEmbedUrl(movie.trailerUrl);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90">
      <div className="relative w-full max-w-4xl mx-4">
        {/* Close Button */}
        <Button
          onClick={onClose}
          variant="ghost"
          className="absolute -top-12 right-0 text-white hover:text-gray-300 z-10"
        >
          <X className="w-8 h-8" />
        </Button>

        {/* Video Container */}
        <div className="relative bg-black rounded-lg overflow-hidden shadow-2xl">
          {embedUrl ? (
            <div className="aspect-video">
              <iframe
                src={embedUrl}
                title={`${movie.title} Trailer`}
                className="w-full h-full"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </div>
          ) : (
            <div className="aspect-video bg-gray-800 flex items-center justify-center">
              <div className="text-center text-white">
                <h3 className="text-2xl font-semibold mb-2">{movie.title}</h3>
                <p className="text-gray-300">Trailer not available</p>
              </div>
            </div>
          )}

          {/* Movie Info */}
          <div className="p-6 bg-gradient-to-t from-black to-transparent">
            <h2 className="text-white text-2xl font-bold mb-2">{movie.title}</h2>
            <div className="flex items-center space-x-4 text-sm text-gray-300 mb-3">
              <span className="bg-red-600 text-white px-2 py-1 rounded text-xs">
                {movie.rating}
              </span>
              <span>{movie.year}</span>
              <span>{movie.duration}</span>
              <span className="bg-gray-600 px-2 py-1 rounded text-xs">
                {movie.genre}
              </span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">
              {movie.description}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrailerModal;