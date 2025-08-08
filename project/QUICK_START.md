# 🚀 EmpowerVerse Quick Start Guide

## ⚡ Start Demo in 30 Seconds

### Option 1: Easy Start (Recommended)
```bash
cd c:\Users\HP\Downloads\empowerverse\project
python start_demo.py
```

### Option 2: Manual Start
```bash
cd c:\Users\HP\Downloads\empowerverse\project
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 🌐 Access Your Demo

Once the server starts, visit these URLs:

### 📚 **API Documentation**
- **Interactive Docs:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### 🎯 **Demo Endpoints**
- **Dashboard:** http://127.0.0.1:8000/api/v1/demo/dashboard
- **Users:** http://127.0.0.1:8000/api/v1/demo/users
- **Posts:** http://127.0.0.1:8000/api/v1/demo/posts
- **Categories:** http://127.0.0.1:8000/api/v1/demo/categories
- **Interactions:** http://127.0.0.1:8000/api/v1/demo/interactions/stats

### 🤖 **AI Recommendations**
- **Personalized Feed:** http://127.0.0.1:8000/api/v1/feed?username=alex_entrepreneur
- **Trending Content:** http://127.0.0.1:8000/api/v1/trending
- **Similar Content:** http://127.0.0.1:8000/api/v1/similar/1?username=sarah_developer

## 🎬 **Perfect for Presentations!**

Your demo includes:
- ✅ **5 Professional Users** with diverse profiles
- ✅ **8 Engaging Posts** with real YouTube content
- ✅ **Rich Analytics** and engagement metrics
- ✅ **AI-Powered Recommendations** 
- ✅ **Production-Ready Architecture**

## 🔄 **Refresh Sample Data**

If you need fresh data:
```bash
python create_sample_data_postgres.py
```

## 🛑 **Stop Server**

Press `Ctrl+C` in the terminal to stop the server.

---

**🎉 Your EmpowerVerse demo is ready to impress!** 🚀