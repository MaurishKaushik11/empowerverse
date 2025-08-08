from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_BASE_URL: str = "https://api.socialverseapp.com"
    FLIC_TOKEN: str = "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:123456@localhost:5432/video_recommendation_db"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # ML Model Configuration
    MODEL_PATH: str = "./models"
    EMBEDDING_DIM: int = 128
    BATCH_SIZE: int = 32
    LEARNING_RATE: float = 0.001
    
    # Recommendation Configuration
    MAX_RECOMMENDATIONS: int = 50
    COLD_START_THRESHOLD: int = 5
    SIMILARITY_THRESHOLD: float = 0.3
    
    # Cache Configuration
    CACHE_TTL: int = 3600  # 1 hour
    
    # Development Configuration
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create models directory if it doesn't exist
def ensure_models_directory():
    models_path = "./models"
    if not os.path.exists(models_path):
        os.makedirs(models_path)
        print(f"Created models directory: {models_path}")

settings = Settings()
ensure_models_directory()