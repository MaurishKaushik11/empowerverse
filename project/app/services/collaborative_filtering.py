import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
import logging
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
import pickle
import os

from app.database.models import User, Post, UserInteraction
from app.core.config import settings

logger = logging.getLogger(__name__)

class CollaborativeFilter:
    """
    Collaborative Filtering implementation for video recommendations.
    Supports both user-based and item-based collaborative filtering.
    """
    
    def __init__(self):
        self.user_similarity_matrix = None
        self.item_similarity_matrix = None
        self.user_item_matrix = None
        self.svd_model = TruncatedSVD(n_components=50, random_state=42)
        self.user_factors = None
        self.item_factors = None
        self.load_models()
    
    async def get_user_similarities(self, user_id: int, candidate_items: List[int], db: Session) -> List[float]:
        """
        Get recommendation scores using user-based collaborative filtering.
        """
        try:
            # Build or load user-item interaction matrix
            if self.user_item_matrix is None:
                await self._build_user_item_matrix(db)
            
            if self.user_item_matrix is None:
                # Fallback to random scores
                return [np.random.random() for _ in candidate_items]
            
            # Get user index
            user_idx = self._get_user_index(user_id)
            if user_idx is None:
                return [np.random.random() for _ in candidate_items]
            
            # Calculate user similarities if not cached
            if self.user_similarity_matrix is None:
                await self._calculate_user_similarities()
            
            # Get similar users
            similar_users = self._get_similar_users(user_idx, top_k=50)
            
            # Calculate scores for candidate items
            scores = []
            for item_id in candidate_items:
                item_idx = self._get_item_index(item_id)
                if item_idx is not None:
                    score = self._predict_user_item_score(user_idx, item_idx, similar_users)
                else:
                    score = 0.0
                scores.append(score)
            
            return scores
            
        except Exception as e:
            logger.error(f"Error in collaborative filtering: {str(e)}")
            return [np.random.random() for _ in candidate_items]
    
    async def get_item_similarities(self, item_id: int, candidate_items: List[int], db: Session) -> List[float]:
        """
        Get recommendation scores using item-based collaborative filtering.
        """
        try:
            # Build or load user-item interaction matrix
            if self.user_item_matrix is None:
                await self._build_user_item_matrix(db)
            
            if self.user_item_matrix is None:
                return [np.random.random() for _ in candidate_items]
            
            # Calculate item similarities if not cached
            if self.item_similarity_matrix is None:
                await self._calculate_item_similarities()
            
            # Get item index
            item_idx = self._get_item_index(item_id)
            if item_idx is None:
                return [np.random.random() for _ in candidate_items]
            
            # Calculate similarities with candidate items
            scores = []
            for candidate_id in candidate_items:
                candidate_idx = self._get_item_index(candidate_id)
                if candidate_idx is not None and candidate_idx < len(self.item_similarity_matrix):
                    similarity = self.item_similarity_matrix[item_idx][candidate_idx]
                else:
                    similarity = 0.0
                scores.append(float(similarity))
            
            return scores
            
        except Exception as e:
            logger.error(f"Error in item-based collaborative filtering: {str(e)}")
            return [np.random.random() for _ in candidate_items]
    
    async def get_matrix_factorization_scores(self, user_id: int, candidate_items: List[int], db: Session) -> List[float]:
        """
        Get recommendation scores using matrix factorization (SVD).
        """
        try:
            # Build or load user-item interaction matrix
            if self.user_item_matrix is None:
                await self._build_user_item_matrix(db)
            
            if self.user_item_matrix is None:
                return [np.random.random() for _ in candidate_items]
            
            # Perform matrix factorization if not done
            if self.user_factors is None or self.item_factors is None:
                await self._perform_matrix_factorization()
            
            # Get user index
            user_idx = self._get_user_index(user_id)
            if user_idx is None or user_idx >= len(self.user_factors):
                return [np.random.random() for _ in candidate_items]
            
            # Calculate scores for candidate items
            scores = []
            user_vector = self.user_factors[user_idx]
            
            for item_id in candidate_items:
                item_idx = self._get_item_index(item_id)
                if item_idx is not None and item_idx < len(self.item_factors):
                    item_vector = self.item_factors[item_idx]
                    score = np.dot(user_vector, item_vector)
                else:
                    score = 0.0
                scores.append(float(score))
            
            return scores
            
        except Exception as e:
            logger.error(f"Error in matrix factorization: {str(e)}")
            return [np.random.random() for _ in candidate_items]
    
    async def _build_user_item_matrix(self, db: Session):
        """
        Build user-item interaction matrix from database.
        """
        try:
            # Get all interactions
            interactions = db.query(UserInteraction).all()
            
            if not interactions:
                logger.warning("No interactions found for building user-item matrix")
                return
            
            # Create mappings
            users = list(set([interaction.user_id for interaction in interactions]))
            items = list(set([interaction.post_id for interaction in interactions]))
            
            self.user_to_idx = {user_id: idx for idx, user_id in enumerate(users)}
            self.idx_to_user = {idx: user_id for user_id, idx in self.user_to_idx.items()}
            self.item_to_idx = {item_id: idx for idx, item_id in enumerate(items)}
            self.idx_to_item = {idx: item_id for item_id, idx in self.item_to_idx.items()}
            
            # Build interaction matrix
            n_users = len(users)
            n_items = len(items)
            
            # Create sparse matrix for memory efficiency
            row_indices = []
            col_indices = []
            data = []
            
            for interaction in interactions:
                user_idx = self.user_to_idx[interaction.user_id]
                item_idx = self.item_to_idx[interaction.post_id]
                
                # Weight different interaction types
                weight = self._get_interaction_weight(interaction.interaction_type)
                if interaction.interaction_value:
                    weight *= interaction.interaction_value
                
                row_indices.append(user_idx)
                col_indices.append(item_idx)
                data.append(weight)
            
            self.user_item_matrix = csr_matrix(
                (data, (row_indices, col_indices)), 
                shape=(n_users, n_items)
            )
            
            logger.info(f"Built user-item matrix: {n_users} users, {n_items} items, {len(data)} interactions")
            
        except Exception as e:
            logger.error(f"Error building user-item matrix: {str(e)}")
            self.user_item_matrix = None
    
    async def _calculate_user_similarities(self):
        """
        Calculate user-user similarity matrix using cosine similarity.
        """
        try:
            if self.user_item_matrix is None:
                return
            
            # Calculate cosine similarity between users
            user_similarities = cosine_similarity(self.user_item_matrix)
            self.user_similarity_matrix = user_similarities
            
            logger.info("Calculated user similarity matrix")
            
        except Exception as e:
            logger.error(f"Error calculating user similarities: {str(e)}")
    
    async def _calculate_item_similarities(self):
        """
        Calculate item-item similarity matrix using cosine similarity.
        """
        try:
            if self.user_item_matrix is None:
                return
            
            # Transpose matrix to get item-user matrix
            item_user_matrix = self.user_item_matrix.T
            
            # Calculate cosine similarity between items
            item_similarities = cosine_similarity(item_user_matrix)
            self.item_similarity_matrix = item_similarities
            
            logger.info("Calculated item similarity matrix")
            
        except Exception as e:
            logger.error(f"Error calculating item similarities: {str(e)}")
    
    async def _perform_matrix_factorization(self):
        """
        Perform matrix factorization using SVD.
        """
        try:
            if self.user_item_matrix is None:
                return
            
            # Fit SVD model
            self.svd_model.fit(self.user_item_matrix)
            
            # Get user and item factors
            self.user_factors = self.svd_model.transform(self.user_item_matrix)
            self.item_factors = self.svd_model.components_.T
            
            logger.info(f"Performed matrix factorization with {self.svd_model.n_components} components")
            
        except Exception as e:
            logger.error(f"Error in matrix factorization: {str(e)}")
    
    def _get_user_index(self, user_id: int) -> Optional[int]:
        """Get user index from user ID."""
        return getattr(self, 'user_to_idx', {}).get(user_id)
    
    def _get_item_index(self, item_id: int) -> Optional[int]:
        """Get item index from item ID."""
        return getattr(self, 'item_to_idx', {}).get(item_id)
    
    def _get_similar_users(self, user_idx: int, top_k: int = 50) -> List[Tuple[int, float]]:
        """
        Get top-k similar users for a given user.
        """
        if self.user_similarity_matrix is None:
            return []
        
        user_similarities = self.user_similarity_matrix[user_idx]
        
        # Get indices of most similar users (excluding self)
        similar_indices = np.argsort(user_similarities)[::-1][1:top_k+1]
        
        similar_users = [
            (idx, user_similarities[idx]) 
            for idx in similar_indices 
            if user_similarities[idx] > 0
        ]
        
        return similar_users
    
    def _predict_user_item_score(self, user_idx: int, item_idx: int, similar_users: List[Tuple[int, float]]) -> float:
        """
        Predict user-item interaction score using similar users.
        """
        if not similar_users:
            return 0.0
        
        numerator = 0.0
        denominator = 0.0
        
        for similar_user_idx, similarity in similar_users:
            if similar_user_idx < self.user_item_matrix.shape[0] and item_idx < self.user_item_matrix.shape[1]:
                rating = self.user_item_matrix[similar_user_idx, item_idx]
                if rating > 0:
                    numerator += similarity * rating
                    denominator += abs(similarity)
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _get_interaction_weight(self, interaction_type: str) -> float:
        """
        Get weight for different interaction types.
        """
        weights = {
            'view': 1.0,
            'like': 2.0,
            'share': 3.0,
            'bookmark': 2.5,
            'rate': 2.0,
            'comment': 1.5
        }
        
        return weights.get(interaction_type, 1.0)
    
    def save_models(self):
        """
        Save collaborative filtering models to disk.
        """
        try:
            os.makedirs(settings.MODEL_PATH, exist_ok=True)
            
            models_to_save = {
                'user_similarity_matrix': self.user_similarity_matrix,
                'item_similarity_matrix': self.item_similarity_matrix,
                'user_item_matrix': self.user_item_matrix,
                'user_factors': self.user_factors,
                'item_factors': self.item_factors,
                'user_to_idx': getattr(self, 'user_to_idx', {}),
                'item_to_idx': getattr(self, 'item_to_idx', {}),
                'idx_to_user': getattr(self, 'idx_to_user', {}),
                'idx_to_item': getattr(self, 'idx_to_item', {})
            }
            
            model_path = os.path.join(settings.MODEL_PATH, 'collaborative_filtering.pkl')
            
            with open(model_path, 'wb') as f:
                pickle.dump(models_to_save, f)
            
            # Save SVD model separately
            svd_path = os.path.join(settings.MODEL_PATH, 'svd_model.pkl')
            with open(svd_path, 'wb') as f:
                pickle.dump(self.svd_model, f)
            
            logger.info("Saved collaborative filtering models")
            
        except Exception as e:
            logger.error(f"Error saving collaborative filtering models: {str(e)}")
    
    def load_models(self):
        """
        Load collaborative filtering models from disk.
        """
        try:
            model_path = os.path.join(settings.MODEL_PATH, 'collaborative_filtering.pkl')
            svd_path = os.path.join(settings.MODEL_PATH, 'svd_model.pkl')
            
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    models = pickle.load(f)
                
                self.user_similarity_matrix = models.get('user_similarity_matrix')
                self.item_similarity_matrix = models.get('item_similarity_matrix')
                self.user_item_matrix = models.get('user_item_matrix')
                self.user_factors = models.get('user_factors')
                self.item_factors = models.get('item_factors')
                self.user_to_idx = models.get('user_to_idx', {})
                self.item_to_idx = models.get('item_to_idx', {})
                self.idx_to_user = models.get('idx_to_user', {})
                self.idx_to_item = models.get('idx_to_item', {})
                
                logger.info("Loaded collaborative filtering models")
            
            if os.path.exists(svd_path):
                with open(svd_path, 'rb') as f:
                    self.svd_model = pickle.load(f)
                logger.info("Loaded SVD model")
                
        except Exception as e:
            logger.warning(f"Could not load collaborative filtering models: {str(e)}")

class HybridCollaborativeFilter:
    """
    Hybrid collaborative filtering that combines multiple CF approaches.
    """
    
    def __init__(self):
        self.cf = CollaborativeFilter()
        self.weights = {
            'user_based': 0.4,
            'item_based': 0.3,
            'matrix_factorization': 0.3
        }
    
    async def get_hybrid_scores(self, user_id: int, candidate_items: List[int], db: Session) -> List[float]:
        """
        Get hybrid collaborative filtering scores.
        """
        try:
            # Get scores from different CF methods
            user_scores = await self.cf.get_user_similarities(user_id, candidate_items, db)
            item_scores = []  # Would need reference item for item-based CF
            mf_scores = await self.cf.get_matrix_factorization_scores(user_id, candidate_items, db)
            
            # Combine scores
            hybrid_scores = []
            for i in range(len(candidate_items)):
                score = (
                    user_scores[i] * self.weights['user_based'] +
                    mf_scores[i] * self.weights['matrix_factorization']
                )
                hybrid_scores.append(score)
            
            return hybrid_scores
            
        except Exception as e:
            logger.error(f"Error in hybrid collaborative filtering: {str(e)}")
            return [np.random.random() for _ in candidate_items]