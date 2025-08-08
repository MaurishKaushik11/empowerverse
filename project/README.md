# Video Recommendation Engine

A sophisticated recommendation system that suggests personalized video content based on user preferences and engagement patterns using deep neural networks.

## 🎯 Project Overview

This project implements a video recommendation algorithm that:

- Delivers personalized content recommendations using deep neural networks
- Handles cold start problems using mood-based recommendations
- Utilizes Graph/Deep neural networks for content analysis
- Integrates with external APIs for data collection
- Implements efficient data caching and pagination
- Supports collaborative filtering and content-based filtering
- Provides hybrid recommendation approaches

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Machine Learning**: PyTorch, TensorFlow, scikit-learn
- **Caching**: Redis
- **Task Queue**: Celery
- **Documentation**: Swagger/OpenAPI
- **Migration**: Alembic

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Virtual environment (recommended)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/video-recommendation-engine.git
cd video-recommendation-engine
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# API Configuration
API_BASE_URL=https://api.socialverseapp.com
FLIC_TOKEN=your_flic_token_here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/video_recommendation_db

# Redis Configuration
REDIS_URL=redis://localhost:6379

# ML Model Configuration
MODEL_PATH=./models
EMBEDDING_DIM=128
BATCH_SIZE=32
LEARNING_RATE=0.001

# Recommendation Configuration
MAX_RECOMMENDATIONS=50
COLD_START_THRESHOLD=5
SIMILARITY_THRESHOLD=0.3

# Cache Configuration
CACHE_TTL=3600
```

### 5. Set Up Database

Create PostgreSQL database:

```bash
createdb video_recommendation_db
```

Run database migrations:

```bash
alembic upgrade head
```

### 6. Create Model Directory

```bash
mkdir -p models
```

### 7. Start the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📊 API Endpoints

### Recommendation Endpoints

#### Get Personalized Feed

```http
GET /api/v1/feed?username={username}&page=1&page_size=20
```

Returns personalized video recommendations for a specific user.

**Parameters:**
- `username` (required): Username for personalized recommendations
- `project_code` (optional): Category/project code filter
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Number of items per page (default: 20)
- `mood` (optional): Mood filter
- `category` (optional): Category filter

#### Get Category-based Feed

```http
GET /api/v1/feed/category?username={username}&project_code={project_code}
```

Returns category-specific video recommendations for a user.

#### Get Trending Content

```http
GET /api/v1/trending?page=1&page_size=20&category=Motivation
```

Returns trending video content based on engagement metrics.

#### Get Similar Content

```http
GET /api/v1/similar/{post_id}?username={username}&page=1&page_size=20
```

Returns content similar to a specific post using content-based filtering.

#### Record User Interaction

```http
POST /api/v1/interaction
```

Record user interaction with a post for improving recommendations.

**Request Body:**
```json
{
  "username": "user123",
  "post_id": 1234,
  "interaction_type": "like",
  "interaction_value": 1.0
}
```

### Data Collection Endpoints (Internal Use)

These endpoints require the `Flic-Token` header for authentication.

#### Collect Viewed Posts

```http
POST /api/v1/collect/viewed-posts?page=1&page_size=1000
```

#### Collect Liked Posts

```http
POST /api/v1/collect/liked-posts?page=1&page_size=1000
```

#### Collect Inspired Posts

```http
POST /api/v1/collect/inspired-posts?page=1&page_size=1000
```

#### Collect Rated Posts

```http
POST /api/v1/collect/rated-posts?page=1&page_size=1000
```

#### Collect All Posts

```http
POST /api/v1/collect/all-posts?page=1&page_size=1000
```

#### Collect All Users

```http
POST /api/v1/collect/all-users?page=1&page_size=1000
```

#### Get Collection Status

```http
GET /api/v1/collection-status
```

## 🧠 Machine Learning Models

### Deep Recommendation Model

The system uses a deep neural network implemented in PyTorch with:

- Multi-layer perceptron architecture
- Attention mechanism for feature importance
- Batch normalization and dropout for regularization
- User and item embedding layers

### Content Embedding Model

Uses TensorFlow/Keras for generating content embeddings:

- Processes user profiles and post metadata
- Generates fixed-size embedding vectors
- Supports both user and item embeddings

### Collaborative Filtering

Implements multiple collaborative filtering approaches:

- User-based collaborative filtering
- Item-based collaborative filtering
- Matrix factorization using SVD
- Hybrid collaborative filtering

### Graph Neural Networks

Optional GNN support for capturing complex relationships:

- User-item interaction graphs
- Item-item similarity graphs
- Graph convolutional networks

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | External API base URL | `https://api.socialverseapp.com` |
| `FLIC_TOKEN` | Authentication token for external API | Required |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `MODEL_PATH` | Directory for ML models | `./models` |
| `EMBEDDING_DIM` | Embedding vector dimension | `128` |
| `MAX_RECOMMENDATIONS` | Maximum recommendations per request | `50` |
| `COLD_START_THRESHOLD` | Minimum interactions for personalization | `5` |
| `SIMILARITY_THRESHOLD` | Minimum similarity for recommendations | `0.3` |

## 🧪 Testing

Run tests using pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

## 📚 API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🏗️ Architecture

### System Components

1. **FastAPI Application**: Main web framework handling HTTP requests
2. **Database Layer**: PostgreSQL with SQLAlchemy ORM
3. **Recommendation Engine**: Core ML-based recommendation logic
4. **Data Collector**: Service for collecting external API data
5. **Neural Networks**: Deep learning models for recommendations
6. **Collaborative Filtering**: Traditional recommendation algorithms
7. **Caching Layer**: Redis for performance optimization

### Data Flow

1. **Data Collection**: External APIs → Data Collector → Database
2. **User Request**: Client → FastAPI → Recommendation Engine
3. **ML Processing**: User/Item Embeddings → Neural Networks → Scores
4. **Hybrid Scoring**: Deep Learning + Collaborative Filtering + Content-Based
5. **Response**: Ranked Recommendations → Client

## 🔄 Data Pipeline

### Collection Process

1. **Scheduled Collection**: Periodic data collection from external APIs
2. **Data Processing**: Clean and normalize collected data
3. **Database Storage**: Store users, posts, categories, topics, interactions
4. **Embedding Generation**: Create user and item embeddings
5. **Model Training**: Update ML models with new data

### Recommendation Process

1. **User Profile**: Analyze user preferences and interaction history
2. **Candidate Generation**: Get relevant posts based on filters
3. **Feature Engineering**: Extract user and item features
4. **ML Scoring**: Apply deep learning and collaborative filtering
5. **Hybrid Ranking**: Combine multiple recommendation approaches
6. **Post-processing**: Apply business rules and diversity
7. **Response**: Return ranked recommendations

## 🚀 Deployment

### Production Setup

1. **Environment**: Set up production environment variables
2. **Database**: Configure PostgreSQL with proper indexing
3. **Redis**: Set up Redis cluster for caching
4. **ML Models**: Pre-train and deploy ML models
5. **Monitoring**: Set up logging and monitoring
6. **Load Balancing**: Configure load balancer for high availability

### Docker Deployment

```bash
# Build Docker image
docker build -t video-recommendation-engine .

# Run with Docker Compose
docker-compose up -d
```

## 📈 Performance Optimization

### Caching Strategy

- **User Embeddings**: Cache user embeddings for 1 hour
- **Post Embeddings**: Cache post embeddings for 24 hours
- **Recommendations**: Cache recommendations for 30 minutes
- **Similarity Matrices**: Cache similarity computations

### Database Optimization

- **Indexing**: Proper indexes on user_id, post_id, timestamps
- **Partitioning**: Partition large tables by date
- **Connection Pooling**: Use connection pooling for database access
- **Query Optimization**: Optimize complex recommendation queries

## 🔍 Monitoring and Logging

### Metrics to Monitor

- **API Response Times**: Track recommendation latency
- **Model Performance**: Monitor recommendation accuracy
- **Database Performance**: Track query execution times
- **Cache Hit Rates**: Monitor caching effectiveness
- **User Engagement**: Track click-through rates

### Logging

- **Structured Logging**: Use JSON format for logs
- **Log Levels**: Appropriate log levels for different components
- **Error Tracking**: Comprehensive error logging and alerting
- **Audit Logs**: Track all user interactions and recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- PyTorch and TensorFlow for ML capabilities
- PostgreSQL for robust data storage
- Redis for high-performance caching
- The open-source community for various libraries and tools

## 📞 Support

For support and questions:

- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation at `/docs` endpoint

---

**Note**: This is a sophisticated recommendation system designed for production use. Make sure to properly configure all components and test thoroughly before deploying to production.