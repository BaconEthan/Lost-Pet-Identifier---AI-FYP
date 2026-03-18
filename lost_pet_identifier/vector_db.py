"""
FAISS vector database for storing and retrieving embeddings.
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any, Optional, Tuple
import json


class VectorDatabase:
    """FAISS-based vector database for pet embeddings."""
    
    def __init__(self, embedding_dim: int, index_path: Optional[str] = None):
        """
        Initialize vector database.
        
        Args:
            embedding_dim: Dimension of embedding vectors
            index_path: Path to save/load FAISS index
        """
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        
        # Initialize FAISS index (L2 distance, but we'll use cosine similarity)
        # Using inner product since embeddings are normalized
        self.index = faiss.IndexFlatIP(embedding_dim)
        
        # Metadata storage: list of dicts, one per vector
        self.metadata: List[Dict[str, Any]] = []
        
        # Load existing index if path provided and exists and has content
        if index_path and os.path.exists(index_path) and os.path.getsize(index_path) > 0:
            try:
                self.load(index_path)
            except Exception:
                # If loading fails, start with empty index
                self.index = faiss.IndexFlatIP(embedding_dim)
                self.metadata = []
    
    def add(
        self,
        embedding: np.ndarray,
        metadata: Dict[str, Any]
    ):
        """
        Add an embedding with metadata to the database.
        
        Args:
            embedding: Normalized embedding vector
            metadata: Associated metadata dictionary
        """
        # Ensure embedding is normalized and right shape
        embedding = embedding.flatten()
        if len(embedding) != self.embedding_dim:
            raise ValueError(
                f"Embedding dimension mismatch: expected {self.embedding_dim}, "
                f"got {len(embedding)}"
            )
        
        # Normalize to unit vector
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        # Add to FAISS index
        embedding_2d = embedding.reshape(1, -1).astype('float32')
        self.index.add(embedding_2d)
        
        # Store metadata
        self.metadata.append(metadata.copy())
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Search for k most similar embeddings.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of (similarity_score, metadata) tuples, sorted by similarity
        """
        if self.index.ntotal == 0:
            return []
        
        # Normalize query embedding
        query_embedding = query_embedding.flatten()
        norm = np.linalg.norm(query_embedding)
        if norm > 0:
            query_embedding = query_embedding / norm
        
        # Prepare query
        query_2d = query_embedding.reshape(1, -1).astype('float32')
        
        # Search (k+1 to handle potential self-match)
        k_actual = min(k + 1, self.index.ntotal)
        distances, indices = self.index.search(query_2d, k_actual)
        
        # Convert distances to similarity scores (inner product = cosine for normalized vectors)
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                # Inner product is already cosine similarity for normalized vectors
                similarity = float(distance)
                results.append((similarity, self.metadata[idx].copy()))
        
        # Sort by similarity (descending) and return top k
        results.sort(key=lambda x: x[0], reverse=True)
        return results[:k]
    
    def save(self, index_path: Optional[str] = None):
        """
        Save the index and metadata to disk.
        
        Args:
            index_path: Path to save (uses self.index_path if None)
        """
        path = index_path or self.index_path
        if not path:
            raise ValueError("No index path provided")
        
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, path)
        
        # Save metadata
        metadata_path = path + ".metadata"
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load(self, index_path: Optional[str] = None):
        """
        Load the index and metadata from disk.
        
        Args:
            index_path: Path to load (uses self.index_path if None)
        """
        path = index_path or self.index_path
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Index not found: {path}")
        
        # Load FAISS index
        self.index = faiss.read_index(path)
        
        # Load metadata
        metadata_path = path + ".metadata"
        if os.path.exists(metadata_path):
            with open(metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
        else:
            self.metadata = []
    
    def size(self) -> int:
        """Get the number of vectors in the database."""
        return self.index.ntotal
    
    def clear(self):
        """Clear all vectors and metadata."""
        self.index.reset()
        self.metadata = []

