import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging
from sklearn.preprocessing import StandardScaler
import pickle
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

class DeepRecommendationModel(nn.Module):
    """
    Deep Neural Network for video recommendation using PyTorch.
    Implements a multi-layer perceptron with attention mechanism.
    """
    
    def __init__(self, user_dim=128, item_dim=128, hidden_dims=[256, 128, 64]):
        super(DeepRecommendationModel, self).__init__()
        
        self.user_dim = user_dim
        self.item_dim = item_dim
        self.hidden_dims = hidden_dims
        
        # User embedding layers
        self.user_embedding = nn.Linear(user_dim, hidden_dims[0] // 2)
        self.user_bn = nn.BatchNorm1d(hidden_dims[0] // 2)
        
        # Item embedding layers
        self.item_embedding = nn.Linear(item_dim, hidden_dims[0] // 2)
        self.item_bn = nn.BatchNorm1d(hidden_dims[0] // 2)
        
        # Combined feature layers
        layers = []
        input_dim = hidden_dims[0]
        
        for hidden_dim in hidden_dims[1:]:
            layers.extend([
                nn.Linear(input_dim, hidden_dim),
                nn.BatchNorm1d(hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.3)
            ])
            input_dim = hidden_dim
        
        # Output layer
        layers.append(nn.Linear(input_dim, 1))
        layers.append(nn.Sigmoid())
        
        self.mlp = nn.Sequential(*layers)
        
        # Attention mechanism
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_dims[0],
            num_heads=8,
            dropout=0.1
        )
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.to(self.device)
        
        # Load pre-trained weights if available
        self.load_model()
    
    def forward(self, user_features, item_features):
        """Forward pass through the network."""
        batch_size = user_features.size(0)
        
        # Process user features
        user_emb = F.relu(self.user_bn(self.user_embedding(user_features)))
        
        # Process item features
        item_emb = F.relu(self.item_bn(self.item_embedding(item_features)))
        
        # Combine features
        combined = torch.cat([user_emb, item_emb], dim=1)
        
        # Apply attention (reshape for attention mechanism)
        combined_reshaped = combined.unsqueeze(0)  # Add sequence dimension
        attended, _ = self.attention(combined_reshaped, combined_reshaped, combined_reshaped)
        attended = attended.squeeze(0)  # Remove sequence dimension
        
        # Pass through MLP
        output = self.mlp(attended)
        
        return output.squeeze()
    
    async def predict(self, user_embedding: np.ndarray, item_embeddings: List[np.ndarray], user_profile: Dict) -> List[float]:
        """Make predictions for user-item pairs."""
        try:
            self.eval()
            
            with torch.no_grad():
                # Convert to tensors
                user_tensor = torch.FloatTensor(user_embedding).unsqueeze(0).to(self.device)
                
                predictions = []
                
                for item_embedding in item_embeddings:
                    item_tensor = torch.FloatTensor(item_embedding).unsqueeze(0).to(self.device)
                    
                    # Make prediction
                    pred = self.forward(user_tensor, item_tensor)
                    predictions.append(float(pred.cpu().numpy()))
                
                return predictions
                
        except Exception as e:
            logger.error(f"Error in deep model prediction: {str(e)}")
            # Return random scores as fallback
            return [np.random.random() for _ in item_embeddings]
    
    def load_model(self):
        """Load pre-trained model weights."""
        model_path = os.path.join(settings.MODEL_PATH, "deep_recommendation_model.pth")
        
        if os.path.exists(model_path):
            try:
                checkpoint = torch.load(model_path, map_location=self.device)
                self.load_state_dict(checkpoint['model_state_dict'])
                logger.info("Loaded pre-trained deep recommendation model")
            except Exception as e:
                logger.warning(f"Could not load pre-trained model: {str(e)}")
        else:
            logger.info("No pre-trained model found, using random initialization")
    
    def save_model(self):
        """Save model weights."""
        os.makedirs(settings.MODEL_PATH, exist_ok=True)
        model_path = os.path.join(settings.MODEL_PATH, "deep_recommendation_model.pth")
        
        torch.save({
            'model_state_dict': self.state_dict(),
            'user_dim': self.user_dim,
            'item_dim': self.item_dim,
            'hidden_dims': self.hidden_dims
        }, model_path)
        
        logger.info(f"Model saved to {model_path}")

class ContentEmbeddingModel:
    """
    Model for generating content embeddings using TensorFlow/Keras.
    Handles both user and item embeddings.
    """
    
    def __init__(self):
        self.embedding_dim = settings.EMBEDDING_DIM
        self.scaler = StandardScaler()
        self.model = None
        self.load_model()
    
    def build_model(self):
        """Build the content embedding model."""
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Model
            from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
            
            # Input layer
            input_layer = Input(shape=(None,))  # Variable input size
            
            # Embedding layers
            x = Dense(256, activation='relu')(input_layer)
            x = BatchNormalization()(x)
            x = Dropout(0.3)(x)
            
            x = Dense(128, activation='relu')(x)
            x = BatchNormalization()(x)
            x = Dropout(0.2)(x)
            
            # Output embedding
            output = Dense(self.embedding_dim, activation='tanh')(x)
            
            model = Model(inputs=input_layer, outputs=output)
            model.compile(optimizer='adam', loss='mse')
            
            self.model = model
            logger.info("Built content embedding model")
            
        except ImportError:
            logger.warning("TensorFlow not available, using fallback embedding generation")
            self.model = None
        except Exception as e:
            logger.error(f"Error building content embedding model: {str(e)}")
            self.model = None
    
    async def generate_user_embedding(self, user_profile: Dict) -> np.ndarray:
        """Generate embedding for a user based on their profile and interactions."""
        try:
            # Extract features from user profile
            features = self._extract_user_features(user_profile)
            
            if self.model is not None:
                # Use trained model
                features_scaled = self.scaler.fit_transform([features])
                embedding = self.model.predict(features_scaled)[0]
            else:
                # Fallback: use feature hashing and dimensionality reduction
                embedding = self._generate_fallback_embedding(features)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating user embedding: {str(e)}")
            # Return random embedding as fallback
            return np.random.randn(self.embedding_dim)
    
    async def generate_post_embedding(self, post) -> np.ndarray:
        """Generate embedding for a post based on its content and metadata."""
        try:
            # Extract features from post
            features = self._extract_post_features(post)
            
            if self.model is not None:
                # Use trained model
                features_scaled = self.scaler.fit_transform([features])
                embedding = self.model.predict(features_scaled)[0]
            else:
                # Fallback: use feature hashing and dimensionality reduction
                embedding = self._generate_fallback_embedding(features)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating post embedding: {str(e)}")
            # Return random embedding as fallback
            return np.random.randn(self.embedding_dim)
    
    def _extract_user_features(self, user_profile: Dict) -> List[float]:
        """Extract numerical features from user profile."""
        features = []
        
        # Basic user features
        features.append(user_profile.get("total_interactions", 0))
        
        # Interaction patterns
        interaction_patterns = user_profile.get("interaction_patterns", {})
        features.append(interaction_patterns.get("engagement_score", 0))
        
        # Interaction type distribution
        interaction_types = interaction_patterns.get("interaction_types", {})
        features.extend([
            interaction_types.get("view", 0),
            interaction_types.get("like", 0),
            interaction_types.get("share", 0),
            interaction_types.get("bookmark", 0),
            interaction_types.get("rate", 0)
        ])
        
        # Preferences (one-hot encoded categories)
        preferences = user_profile.get("preferences", {})
        categories = preferences.get("categories", [])
        
        # Common categories for one-hot encoding
        common_categories = ["Flic", "Motivation", "Education", "Entertainment", "Wellness", "Technology"]
        for category in common_categories:
            features.append(1.0 if category in categories else 0.0)
        
        # Pad or truncate to fixed size
        target_size = 50
        if len(features) < target_size:
            features.extend([0.0] * (target_size - len(features)))
        else:
            features = features[:target_size]
        
        return features
    
    def _extract_post_features(self, post) -> List[float]:
        """Extract numerical features from post."""
        features = []
        
        # Engagement metrics
        features.extend([
            float(post.view_count),
            float(post.upvote_count),
            float(post.comment_count),
            float(post.share_count),
            float(post.bookmark_count),
            float(post.rating_count),
            float(post.average_rating)
        ])
        
        # Content features
        features.append(len(post.title))  # Title length
        features.append(len(post.tags) if post.tags else 0)  # Number of tags
        
        # Category one-hot encoding
        common_categories = ["Flic", "Motivation", "Education", "Entertainment", "Wellness", "Technology"]
        for category in common_categories:
            features.append(1.0 if post.category.name == category else 0.0)
        
        # Temporal features
        from datetime import datetime
        days_since_creation = (datetime.utcnow() - post.created_at).days
        features.append(float(days_since_creation))
        
        # Boolean features
        features.extend([
            1.0 if post.is_available_in_public_feed else 0.0,
            1.0 if post.is_locked else 0.0
        ])
        
        # Pad or truncate to fixed size
        target_size = 50
        if len(features) < target_size:
            features.extend([0.0] * (target_size - len(features)))
        else:
            features = features[:target_size]
        
        return features
    
    def _generate_fallback_embedding(self, features: List[float]) -> np.ndarray:
        """Generate embedding using simple feature hashing when ML models are not available."""
        # Convert features to numpy array
        features_array = np.array(features)
        
        # Simple dimensionality reduction using random projection
        np.random.seed(42)  # For reproducibility
        projection_matrix = np.random.randn(len(features), self.embedding_dim)
        
        # Project features to embedding space
        embedding = np.dot(features_array, projection_matrix)
        
        # Normalize
        embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
        
        return embedding
    
    def load_model(self):
        """Load pre-trained content embedding model."""
        model_path = os.path.join(settings.MODEL_PATH, "content_embedding_model.h5")
        scaler_path = os.path.join(settings.MODEL_PATH, "content_scaler.pkl")
        
        try:
            if os.path.exists(model_path):
                import tensorflow as tf
                self.model = tf.keras.models.load_model(model_path)
                logger.info("Loaded pre-trained content embedding model")
            
            if os.path.exists(scaler_path):
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                logger.info("Loaded content embedding scaler")
                
        except ImportError:
            logger.warning("TensorFlow not available for loading model")
            self.build_model()
        except Exception as e:
            logger.warning(f"Could not load pre-trained content model: {str(e)}")
            self.build_model()
    
    def save_model(self):
        """Save the content embedding model."""
        if self.model is None:
            return
        
        os.makedirs(settings.MODEL_PATH, exist_ok=True)
        
        model_path = os.path.join(settings.MODEL_PATH, "content_embedding_model.h5")
        scaler_path = os.path.join(settings.MODEL_PATH, "content_scaler.pkl")
        
        try:
            self.model.save(model_path)
            
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logger.info("Content embedding model saved")
            
        except Exception as e:
            logger.error(f"Error saving content embedding model: {str(e)}")

class GraphNeuralNetwork:
    """
    Graph Neural Network for capturing user-item and item-item relationships.
    Uses PyTorch Geometric for graph operations.
    """
    
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.build_model()
    
    def build_model(self):
        """Build GNN model for recommendation."""
        try:
            # Try to import PyTorch Geometric
            import torch_geometric
            from torch_geometric.nn import GCNConv, global_mean_pool
            
            class GNNRecommender(nn.Module):
                def __init__(self, num_features, hidden_dim=64):
                    super(GNNRecommender, self).__init__()
                    self.conv1 = GCNConv(num_features, hidden_dim)
                    self.conv2 = GCNConv(hidden_dim, hidden_dim)
                    self.conv3 = GCNConv(hidden_dim, 32)
                    self.classifier = nn.Linear(32, 1)
                    self.dropout = nn.Dropout(0.3)
                
                def forward(self, x, edge_index, batch=None):
                    x = F.relu(self.conv1(x, edge_index))
                    x = self.dropout(x)
                    x = F.relu(self.conv2(x, edge_index))
                    x = self.dropout(x)
                    x = F.relu(self.conv3(x, edge_index))
                    
                    if batch is not None:
                        x = global_mean_pool(x, batch)
                    
                    x = self.classifier(x)
                    return torch.sigmoid(x)
            
            self.model = GNNRecommender(num_features=128).to(self.device)
            logger.info("Built Graph Neural Network model")
            
        except ImportError:
            logger.warning("PyTorch Geometric not available, GNN features disabled")
            self.model = None
        except Exception as e:
            logger.error(f"Error building GNN model: {str(e)}")
            self.model = None
    
    async def get_graph_recommendations(self, user_id: int, candidate_items: List[int], db) -> List[float]:
        """Get recommendations using graph neural network."""
        if self.model is None:
            # Return random scores as fallback
            return [np.random.random() for _ in candidate_items]
        
        try:
            # Build graph from user interactions
            graph_data = await self._build_interaction_graph(user_id, candidate_items, db)
            
            if graph_data is None:
                return [np.random.random() for _ in candidate_items]
            
            self.model.eval()
            with torch.no_grad():
                predictions = self.model(graph_data.x, graph_data.edge_index)
                return predictions.cpu().numpy().tolist()
                
        except Exception as e:
            logger.error(f"Error in GNN recommendations: {str(e)}")
            return [np.random.random() for _ in candidate_items]
    
    async def _build_interaction_graph(self, user_id: int, candidate_items: List[int], db):
        """Build interaction graph for GNN processing."""
        # This would require implementing graph construction from user interactions
        # For now, return None to indicate graph construction is not implemented
        return None