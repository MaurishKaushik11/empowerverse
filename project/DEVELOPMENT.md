# EmpowerVerse Development Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ (optional, SQLite fallback available)
- Redis 6+ (optional, for caching)

### One-Command Setup
```bash
python start_dev.py
```

This script will:
- Check dependencies
- Set up the environment
- Run database migrations
- Start both backend and frontend servers

## 🛠️ Manual Setup

### Backend Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Database Setup**
```bash
# For PostgreSQL (recommended)
createdb video_recommendation_db

# Run migrations
alembic upgrade head
```

5. **Start Backend Server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. **Install Dependencies**
```bash
npm install
```

2. **Start Development Server**
```bash
npm run dev
```

## 📊 API Endpoints

### Recommendation Endpoints

#### Get Personalized Feed
```http
GET /api/v1/feed?username={username}&page=1&page_size=20
```

#### Get Category Feed
```http
GET /api/v1/feed/category?username={username}&project_code={project_code}
```

#### Get Trending Content
```http
GET /api/v1/trending?page=1&page_size=20&category=Motivation
```

#### Get Similar Content
```http
GET /api/v1/similar/{post_id}?username={username}
```

#### Record Interaction
```http
POST /api/v1/interaction
Content-Type: application/json

{
  "username": "user123",
  "post_id": 1234,
  "interaction_type": "like",
  "interaction_value": 1.0
}
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api_endpoints.py
```

### Frontend Tests
```bash
# Run tests
npm test

# Run tests in watch mode
npm run test:watch
```

## 🏗️ Architecture Overview

### Backend Components
- **FastAPI Application**: Main web framework
- **Database Layer**: PostgreSQL with SQLAlchemy ORM
- **Recommendation Engine**: ML-based recommendation logic
- **Neural Networks**: PyTorch & TensorFlow models
- **Data Collector**: External API data collection
- **Caching Layer**: Redis for performance

### Frontend Components
- **React Application**: Main UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **API Service**: Backend communication
- **State Management**: React hooks

## 🔧 Development Features

### Hot Reload
- Backend: Automatic reload on code changes
- Frontend: Vite hot module replacement

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Error Handling
- Comprehensive error boundaries
- Graceful API fallbacks
- Development error details

## 📝 Code Structure

```
project/
├── app/                    # Backend application
│   ├── core/              # Core configuration
│   ├── database/          # Database models and connection
│   ├── routers/           # API route handlers
│   ├── services/          # Business logic services
│   └── schemas/           # Pydantic schemas
├── src/                   # Frontend application
│   ├── components/        # React components
│   ├── services/          # API and business services
│   └── types/             # TypeScript type definitions
├── tests/                 # Test files
├── models/                # ML model storage
└── docs/                  # Documentation
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Manual Deployment
1. Set production environment variables
2. Build frontend: `npm run build`
3. Start backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
4. Serve frontend with nginx or similar

## 🔍 Debugging

### Backend Debugging
- Logs are available in console
- Use `--log-level debug` for detailed logs
- Database queries logged when `DEBUG=True`

### Frontend Debugging
- React DevTools browser extension
- Console logs for API calls
- Network tab for request inspection

## 📈 Performance Optimization

### Backend
- Database connection pooling
- Redis caching for recommendations
- Async/await for I/O operations
- ML model caching

### Frontend
- Code splitting with Vite
- Image lazy loading
- API response caching
- Optimized re-renders

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [PyTorch Documentation](https://pytorch.org/)
- [TensorFlow Documentation](https://tensorflow.org/)

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Fallback to SQLite will be used automatically

**Frontend Build Errors**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version compatibility

**ML Model Loading Issues**
- Ensure models directory exists
- Check model file permissions
- Verify PyTorch/TensorFlow installation

**API Connection Issues**
- Verify backend server is running on port 8000
- Check CORS configuration
- Ensure API_BASE_URL is correct in frontend