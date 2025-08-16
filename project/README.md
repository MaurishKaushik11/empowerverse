# Video Recommendation Engine

A sophisticated recommendation system for personalized video content based on user interactions and preferences.

## Features

- **Personalized Recommendations**: Content-based filtering using user interaction history
- **Category Filtering**: Filter recommendations by category, tags, or project codes
- **Cold Start Handling**: Popular content recommendations for new users
- **Multiple Endpoints**: Both modern `/feed` and legacy `/recommend` endpoints
- **Real-time Data Collection**: Scripts to collect users, posts, and interactions from API
- **SQLite Database**: Lightweight database for development and testing

## API Endpoints

### Main Feed Endpoint
```
GET /feed?username={username}&top_k={number}&category={category}&tag={tag}&project_code={code}
```

**Parameters:**
- `username` (required): Username for personalized recommendations
- `top_k` (optional, default=5): Number of recommendations to return (1-100)
- `category` (optional): Filter by category name
- `tag` (optional): Filter by tag
- `project_code` (optional): Filter by project code

**Example Requests:**
```bash
# Basic personalized feed
curl "http://127.0.0.1:8000/feed?username=alice&top_k=5"

# Category filtered feed
curl "http://127.0.0.1:8000/feed?username=bob&category=fitness&top_k=3"

# Tag filtered feed
curl "http://127.0.0.1:8000/feed?username=charlie&tag=cooking&top_k=2"

# Project code filtered feed
curl "http://127.0.0.1:8000/feed?username=alice&project_code=EV&top_k=3"

# Combined filters
curl "http://127.0.0.1:8000/feed?username=alice&category=education&project_code=EV&top_k=2"
```

### Legacy Endpoint
```
GET /recommend/{user_id}?top_k={number}
```

**Parameters:**
- `user_id` (required): User ID for recommendations
- `top_k` (optional, default=5): Number of recommendations

**Example:**
```bash
curl "http://127.0.0.1:8000/recommend/1?top_k=5"
```

### Health Check
```
GET /
```

Returns: `{"status": "ok"}`

## Response Format

```json
{
  "username": "alice",
  "top_k": 3,
  "project_code": null,
  "category": null,
  "tag": null,
  "results": [
    {
      "post_id": 4,
      "title": "Advanced Python Programming",
      "slug": "advanced-python",
      "score": 9.0433,
      "tags": ["advanced", "programming", "python"],
      "view_count": 300,
      "upvote_count": 45,
      "bookmark_count": 25,
      "average_rating": 4.8,
      "project_code": "EV",
      "video_link": "https://example.com/video4.mp4",
      "thumbnail_url": "https://example.com/thumb4.jpg",
      "category": {"name": "education", "id": 1},
      "topic": {"name": "Programming", "project_code": "EV"}
    }
  ]
}
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MaurishKaushik11/empowerverse.git
cd empowerverse/project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
FLIC_TOKEN=your_flic_token_here
API_BASE_URL=https://api.socialverseapp.com
DATABASE_URL=sqlite:///./app.db
```

### 4. Initialize Database and Sample Data
```bash
# Create database tables and add sample data
python setup_database.py
python create_sample_data.py
```

### 5. Start the Server
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The server will be available at:
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Data Collection

### Collect Real Data from API
```bash
# Collect users
python app/collect_users.py

# Collect posts
python app/collect_data.py

# Collect interactions (with fallback to synthetic data)
python app/collect_interactions.py
```

### Create Sample Data for Testing
```bash
python create_sample_data.py
```

## Testing

Run the comprehensive test suite:
```bash
python test_endpoints.py
```

This will test all endpoints with various scenarios including:
- Personalized recommendations for existing users
- Category, tag, and project code filtering
- Cold start scenarios for new users
- Legacy endpoint compatibility
- Edge cases and error handling

## Recommendation Algorithm

The system uses a hybrid approach combining:

1. **Content-Based Filtering**: Matches user preferences with post tags
2. **Popularity Scoring**: Considers view counts, upvotes, and bookmarks
3. **Interaction Weighting**: Different weights for different interaction types:
   - View: 0.2
   - Like: 1.0
   - Bookmark: 1.2
   - Rating: 1.5 (scaled by rating value)

4. **Seen Penalty**: Reduces scores for previously interacted content
5. **Cold Start Handling**: Shows popular content to new users

## Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `created_at`: Account creation timestamp

### Posts
- `id`: Primary key
- `title`: Post title
- `slug`: Unique URL slug
- `view_count`, `upvote_count`, `bookmark_count`: Engagement metrics
- `rating_count`, `average_rating`: Rating information
- `tags`: JSON array of tags
- `category`, `topic`: JSON objects with metadata
- `project_code`: Project classification
- `video_link`, `thumbnail_url`: Media URLs

### Interactions
- `id`: Primary key
- `user_id`: Foreign key to users
- `post_id`: Foreign key to posts
- `type`: Interaction type (view, like, bookmark, rating)
- `value`: Optional value (e.g., rating score)
- `timestamp`: Interaction timestamp

## Project Structure

```
project/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── recommend.py            # Recommendation logic
│   ├── collect_data.py         # Post data collection
│   ├── collect_users.py        # User data collection
│   ├── collect_interactions.py # Interaction data collection
│   └── database/
│       ├── database.py         # Database configuration
│       └── models.py           # SQLAlchemy models
├── setup_database.py           # Database initialization
├── create_sample_data.py       # Sample data creation
├── test_endpoints.py           # Comprehensive test suite
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## Development

### Adding New Features
1. Update models in `app/database/models.py`
2. Modify recommendation logic in `app/recommend.py`
3. Add new endpoints in `app/main.py`
4. Update tests in `test_endpoints.py`

### Database Migrations
For schema changes, recreate the database:
```bash
rm app.db
python setup_database.py
python create_sample_data.py
```

## Production Deployment

### Environment Variables
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
FLIC_TOKEN=your_production_token
API_BASE_URL=https://api.socialverseapp.com
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.