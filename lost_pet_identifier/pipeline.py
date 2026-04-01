"""
Main pipeline orchestrator that connects all components.
"""

import os
from typing import Optional, Dict, Any, List
from pathlib import Path

from .ingestion import DataIngestion
from .embeddings import CLIPEmbedder
from .llm_extractor import LLMFeatureExtractor
from .birdnet_classifier import BirdNetClassifier
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
        device: Optional[str] = None,
        enable_birdnet: bool = True,
        birdnet_min_confidence: float = 0.1,
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

        self.birdnet_min_confidence = float(birdnet_min_confidence)
        self.birdnet = BirdNetClassifier() if enable_birdnet else None
        
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
        audio_path: Optional[str] = None,
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

        # Optional audio -> BirdNET -> (text prompt + metadata)
        birdnet_text = ""
        birdnet_features: Dict[str, Any] = {}
        if audio_path and self.birdnet is not None and getattr(self.birdnet, "available", False):
            detections = self.birdnet.analyze(audio_path, min_confidence=self.birdnet_min_confidence)
            birdnet_text = self.birdnet.format_for_clip(detections)
            birdnet_features = self.birdnet.to_metadata(detections)
        
        # Extract structured features from description
        if description:
            features = self.llm_extractor.extract_features(description)
            normalized_text = self.llm_extractor.features_to_text(features)
        else:
            features = {}
            normalized_text = ""
        
        # Combine text signals (LLM-normalized + BirdNET prompt if present)
        text_parts: List[str] = []
        if normalized_text and normalized_text.strip():
            text_parts.append(normalized_text)
        elif description:
            text_parts.append(description)
        if birdnet_text:
            text_parts.append(birdnet_text)
        combined_text = " | ".join(text_parts)

        # Generate embedding
        embedding = self.embedder.embed_multimodal(
            image=image,
            text=combined_text,
            fusion_method="average"
        )
        
        # Create metadata
        metadata = self.ingestion.create_metadata(
            image_path=image_path,
            audio_path=audio_path,
            description=description,
            location=location,
            date=date,
            additional_info={
                **(additional_metadata or {}),
                "extracted_features": features,
                "normalized_text": normalized_text,
                "birdnet_text": birdnet_text,
                **birdnet_features,
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
        audio_path: Optional[str] = None,
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

        birdnet_text = ""
        if audio_path and self.birdnet is not None and getattr(self.birdnet, "available", False):
            detections = self.birdnet.analyze(audio_path, min_confidence=self.birdnet_min_confidence)
            birdnet_text = self.birdnet.format_for_clip(detections)

        # Combine description + BirdNET prompt
        text_parts: List[str] = []
        if normalized_text and normalized_text.strip():
            text_parts.append(normalized_text)
        elif description:
            text_parts.append(description)
        if birdnet_text:
            text_parts.append(birdnet_text)
        combined_text = " | ".join(text_parts) if text_parts else None
        
        # Perform matching
        results = self.matcher.match(
            image=image,
            text=combined_text,
            k=k,
            fusion_method=fusion_method
        )
        
        # Generate explanation if requested
        explanation = None
        if include_explanation:
            query_desc_parts: List[str] = []
            if description:
                query_desc_parts.append(description)
            if birdnet_text:
                query_desc_parts.append(f"(audio: {birdnet_text})")
            query_desc = " ".join(query_desc_parts) if query_desc_parts else "image-based search"
            explanation = self.explainer.explain_results(query_desc, results, top_n=min(3, k))
        
        return {
            "results": results,
            "explanation": explanation,
            "query": {
                "has_image": image is not None,
                "has_audio": bool(audio_path),
                "audio_path": audio_path,
                "description": description,
                "normalized_description": normalized_text,
                "birdnet_text": birdnet_text,
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

