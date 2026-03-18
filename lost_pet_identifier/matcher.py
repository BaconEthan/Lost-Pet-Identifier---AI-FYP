"""
Similarity matching engine for ranking pet matches.
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from .embeddings import CLIPEmbedder
from .vector_db import VectorDatabase


class SimilarityMatcher:
    """Matches lost pets against found pets using similarity scores."""
    
    def __init__(
        self,
        embedder: CLIPEmbedder,
        vector_db: VectorDatabase
    ):
        """
        Initialize similarity matcher.
        
        Args:
            embedder: CLIP embedder instance
            vector_db: Vector database instance
        """
        self.embedder = embedder
        self.vector_db = vector_db
    
    def match(
        self,
        image: Optional[Any] = None,
        text: Optional[str] = None,
        k: int = 5,
        fusion_method: str = "average"
    ) -> List[Dict[str, Any]]:
        """
        Match a lost pet query against the database.
        
        Args:
            image: PIL Image or path to image
            text: Text description
            k: Number of top results to return
            fusion_method: How to combine image/text embeddings
            
        Returns:
            List of match results with similarity scores and metadata
        """
        # Generate query embedding
        query_embedding = self.embedder.embed_multimodal(
            image=image,
            text=text,
            fusion_method=fusion_method
        )
        
        # Search in vector database
        results = self.vector_db.search(query_embedding, k=k)
        
        # Format results
        formatted_results = []
        for similarity, metadata in results:
            result = {
                "similarity_score": float(similarity),
                "metadata": metadata,
                "image_path": metadata.get("image_path"),
                "description": metadata.get("description", ""),
                "location": metadata.get("location"),
                "date": metadata.get("date")
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def match_image_only(self, image: Any, k: int = 5) -> List[Dict[str, Any]]:
        """Match using image only."""
        return self.match(image=image, text=None, k=k, fusion_method="image_only")
    
    def match_text_only(self, text: str, k: int = 5) -> List[Dict[str, Any]]:
        """Match using text only."""
        return self.match(image=None, text=text, k=k, fusion_method="text_only")

