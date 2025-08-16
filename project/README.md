# Video Recommendation Engine

A personalized video recommendation system with content-based filtering and user interaction tracking.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/MaurishKaushik11/empowerverse.git
cd empowerverse/project

# Install dependencies
pip install -r requirements.txt

# Setup database and sample data
python setup_database.py
python create_sample_data.py

# Start server
python start_server.py
```

**Server runs on:** http://127.0.0.1:8000

## API Endpoints

### Main Feed Endpoint
```
GET /feed?username={username}&top_k={number}&category={category}&tag={tag}&project_code={code}
```

**Examples:**
```bash
# Basic recommendations
curl "http://127.0.0.1:8000/feed?username=alice&top_k=5"

# With filters
curl "http://127.0.0.1:8000/feed?username=bob&category=fitness&top_k=3"
curl "http://127.0.0.1:8000/feed?username=alice&tag=python&top_k=2"
curl "http://127.0.0.1:8000/feed?username=charlie&project_code=EV&top_k=3"
```

### Legacy Endpoint
```
GET /recommend/{user_id}?top_k={number}
```

**Example:**
```bash
curl "http://127.0.0.1:8000/recommend/1?top_k=5"
```

## Response Format

```json
{
  "username": "alice",
  "top_k": 3,
  "results": [
    {
      "post_id": 4,
      "title": "Advanced Python Programming",
      "slug": "advanced-python",
      "score": 9.0433,
      "tags": ["python", "programming"],
      "view_count": 300,
      "upvote_count": 45,
      "average_rating": 4.8,
      "project_code": "EV",
      "video_link": "https://example.com/video4.mp4",
      "category": {"name": "education", "id": 1}
    }
  ]
}
```

## Test Data

**Users:** alice, bob, charlie, diana, eve  
**Categories:** education, fitness, lifestyle, wellness  
**Tags:** python, fitness, cooking, meditation  
**Project Codes:** EV, FIT, COOK, WELL

## Testing

```bash
# Run all tests
python test_endpoints.py

# Test specific endpoint
curl "http://127.0.0.1:8000/feed?username=alice&top_k=3"
```

## Documentation

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Features

- ✅ Personalized recommendations based on user interactions
- ✅ Content filtering by category, tags, and project codes
- ✅ Cold start handling for new users
- ✅ SQLite database with sample data
- ✅ Comprehensive test suite (22 tests)
- ✅ Easy setup and deployment

## Environment Setup

Create `.env` file:
```env
FLIC_TOKEN=your_token_here
API_BASE_URL=https://api.socialverseapp.com
DATABASE_URL=sqlite:///./app.db
```

## Data Collection

```bash
# Collect real data from API
python app/collect_users.py
python app/collect_data.py
python app/collect_interactions.py
```

## Project Structure

```
project/
├── app/
│   ├── main.py              # FastAPI app
│   ├── recommend.py         # Recommendation logic
│   ├── collect_*.py         # Data collection
│   └── database/            # Models & DB config
├── setup_database.py        # DB initialization
├── create_sample_data.py    # Sample data
├── test_endpoints.py        # Test suite
└── start_server.py          # Server startup
```

## License

MIT License