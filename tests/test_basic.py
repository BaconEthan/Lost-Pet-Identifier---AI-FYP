"""
Basic tests for the Lost Pet Identifier system.
"""

import os
import sys
import tempfile
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lost_pet_identifier import LostPetIdentifier
from lost_pet_identifier.embeddings import CLIPEmbedder
from lost_pet_identifier.vector_db import VectorDatabase
from lost_pet_identifier.llm_extractor import LLMFeatureExtractor


def test_clip_embedder():
    """Test CLIP embedding generation."""
    print("Testing CLIP embedder...")
    embedder = CLIPEmbedder()
    
    # Test text embedding
    text_emb = embedder.embed_text("small brown dog")
    assert text_emb.shape == (embedder.get_embedding_dim(),)
    assert np.abs(np.linalg.norm(text_emb) - 1.0) < 0.01  # Should be normalized
    
    print("CLIP embedder test passed")


def test_vector_db():
    """Test vector database operations."""
    print("Testing vector database...")
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        db_path = tmp.name
    
    try:
        db = VectorDatabase(embedding_dim=512, index_path=db_path)
        
        # Add some test embeddings
        for i in range(5):
            emb = np.random.rand(512).astype('float32')
            emb = emb / np.linalg.norm(emb)  # Normalize
            metadata = {"id": i, "description": f"test pet {i}"}
            db.add(emb, metadata)
        
        assert db.size() == 5
        
        # Test search
        query = np.random.rand(512).astype('float32')
        query = query / np.linalg.norm(query)
        results = db.search(query, k=3)
        
        assert len(results) == 3
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)
        
        # Test save/load
        db.save()
        db2 = VectorDatabase(embedding_dim=512, index_path=db_path)
        assert db2.size() == 5
        
        print("Vector database test passed")
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
        if os.path.exists(db_path + ".metadata"):
            os.unlink(db_path + ".metadata")


def test_llm_extractor():
    """Test LLM feature extraction (may fail if Ollama not running)."""
    print("Testing LLM extractor...")
    
    extractor = LLMFeatureExtractor()
    
    # Test basic extraction (will use fallback if Ollama not available)
    features = extractor.extract_features("small brown dog with floppy ears")
    
    assert isinstance(features, dict)
    assert "species" in features
    assert "color" in features
    
    print("LLM extractor test passed (may have used fallback)")


def test_pipeline():
    """Test the main pipeline."""
    print("Testing main pipeline...")
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        db_path = tmp.name
    
    try:
        identifier = LostPetIdentifier(vector_db_path=db_path)
        
        # Add a found pet
        idx = identifier.add_found_pet(
            description="small brown dog with floppy ears",
            location="Test Location"
        )
        
        assert identifier.get_database_size() == 1
        
        # Search
        results = identifier.search_lost_pet(
            description="brown dog",
            k=3
        )
        
        assert len(results['results']) > 0
        
        print("Pipeline test passed")
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
        if os.path.exists(db_path + ".metadata"):
            os.unlink(db_path + ".metadata")


if __name__ == "__main__":
    print("Running basic tests...\n")
    
    try:
        test_clip_embedder()
        test_vector_db()
        test_llm_extractor()
        test_pipeline()
        
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()

