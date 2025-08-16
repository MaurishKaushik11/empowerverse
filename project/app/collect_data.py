import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database import models
import requests

# Load variables from .env at project root
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.socialverseapp.com").rstrip("/")
FLIC_TOKEN = os.getenv("FLIC_TOKEN", "")

if not FLIC_TOKEN:
    raise RuntimeError("FLIC_TOKEN is missing. Put it in your .env file at project root.")

HEADERS = {"Flic-Token": FLIC_TOKEN}

def fetch_posts(page=1, page_size=1000):
    url = f"{API_BASE_URL}/posts/summary/get"
    r = requests.get(url, headers=HEADERS, params={"page": page, "page_size": page_size}, timeout=30)
    if r.status_code != 200:
        print(f"API error {r.status_code}: {r.text}")
        return []
    data = r.json()
    posts = data.get("post") or data.get("posts") or data.get("data") or []
    return posts

def save_posts():
    db: Session = SessionLocal()
    posts = fetch_posts()
    saved = 0
    for post in posts:
        slug = post.get("slug") or f"post-{post.get('id')}"
        title = post.get("title") or slug
        existing = db.query(models.Post).filter_by(slug=slug).first()
        if not existing:
            existing = models.Post(slug=slug, title=title)

        existing.view_count = post.get("view_count") or 0
        existing.upvote_count = post.get("upvote_count") or 0
        existing.comment_count = post.get("comment_count") or 0
        existing.rating_count = post.get("rating_count") or 0
        try:
            existing.average_rating = float(post.get("average_rating") or 0)
        except Exception:
            existing.average_rating = 0.0

        existing.share_count = post.get("share_count") or 0
        existing.bookmark_count = post.get("bookmark_count") or 0
        existing.is_available_in_public_feed = bool(post.get("is_available_in_public_feed", True))
        existing.is_locked = bool(post.get("is_locked", False))
        existing.video_link = post.get("video_link")
        existing.thumbnail_url = post.get("thumbnail_url")
        existing.gif_thumbnail_url = post.get("gif_thumbnail_url")
        existing.tags = post.get("tags") or []
        existing.created_at_ms = post.get("created_at")
        existing.owner = post.get("owner")
        existing.category = post.get("category")
        existing.topic = post.get("topic")
        existing.base_token = post.get("baseToken") or post.get("base_token")
        
        # Extract project_code from topic if available
        if existing.topic and isinstance(existing.topic, dict):
            existing.project_code = existing.topic.get("project_code")

        db.add(existing)
        saved += 1

    db.commit()
    db.close()
    print(f"Saved {saved} posts.")

if __name__ == "__main__":
    save_posts()