
# Swift Design | Netflix Clone

This is a fullstack Netflix Clone built with React (frontend) and FastAPI (backend), designed and maintained by Swift Design.

## Features
- Browse trending, popular, and categorized movies
- Watch trailers
- Responsive UI with modern design
- Backend API with FastAPI and MongoDB

## Project Structure
- `frontend/` — React app (UI, components, pages)
- `backend/` — FastAPI server, routers, models, services

## Getting Started

### Prerequisites
- Node.js & npm
- Python 3.8+
- MongoDB (local or cloud)

### Frontend Setup
```bash
cd frontend
npm install
npm run build
npx serve -s build
```
Visit `http://localhost:5000` (or the port shown) to view the app.

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --reload
```
Backend runs at `http://localhost:8000` by default.

### Environment Variables
Create a `.env` file in `backend/` with:
```
MONGO_URL=your_mongodb_url
DB_NAME=your_db_name
TMDB_API_KEY=your_tmdb_api_key
TMDB_API_KEY_2=your_tmdb_api_key_2
```

## License
© 2025 Swift Design. All rights reserved.
