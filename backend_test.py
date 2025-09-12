#!/usr/bin/env python3
"""
Netflix Clone Backend API Test Suite
Tests all TMDB API integration endpoints
"""

import requests
import json
import sys
import os
from typing import Dict, List, Any
from datetime import datetime

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except FileNotFoundError:
        return "http://localhost:8001"
    return "http://localhost:8001"

BACKEND_URL = get_backend_url()
API_BASE = f"{BACKEND_URL}/api"

class NetflixBackendTester:
    def __init__(self):
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'test_details': []
        }
        
    def log_test(self, test_name: str, passed: bool, details: str = "", response_data: Any = None):
        """Log test result"""
        self.results['total_tests'] += 1
        if passed:
            self.results['passed'] += 1
            status = "✅ PASS"
        else:
            self.results['failed'] += 1
            status = "❌ FAIL"
            
        self.results['test_details'].append({
            'test': test_name,
            'status': status,
            'details': details,
            'response_data': response_data
        })
        
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        print()

    def validate_movie_structure(self, movie: Dict) -> tuple[bool, str]:
        """Validate movie data structure"""
        required_fields = [
            'id', 'title', 'image', 'backdrop_image', 'description', 
            'year', 'duration', 'rating', 'genre', 'tmdb_id', 'media_type'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in movie:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing fields: {missing_fields}"
        
        # Validate data types and content
        if not isinstance(movie['id'], int):
            return False, "id should be integer"
        if not isinstance(movie['title'], str) or not movie['title']:
            return False, "title should be non-empty string"
        if not isinstance(movie['image'], str) or not movie['image'].startswith('http'):
            return False, "image should be valid URL"
        if not isinstance(movie['backdrop_image'], str) or not movie['backdrop_image'].startswith('http'):
            return False, "backdrop_image should be valid URL"
        if not isinstance(movie['description'], str):
            return False, "description should be string"
        if movie['media_type'] not in ['movie', 'tv']:
            return False, "media_type should be 'movie' or 'tv'"
            
        return True, "Valid movie structure"

    def test_basic_api_endpoint(self):
        """Test basic API endpoint /api/"""
        try:
            response = requests.get(f"{API_BASE}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'Netflix Clone API' in data['message']:
                    self.log_test("Basic API Endpoint", True, f"Response: {data['message']}")
                else:
                    self.log_test("Basic API Endpoint", False, f"Unexpected response: {data}")
            else:
                self.log_test("Basic API Endpoint", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Basic API Endpoint", False, f"Exception: {str(e)}")

    def test_trending_movies(self):
        """Test /api/movies/trending endpoint"""
        try:
            response = requests.get(f"{API_BASE}/movies/trending", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check response structure
                if not all(key in data for key in ['success', 'data', 'total']):
                    self.log_test("Trending Movies", False, "Missing required response fields")
                    return
                
                if not data['success']:
                    self.log_test("Trending Movies", False, "API returned success=false")
                    return
                
                movies = data['data']
                if not movies:
                    self.log_test("Trending Movies", False, "No movies returned (empty array)")
                    return
                
                # Validate first movie structure
                valid, msg = self.validate_movie_structure(movies[0])
                if not valid:
                    self.log_test("Trending Movies", False, f"Invalid movie structure: {msg}")
                    return
                
                self.log_test("Trending Movies", True, 
                            f"Returned {len(movies)} movies. Sample: {movies[0]['title']} ({movies[0]['year']})")
                
            else:
                self.log_test("Trending Movies", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Trending Movies", False, f"Exception: {str(e)}")

    def test_popular_movies(self):
        """Test /api/movies/popular endpoint"""
        try:
            response = requests.get(f"{API_BASE}/movies/popular", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('success'):
                    self.log_test("Popular Movies", False, "API returned success=false")
                    return
                
                movies = data['data']
                if not movies:
                    self.log_test("Popular Movies", False, "No movies returned")
                    return
                
                # Validate movie structure
                valid, msg = self.validate_movie_structure(movies[0])
                if not valid:
                    self.log_test("Popular Movies", False, f"Invalid movie structure: {msg}")
                    return
                
                self.log_test("Popular Movies", True, 
                            f"Returned {len(movies)} movies. Sample: {movies[0]['title']}")
                
            else:
                self.log_test("Popular Movies", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Popular Movies", False, f"Exception: {str(e)}")

    def test_category_movies(self, category: str):
        """Test /api/movies/category/{category} endpoint"""
        try:
            response = requests.get(f"{API_BASE}/movies/category/{category}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('success'):
                    self.log_test(f"Category Movies ({category})", False, "API returned success=false")
                    return
                
                movies = data['data']
                if not movies:
                    self.log_test(f"Category Movies ({category})", False, "No movies returned")
                    return
                
                # Validate movie structure
                valid, msg = self.validate_movie_structure(movies[0])
                if not valid:
                    self.log_test(f"Category Movies ({category})", False, f"Invalid movie structure: {msg}")
                    return
                
                self.log_test(f"Category Movies ({category})", True, 
                            f"Returned {len(movies)} movies. Sample: {movies[0]['title']}")
                
            else:
                self.log_test(f"Category Movies ({category})", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test(f"Category Movies ({category})", False, f"Exception: {str(e)}")

    def test_search_movies(self):
        """Test /api/movies/search endpoint"""
        try:
            search_query = "spider"
            response = requests.get(f"{API_BASE}/movies/search?q={search_query}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('success'):
                    self.log_test("Search Movies", False, "API returned success=false")
                    return
                
                movies = data['data']
                if not movies:
                    self.log_test("Search Movies", False, f"No results for query '{search_query}'")
                    return
                
                # Validate movie structure
                valid, msg = self.validate_movie_structure(movies[0])
                if not valid:
                    self.log_test("Search Movies", False, f"Invalid movie structure: {msg}")
                    return
                
                # Check if results are relevant to search query
                relevant_results = [m for m in movies if 'spider' in m['title'].lower()]
                
                self.log_test("Search Movies", True, 
                            f"Returned {len(movies)} results for '{search_query}'. "
                            f"Relevant results: {len(relevant_results)}. "
                            f"Sample: {movies[0]['title']}")
                
            else:
                self.log_test("Search Movies", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Search Movies", False, f"Exception: {str(e)}")

    def test_netflix_style_endpoint(self):
        """Test /api/movies/netflix-style endpoint"""
        try:
            response = requests.get(f"{API_BASE}/movies/netflix-style", timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                if not data.get('success'):
                    self.log_test("Netflix Style Endpoint", False, "API returned success=false")
                    return
                
                categories = data.get('categories', {})
                expected_categories = ['trending', 'popular', 'action', 'comedy', 'horror', 'documentaries']
                
                missing_categories = [cat for cat in expected_categories if cat not in categories]
                if missing_categories:
                    self.log_test("Netflix Style Endpoint", False, f"Missing categories: {missing_categories}")
                    return
                
                # Validate each category has movies
                empty_categories = []
                for cat_name, movies in categories.items():
                    if not movies:
                        empty_categories.append(cat_name)
                    elif movies:  # Validate structure of first movie in each category
                        valid, msg = self.validate_movie_structure(movies[0])
                        if not valid:
                            self.log_test("Netflix Style Endpoint", False, 
                                        f"Invalid movie structure in {cat_name}: {msg}")
                            return
                
                if empty_categories:
                    self.log_test("Netflix Style Endpoint", False, f"Empty categories: {empty_categories}")
                    return
                
                total_movies = sum(len(movies) for movies in categories.values())
                self.log_test("Netflix Style Endpoint", True, 
                            f"Returned {len(categories)} categories with {total_movies} total movies")
                
            else:
                self.log_test("Netflix Style Endpoint", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test("Netflix Style Endpoint", False, f"Exception: {str(e)}")

    def test_movie_trailer(self, movie_id: int, media_type: str = "movie"):
        """Test /api/movies/{movie_id}/trailer endpoint"""
        try:
            response = requests.get(f"{API_BASE}/movies/{movie_id}/trailer?media_type={media_type}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') and data.get('trailer_url'):
                    # Validate YouTube URL
                    trailer_url = data['trailer_url']
                    if 'youtube.com/watch?v=' in trailer_url:
                        self.log_test(f"Movie Trailer (ID: {movie_id})", True, 
                                    f"Trailer URL: {trailer_url}")
                    else:
                        self.log_test(f"Movie Trailer (ID: {movie_id})", False, 
                                    f"Invalid trailer URL format: {trailer_url}")
                elif not data.get('success') and data.get('message'):
                    # No trailer available is acceptable
                    self.log_test(f"Movie Trailer (ID: {movie_id})", True, 
                                f"No trailer available: {data['message']}")
                else:
                    self.log_test(f"Movie Trailer (ID: {movie_id})", False, 
                                f"Unexpected response: {data}")
                
            else:
                self.log_test(f"Movie Trailer (ID: {movie_id})", False, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_test(f"Movie Trailer (ID: {movie_id})", False, f"Exception: {str(e)}")

    def test_error_handling(self):
        """Test error handling for invalid endpoints"""
        try:
            # Test invalid category
            response = requests.get(f"{API_BASE}/movies/category/invalid_category", timeout=10)
            if response.status_code == 500:
                self.log_test("Error Handling (Invalid Category)", True, "Correctly returned 500 for invalid category")
            else:
                self.log_test("Error Handling (Invalid Category)", False, f"Expected 500, got {response.status_code}")
            
            # Test invalid movie ID for trailer
            response = requests.get(f"{API_BASE}/movies/999999999/trailer", timeout=10)
            if response.status_code in [200, 404, 500]:  # Any of these are acceptable
                self.log_test("Error Handling (Invalid Movie ID)", True, f"Handled invalid movie ID with status {response.status_code}")
            else:
                self.log_test("Error Handling (Invalid Movie ID)", False, f"Unexpected status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")

    def get_sample_movie_id(self) -> int:
        """Get a sample movie ID from trending movies for trailer testing"""
        try:
            response = requests.get(f"{API_BASE}/movies/trending", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('data'):
                    return data['data'][0]['id']
        except:
            pass
        return 550  # Default to a popular movie ID (Fight Club)

    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 60)
        print("NETFLIX CLONE BACKEND API TEST SUITE")
        print("=" * 60)
        print(f"Testing backend at: {BACKEND_URL}")
        print(f"API base URL: {API_BASE}")
        print()
        
        # Basic API test
        self.test_basic_api_endpoint()
        
        # TMDB API tests
        self.test_trending_movies()
        self.test_popular_movies()
        
        # Category tests
        categories = ['action', 'comedy']
        for category in categories:
            self.test_category_movies(category)
        
        # Search test
        self.test_search_movies()
        
        # Netflix-style endpoint
        self.test_netflix_style_endpoint()
        
        # Trailer test (get sample movie ID first)
        sample_movie_id = self.get_sample_movie_id()
        self.test_movie_trailer(sample_movie_id)
        
        # Error handling tests
        self.test_error_handling()
        
        # Print summary
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Success Rate: {(self.results['passed']/self.results['total_tests']*100):.1f}%")
        print()
        
        if self.results['failed'] > 0:
            print("FAILED TESTS:")
            for test in self.results['test_details']:
                if "❌" in test['status']:
                    print(f"- {test['test']}: {test['details']}")
            print()
        
        return self.results['failed'] == 0

if __name__ == "__main__":
    tester = NetflixBackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All tests passed! Backend is working correctly.")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the details above.")
        sys.exit(1)