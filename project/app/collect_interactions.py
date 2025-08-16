import os, sys, random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.database import SessionLocal
from app.database import models
import requests

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.socialverseapp.com").rstrip("/")
FLIC_TOKEN = os.getenv("FLIC_TOKEN", "")
HEADERS = {"Flic-Token": FLIC_TOKEN} if FLIC_TOKEN else {}

# Config
MAX_USERS_PER_POST = 5           # cap users per post
MIN_SYNTHETIC_PER_POST = 3       # minimum interactions per post to generate

def fetch_interactions_from_api(page=1, page_size=100):
    url = f"{API_BASE_URL}/activities/get"  # placeholder; real endpoint unknown
    try:
        r = requests.get(url, headers=HEADERS, params={"page": page, "page_size": page_size}, timeout=30)
        if r.status_code != 200:
            print(f"[real] API error {r.status_code}: {r.text}")
            return []
        data = r.json()
        items = data.get("interactions") or data.get("activities") or data.get("data") or []
        print(f"[real] fetched {len(items)} interactions")
        return items
    except Exception as e:
        print(f"[real] exception: {e}")
        return []

def save_interactions_from_api():
    db: Session = SessionLocal()
    items = fetch_interactions_from_api()
    saved = 0
    for it in items:
        user_id = it.get("user_id") or it.get("userId")
        post_id = it.get("post_id") or it.get("postId")
        typ = it.get("type") or it.get("action") or "view"
        val = it.get("value")
        if not (user_id and post_id):
            continue
        u = db.query(models.User).filter_by(id=user_id).first()
        p = db.query(models.Post).filter_by(id=post_id).first()
        if not u or not p:
            continue
        exists = db.query(models.Interaction).filter_by(user_id=user_id, post_id=post_id, type=typ).first()
        if not exists:
            db.add(models.Interaction(user_id=user_id, post_id=post_id, type=typ, value=val))
            saved += 1
    db.commit()
    db.close()
    print(f"[real] saved {saved} interactions")
    return saved

def _random_users(db: Session, k: int):
    ids = db.execute(select(models.User.id)).scalars().all()
    return random.sample(ids, min(k, len(ids))) if ids else []

def save_interactions_synthetic():
    db: Session = SessionLocal()
    user_ids_all = db.execute(select(models.User.id)).scalars().all()
    posts = db.execute(select(models.Post)).scalars().all()

    print(f"[synthetic] users available: {len(user_ids_all)}; posts available: {len(posts)}")
    if not user_ids_all or not posts:
        db.close()
        return 0

    total_saved = 0
    for post in posts:
        user_ids = _random_users(db, MAX_USERS_PER_POST)
        if not user_ids:
            continue

        vc = post.view_count or 0
        uc = post.upvote_count or 0
        bc = post.bookmark_count or 0
        rc = post.rating_count or 0
        ar = float(post.average_rating or 0)

        interactions_to_create = []

        # Derive counts and ensure a minimum set per post
        # Use min with len(user_ids) to cap per post
        n_views = min(len(user_ids), max(1, vc // 10))
        n_likes = min(len(user_ids), uc)
        n_bookmarks = min(len(user_ids), bc)
        n_ratings = min(len(user_ids), rc)

        # If all zero, enforce a small baseline so we always create something
        if n_views + n_likes + n_bookmarks + n_ratings < MIN_SYNTHETIC_PER_POST:
            baseline = min(len(user_ids), MIN_SYNTHETIC_PER_POST)
            # Distribute: 1 view, 1 like, rest bookmarks (if baseline >= 2)
            if baseline >= 1:
                n_views = max(n_views, 1)
            if baseline >= 2:
                n_likes = max(n_likes, 1)
            if baseline >= 3:
                n_bookmarks = max(n_bookmarks, baseline - (n_views + n_likes))

        # Pick unique users per type to vary interactions
        random.shuffle(user_ids)
        for uid in user_ids[:n_views]:
            interactions_to_create.append(("view", None, uid))

        random.shuffle(user_ids)
        for uid in user_ids[:n_likes]:
            interactions_to_create.append(("like", None, uid))

        random.shuffle(user_ids)
        for uid in user_ids[:n_bookmarks]:
            interactions_to_create.append(("bookmark", None, uid))

        if ar > 0:
            random.shuffle(user_ids)
            for uid in user_ids[:n_ratings]:
                interactions_to_create.append(("rating", ar, uid))

        # Upsert unique interactions
        for typ, val, uid in interactions_to_create:
            exists = db.query(models.Interaction).filter_by(
                user_id=uid, post_id=post.id, type=typ
            ).first()
            if not exists:
                db.add(models.Interaction(
                    user_id=uid,
                    post_id=post.id,
                    type=typ,
                    value=val
                ))
                total_saved += 1

    db.commit()
    db.close()
    print(f"[synthetic] saved {total_saved} interactions")
    return total_saved

if __name__ == "__main__":
    print("Trying real interactions endpoint...")
    real_saved = save_interactions_from_api()
    if real_saved == 0:
        print("Falling back to synthetic interactions...")
        save_interactions_synthetic()