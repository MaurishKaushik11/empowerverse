import os, sys, math, json
from typing import List, Optional, Dict, Any, Iterable, Set
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.database.database import SessionLocal
from app.database import models

# Weights for interaction types
WEIGHTS = {
    "view": 0.2,
    "like": 1.0,
    "bookmark": 1.2,
    "rating": 1.5,  # if ratings are 0–100, scaled below
}

def normalize_tags(tags) -> Set[str]:
    if not tags:
        return set()
    if isinstance(tags, str):
        try:
            tags = json.loads(tags)
        except Exception:
            tags = [t.strip() for t in tags.split(",") if t.strip()]
    return {str(t).strip().lower() for t in tags if t is not None}

def get_user_profile(db: Session, user_id: int) -> Dict[str, float]:
    """Weighted tag profile from user's interactions."""
    interactions = db.execute(
        select(models.Interaction, models.Post.tags)
        .join(models.Post, models.Post.id == models.Interaction.post_id)
        .where(models.Interaction.user_id == user_id)
    ).all()

    tag_weights: Dict[str, float] = {}
    for inter, tags in interactions:
        w = WEIGHTS.get(inter.type, 0.0)
        if inter.type == "rating" and inter.value is not None:
            val = float(inter.value)
            w *= (val / 5.0) if val <= 5.0 else (val / 100.0)
        for tag in normalize_tags(tags):
            tag_weights[tag] = tag_weights.get(tag, 0.0) + w
    return tag_weights

def popularity_score_for_post(p: models.Post) -> float:
    pop = (p.view_count or 0) + 2 * (p.upvote_count or 0) + 3 * (p.bookmark_count or 0)
    return math.log1p(pop) if pop > 0 else 0.0

def seen_penalty(db: Session, user_id: int, post_id: int) -> float:
    seen_weight = db.execute(
        select(func.count(models.Interaction.id))
        .where(models.Interaction.user_id == user_id, models.Interaction.post_id == post_id)
    ).scalar_one()
    return 0.5 * float(seen_weight)

def score_post_for_user(
    db: Session,
    user_id: int,
    post: models.Post,
    user_tag_profile: Dict[str, float],
    popularity_weight: float = 0.3,
    apply_seen_penalty: bool = True,
) -> float:
    post_tags = normalize_tags(post.tags)
    content_score = sum(user_tag_profile.get(t, 0.0) for t in post_tags)
    popularity = popularity_score_for_post(post)
    penalty = seen_penalty(db, user_id, post.id) if apply_seen_penalty else 0.0
    return content_score + popularity_weight * popularity - penalty

def fetch_posts(db: Session) -> List[models.Post]:
    return db.execute(select(models.Post)).scalars().all()

def filter_posts_by_category(
    posts: Iterable[models.Post],
    category: Optional[str] = None,
    tag: Optional[str] = None,
    project_code: Optional[str] = None
) -> List[models.Post]:
    """
    Filter candidates by:
      - category: matches post.category
      - tag: match against post.tags
      - project_code: matches post.project_code
    If more than one filter is provided, all must match.
    """
    cat = category.strip().lower() if category else None
    tg = tag.strip().lower() if tag else None
    pc = project_code.strip().lower() if project_code else None

    filtered: List[models.Post] = []
    for p in posts:
        ok = True
        if cat is not None:
            # Handle category as JSON or string
            p_cat = ""
            if isinstance(p.category, dict):
                p_cat = (p.category.get("name", "") or "").strip().lower()
            elif isinstance(p.category, str):
                p_cat = p.category.strip().lower()
            ok = ok and (p_cat == cat)
        if tg is not None:
            p_tags = normalize_tags(p.tags)
            ok = ok and (tg in p_tags)
        if pc is not None:
            p_pc = (getattr(p, "project_code", None) or "").strip().lower()
            ok = ok and (p_pc == pc)
        if ok:
            filtered.append(p)
    return filtered

def recommend_for_user(user_id: int, top_k: int = 5) -> List[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        tag_profile = get_user_profile(db, user_id)
        posts = fetch_posts(db)
        if not posts:
            return []
        scored = [(score_post_for_user(db, user_id, p, tag_profile), p) for p in posts]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{
            "post_id": p.id,
            "title": p.title,
            "slug": p.slug,
            "score": round(s, 4),
            "tags": sorted(list(normalize_tags(p.tags))),
            "view_count": p.view_count,
            "upvote_count": p.upvote_count,
            "bookmark_count": p.bookmark_count,
            "average_rating": p.average_rating,
            "project_code": getattr(p, "project_code", None),
            "video_link": p.video_link,
            "thumbnail_url": p.thumbnail_url,
            "category": p.category,
            "topic": p.topic
        } for s, p in scored[:top_k]]
    finally:
        db.close()

def recommend_for_user_by_category(
    user_id: int,
    top_k: int = 5,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    project_code: Optional[str] = None
) -> List[Dict[str, Any]]:
    db: Session = SessionLocal()
    try:
        if not any([category, tag, project_code]):
            return []
        tag_profile = get_user_profile(db, user_id)
        posts = fetch_posts(db)
        candidates = filter_posts_by_category(posts, category=category, tag=tag, project_code=project_code)
        if not candidates:
            return []
        scored = [(score_post_for_user(db, user_id, p, tag_profile), p) for p in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{
            "post_id": p.id,
            "title": p.title,
            "slug": p.slug,
            "score": round(s, 4),
            "tags": sorted(list(normalize_tags(p.tags))),
            "view_count": p.view_count,
            "upvote_count": p.upvote_count,
            "bookmark_count": p.bookmark_count,
            "average_rating": p.average_rating,
            "project_code": getattr(p, "project_code", None),
            "video_link": p.video_link,
            "thumbnail_url": p.thumbnail_url,
            "category": p.category,
            "topic": p.topic
        } for s, p in scored[:top_k]]
    finally:
        db.close()

def get_user_id_by_username(db: Session, username: str) -> Optional[int]:
    row = db.execute(
        select(models.User.id).where(models.User.username == username)
    ).first()
    return row[0] if row else None

def recommend_for_username(username: str, top_k: int = 5):
    db: Session = SessionLocal()
    try:
        user_id = get_user_id_by_username(db, username)
        if user_id is None:
            # Cold start: return popular posts for new users
            posts = fetch_posts(db)
            if not posts:
                return []
            # Sort by popularity score
            scored = [(popularity_score_for_post(p), p) for p in posts]
            scored.sort(key=lambda x: x[0], reverse=True)
            return [{
                "post_id": p.id,
                "title": p.title,
                "slug": p.slug,
                "score": round(s, 4),
                "tags": sorted(list(normalize_tags(p.tags))),
                "view_count": p.view_count,
                "upvote_count": p.upvote_count,
                "bookmark_count": p.bookmark_count,
                "average_rating": p.average_rating,
                "project_code": getattr(p, "project_code", None),
                "video_link": p.video_link,
                "thumbnail_url": p.thumbnail_url,
                "category": p.category,
                "topic": p.topic
            } for s, p in scored[:top_k]]
        return recommend_for_user(user_id=user_id, top_k=top_k)
    finally:
        db.close()

def recommend_for_username_by_category(
    username: str,
    top_k: int = 5,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    project_code: Optional[str] = None
):
    db: Session = SessionLocal()
    try:
        user_id = get_user_id_by_username(db, username)
        if user_id is None:
            # Cold start: return popular posts filtered by category for new users
            if not any([category, tag, project_code]):
                return []
            posts = fetch_posts(db)
            candidates = filter_posts_by_category(posts, category=category, tag=tag, project_code=project_code)
            if not candidates:
                return []
            # Sort by popularity score
            scored = [(popularity_score_for_post(p), p) for p in candidates]
            scored.sort(key=lambda x: x[0], reverse=True)
            return [{
                "post_id": p.id,
                "title": p.title,
                "slug": p.slug,
                "score": round(s, 4),
                "tags": sorted(list(normalize_tags(p.tags))),
                "view_count": p.view_count,
                "upvote_count": p.upvote_count,
                "bookmark_count": p.bookmark_count,
                "average_rating": p.average_rating,
                "project_code": getattr(p, "project_code", None),
                "video_link": p.video_link,
                "thumbnail_url": p.thumbnail_url,
                "category": p.category,
                "topic": p.topic
            } for s, p in scored[:top_k]]
        return recommend_for_user_by_category(
            user_id=user_id,
            top_k=top_k,
            category=category,
            tag=tag,
            project_code=project_code
        )
    finally:
        db.close()