import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response
from typing import Optional
from app.recommend import (
    recommend_for_user,
    recommend_for_user_by_category,
    recommend_for_username,
    recommend_for_username_by_category,
)

app = FastAPI(title="Video Recommendation Engine")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)  # No Content - eliminates the 404

# Main required endpoint
@app.get("/feed")
def feed(
    username: str = Query(..., description="Username"),
    top_k: int = Query(5, ge=1, le=100),
    project_code: Optional[str] = Query(None, description="Project code filter"),
    category: Optional[str] = Query(None, description="Category filter"),
    tag: Optional[str] = Query(None, description="Tag filter")
):
    try:
        if project_code or category or tag:
            results = recommend_for_username_by_category(
                username=username,
                top_k=top_k,
                category=category,
                tag=tag,
                project_code=project_code
            )
        else:
            results = recommend_for_username(username=username, top_k=top_k)
        
        return {
            "username": username,
            "top_k": top_k,
            "project_code": project_code,
            "category": category,
            "tag": tag,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Keep existing endpoint for backward compatibility
@app.get("/recommend/{user_id}")
def recommend(user_id: int, top_k: int = 5):
    try:
        recs = recommend_for_user(user_id=user_id, top_k=top_k)
        return {"user_id": user_id, "top_k": top_k, "results": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
