import React, { useState, useEffect } from "react";
import { Search, Bell, ChevronDown } from "lucide-react";
import { Input } from "./ui/input";

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [showSearch, setShowSearch] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 px-6 py-4 transition-all duration-300 ${
      isScrolled ? "bg-black" : "bg-transparent"
    }`}>
      <div className="flex items-center justify-between">
        {/* Left Side */}
        <div className="flex items-center space-x-8">
          <div className="text-red-600 text-2xl font-bold tracking-wide">
            NETFLIX
          </div>
          <div className="hidden md:flex items-center space-x-6">
            <a href="#" className="text-white hover:text-gray-300 transition-colors">
              Home
            </a>
            <a href="#" className="text-white hover:text-gray-300 transition-colors">
              TV Shows
            </a>
            <a href="#" className="text-white hover:text-gray-300 transition-colors">
              Movies
            </a>
            <a href="#" className="text-white hover:text-gray-300 transition-colors">
              New & Popular
            </a>
            <a href="#" className="text-white hover:text-gray-300 transition-colors">
              My List
            </a>
          </div>
        </div>

        {/* Right Side */}
        <div className="flex items-center space-x-4">
          {/* Search */}
          <div className="relative">
            {showSearch ? (
              <div className="flex items-center bg-black bg-opacity-50 border border-gray-600 rounded">
                <Search 
                  className="w-5 h-5 text-white ml-3 cursor-pointer" 
                  onClick={() => setShowSearch(false)}
                />
                <Input
                  type="text"
                  placeholder="Search..."
                  className="bg-transparent border-0 text-white placeholder-gray-400 focus:outline-none w-64"
                  autoFocus
                  onBlur={() => setShowSearch(false)}
                />
              </div>
            ) : (
              <Search 
                className="w-6 h-6 text-white cursor-pointer hover:text-gray-300 transition-colors" 
                onClick={() => setShowSearch(true)}
              />
            )}
          </div>

          {/* Notifications */}
          <Bell className="w-6 h-6 text-white cursor-pointer hover:text-gray-300 transition-colors" />

          {/* Profile */}
          <div className="flex items-center space-x-2 cursor-pointer">
            <div className="w-8 h-8 bg-red-600 rounded overflow-hidden">
              <img 
                src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=32&h=32&fit=crop&crop=face" 
                alt="Profile" 
                className="w-full h-full object-cover"
              />
            </div>
            <ChevronDown className="w-4 h-4 text-white" />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;