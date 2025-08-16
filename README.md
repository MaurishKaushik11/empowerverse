# 🎬 EmpowerVerse - Video Recommendation Engine

A personalized video recommendation system built with FastAPI, featuring AI-powered content filtering and user interaction tracking.

## 🚀 Quick Start

```bash
# Clone repository
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

**Access:** http://127.0.0.1:8000

## ✨ Features

- 🤖 **AI-Powered Recommendations** - Personalized content based on user interactions
- 🎯 **Smart Filtering** - Category, tag, and project code filtering
- 🔥 **Cold Start Handling** - Popular content for new users
- 📊 **Real-time Analytics** - User engagement tracking
- 🚀 **Fast API** - High-performance async endpoints
- 📱 **Modern UI** - Clean, responsive interface
- 🧪 **Comprehensive Testing** - 22+ automated tests

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite/PostgreSQL
- **Frontend:** React, TypeScript, Tailwind CSS
- **ML/AI:** Content-based filtering, similarity scoring
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Testing:** Pytest, automated endpoint testing

## 📋 API Endpoints

### Main Recommendations
```bash
# Personalized feed
GET /feed?username={user}&top_k={count}

# With filters
GET /feed?username={user}&category={cat}&tag={tag}&project_code={code}

# Legacy endpoint
GET /recommend/{user_id}?top_k={count}
```

### Example Usage
```bash
curl "http://127.0.0.1:8000/feed?username=alice&top_k=5"
curl "http://127.0.0.1:8000/feed?username=bob&category=fitness&top_k=3"
```

## 📊 Sample Data

**Users:** alice, bob, charlie, diana, eve  
**Categories:** education, fitness, lifestyle, wellness  
**Tags:** python, fitness, cooking, meditation  
**Project Codes:** EV, FIT, COOK, WELL

## 🧪 Testing

```bash
# Run all tests
python test_endpoints.py

# Test specific endpoint
curl "http://127.0.0.1:8000/feed?username=alice&top_k=3"
```

## 📖 Documentation

- **API Docs:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **Project Summary:** [PROJECT_SUMMARY.md](project/PROJECT_SUMMARY.md)

## 🏗️ Project Structure

```
empowerverse/
├── project/                 # Main application
│   ├── app/
│   │   ├── main.py         # FastAPI app
│   │   ├── recommend.py    # AI recommendation logic
│   │   └── database/       # Models & DB config
│   ├── setup_database.py   # DB initialization
│   ├── create_sample_data.py # Sample data
│   ├── test_endpoints.py   # Test suite
│   └── start_server.py     # Server startup
└── frontend/               # React UI (optional)
```

## 🔧 Environment Setup

Create `.env` file:
```env
FLIC_TOKEN=your_token_here
API_BASE_URL=https://api.socialverseapp.com
DATABASE_URL=sqlite:///./app.db
```

## 🚀 Production Deployment

### Docker
```bash
docker build -t empowerverse .
docker run -p 8000:8000 empowerverse
```

### Manual
```bash
# Install production dependencies
pip install -r requirements.txt

# Setup PostgreSQL
createdb empowerverse_db
export DATABASE_URL=postgresql://user:pass@localhost/empowerverse_db

# Start with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository:** https://github.com/MaurishKaushik11/empowerverse
- **Issues:** https://github.com/MaurishKaushik11/empowerverse/issues
- **Documentation:** http://127.0.0.1:8000/docs

---

**Built with ❤️ for personalized video recommendations**