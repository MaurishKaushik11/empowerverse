from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserPreferences(BaseModel):
    categories: List[str] = []
    topics: List[str] = []
    mood: str = "energetic"
    content_types: List[str] = []

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    owner: Dict[str, Any]
    category: Dict[str, Any]
    topic: Dict[str, Any]
    video_link: str
    thumbnail_url: str
    gif_thumbnail_url: Optional[str] = None
    view_count: int
    upvote_count: int
    comment_count: int
    share_count: int
    bookmark_count: int
    rating_count: int
    average_rating: float
    is_available_in_public_feed: bool
    is_locked: bool
    tags: List[str] = []
    created_at: int  # Unix timestamp
    upvoted: bool = False
    bookmarked: bool = False
    following: bool = False
    identifier: str
    exit_count: int = 0
    contract_address: str = ""
    chain_id: str = ""
    chart_url: str = ""
    baseToken: Dict[str, str] = {}

class RecommendationResponse(BaseModel):
    status: str
    post: List[PostResponse]
    algorithm_used: str
    total_count: int
    page: int
    page_size: int
    confidence_scores: Optional[List[float]] = None

class FeedRequest(BaseModel):
    username: str
    project_code: Optional[str] = None
    page: int = 1
    page_size: int = 20
    mood: Optional[str] = None
    category: Optional[str] = None

class InteractionRequest(BaseModel):
    username: str
    post_id: int
    interaction_type: str  # view, like, bookmark, share, rate
    interaction_value: Optional[float] = None

class UserProfileUpdate(BaseModel):
    preferences: UserPreferences
    demographics: Optional[Dict[str, Any]] = None