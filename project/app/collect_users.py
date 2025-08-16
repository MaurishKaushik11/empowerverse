import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.database import models
import requests

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.socialverseapp.com").rstrip("/")
FLIC_TOKEN = os.getenv("FLIC_TOKEN", "")

if not FLIC_TOKEN:
    raise RuntimeError("FLIC_TOKEN not set in .env")

HEADERS = {"Flic-Token": FLIC_TOKEN}

def fetch_users(page=1, page_size=1000):
    url = f"{API_BASE_URL}/users/get_all"
    r = requests.get(url, headers=HEADERS, params={"page": page, "page_size": page_size}, timeout=30)
    if r.status_code != 200:
        print(f"API Error {r.status_code}: {r.text}")
        return []
    data = r.json()
    return data.get("users") or data.get("data") or []

def save_users():
    db: Session = SessionLocal()
    users = fetch_users()
    saved = 0
    for u in users:
        username = u.get("username")
        if not username:
            continue
        existing = db.query(models.User).filter_by(username=username).first()
        if not existing:
            existing = models.User(username=username)
            db.add(existing)
            saved += 1
    db.commit()
    db.close()
    print(f"Saved {saved} users.")

if __name__ == "__main__":
    save_users()