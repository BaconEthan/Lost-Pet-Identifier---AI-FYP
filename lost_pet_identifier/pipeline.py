"""
Main pipeline orchestrator that connects all components.
"""

import os
from typing import Optional, Dict, Any, List
from pathlib import Path

from .ingestion import DataIngestion
from .embeddings import CLIPEmbedder
from .llm_extractor import LLMFeatureExtractor
from .vector_db import VectorDatabase
from .matcher import SimilarityMatcher
from .explainer import ResultExplainer


class LostPetIdentifier:
    """Main orchestrator for the lost pet identification system."""
    
    def __init__(
        self,
        clip_model: str = "ViT-B/32",
        ollama_url: str = "http://localhost:11434",
        ollama_model: str = "llama2",
        vector_db_path: Optional[str] = None,
        device: Optional[str] = None
    ):
        """
        Initialize the lost pet identifier system.
        
        Args:
            clip_model: CLIP model name
            ollama_url: Ollama API base URL
            ollama_model: Ollama model name
            vector_db_path: Path to save/load vector database
            device: Device for CLIP ('cuda', 'cpu', or None for auto)
        """
        # Initialize components
        self.ingestion = DataIngestion()
        self.embedder = CLIPEmbedder(model_name=clip_model, device=device)
        self.llm_extractor = LLMFeatureExtractor(
            base_url=ollama_url,
            model=ollama_model
        )
        
        # Initialize vector database
        embedding_dim = self.embedder.get_embedding_dim()
        self.vector_db = VectorDatabase(
            embedding_dim=embedding_dim,
            index_path=vector_db_path
        )
        
        # Initialize matcher and explainer
        self.matcher = SimilarityMatcher(
            embedder=self.embedder,
            vector_db=self.vector_db
        )
        self.explainer = ResultExplainer(llm_extractor=self.llm_extractor)
    
    def add_found_pet(
        self,
        image_path: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        date: Optional[str] = None,
        additional_metadata: Optional[Dict[str, Any]] = None,
        save_index: bool = True
    ) -> int:
        """
        Add a found pet to the database.
        
        Args:
            image_path: Path to pet image
            description: Text description
            location: Location information
            date: Date information
            additional_metadata: Additional metadata fields
            save_index: Whether to save the index after adding
            
        Returns:
            Index of the added pet in the database
        """
        # Load and validate image if provided
        image = None
        if image_path:
            image = self.ingestion.load_image(image_path)
        
        # Extract structured features from description
        if description:
            features = self.llm_extractor.extract_features(description)
            normalized_text = self.llm_extractor.features_to_text(features)
        else:
            features = {}
            normalized_text = ""
        
        # Generate embedding
        embedding = self.embedder.embed_multimodal(
            image=image,
            text=normalized_text if normalized_text else description,
            fusion_method="average"
        )
        
        # Create metadata
        metadata = self.ingestion.create_metadata(
            image_path=image_path,
            description=description,
            location=location,
            date=date,
            additional_info={
                **(additional_metadata or {}),
                "extracted_features": features,
                "normalized_text": normalized_text
            }
        )
        
        # Add to vector database
        self.vector_db.add(embedding, metadata)
        
        # Save index if requested
        if save_index and self.vector_db.index_path:
            self.vector_db.save()
        
        return self.vector_db.size() - 1
    
    def search_lost_pet(
        self,
        image_path: Optional[str] = None,
        description: Optional[str] = None,
        k: int = 5,
        include_explanation: bool = True,
        fusion_method: str = "average"
    ) -> Dict[str, Any]:
        """
        Search for a lost pet in the database.
        
        Args:
            image_path: Path to lost pet image
            description: Text description of lost pet
            k: Number of top results to return
            include_explanation: Whether to include LLM-generated explanation
            fusion_method: How to combine image/text embeddings ('average', 'image_only', 'text_only')
            
        Returns:
            Dictionary with results and optional explanation
        """
        # Load image if provided
        image = None
        if image_path:
            image = self.ingestion.load_image(image_path)
        
        # Extract features from description
        normalized_text = description
        if description:
            features = self.llm_extractor.extract_features(description)
            normalized_text = self.llm_extractor.features_to_text(features)
        
        # Perform matching
        results = self.matcher.match(
            image=image,
            text=normalized_text if normalized_text else description,
            k=k,
            fusion_method=fusion_method
        )
        
        # Generate explanation if requested
        explanation = None
        if include_explanation:
            query_desc = description or "image-based search"
            explanation = self.explainer.explain_results(query_desc, results, top_n=min(3, k))
        
        return {
            "results": results,
            "explanation": explanation,
            "query": {
                "has_image": image is not None,
                "description": description,
                "normalized_description": normalized_text,
                "fusion_method": fusion_method
            }
        }
    
    def save_database(self, path: Optional[str] = None):
        """Save the vector database to disk."""
        self.vector_db.save(path)
    
    def load_database(self, path: str):
        """Load the vector database from disk."""
        self.vector_db.load(path)
    
    def get_database_size(self) -> int:
        """Get the number of pets in the database."""
        return self.vector_db.size()
    
    def clear_database(self):
        """Clear all entries from the database."""
        self.vector_db.clear()

