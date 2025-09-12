import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { ChevronRight } from "lucide-react";

const Home = () => {
  const [email, setEmail] = useState("");
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/browse");
  };

  return (
  <div className="min-h-screen bg-black relative overflow-hidden flex flex-col justify-between">
      {/* Background Movie Grid */}
      <div className="absolute inset-0 opacity-30">
        <div className="grid grid-cols-8 gap-2 h-full p-4 transform rotate-12 scale-110">
          {[...Array(64)].map((_, i) => (
            <div
              key={i}
              className="aspect-[3/4] bg-gradient-to-b from-gray-700 to-gray-900 rounded-sm"
              style={{
                backgroundImage: `url(https://picsum.photos/300/400?random=${i})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center'
              }}
            />
          ))}
        </div>
      </div>

      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-black bg-opacity-60" />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between p-6">
        <div className="text-red-600 text-4xl font-bold tracking-wide">
          NETFLIX
        </div>
        <div className="flex items-center gap-4">
          <select className="bg-black bg-opacity-50 text-white border border-gray-600 rounded px-3 py-1">
            <option>🌐 English</option>
          </select>
          <Button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2">
            Sign In
          </Button>
        </div>
      </header>

      {/* Hero Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-[80vh] text-center px-6">
        <h1 className="text-white text-5xl md:text-6xl font-bold mb-6 max-w-4xl leading-tight">
          Unlimited movies, TV shows, and more
        </h1>
        <p className="text-white text-xl md:text-2xl mb-4">
          Starts at $7.99. Cancel anytime.
        </p>
        <p className="text-white text-lg mb-8">
          Ready to watch? Enter your email to create or restart your membership.
        </p>

        {/* Email Input Form */}
        <div className="flex flex-col sm:flex-row gap-4 w-full max-w-2xl">
          <Input
            type="email"
            placeholder="Email address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="flex-1 bg-black bg-opacity-50 border border-gray-600 text-white placeholder-gray-400 h-14 text-lg px-4"
          />
          <Button
            onClick={handleGetStarted}
            className="bg-red-600 hover:bg-red-700 text-white h-14 px-8 text-lg font-semibold flex items-center gap-2"
          >
            Get Started
            <ChevronRight className="w-5 h-5" />
          </Button>
        </div>
      </div>
      {/* Footer */}
      <footer className="relative z-10 w-full text-center py-6 bg-black bg-opacity-80 text-gray-400 text-sm mt-auto">
        © 2025 Swift Design. All rights reserved.
      </footer>
    </div>
  );
};

export default Home;