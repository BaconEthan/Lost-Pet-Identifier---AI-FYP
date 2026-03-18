"""
CLIP embedding generation for images and text.
"""

import torch
import clip
from PIL import Image
from typing import Union, List, Optional
import numpy as np
import os


class CLIPEmbedder:
    """Generates embeddings using CLIP model for images and text."""
    
    def __init__(self, model_name: str = "ViT-B/32", device: Optional[str] = None):
        """
        Initialize CLIP embedder.
        
        Args:
            model_name: CLIP model name (e.g., "ViT-B/32", "ViT-L/14")
            device: Device to run on ('cuda', 'cpu', or None for auto)
        """
        self.model_name = model_name
        
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        print(f"Loading CLIP model: {model_name} on {self.device}")
        self.model, self.preprocess = clip.load(model_name, device=self.device)
        self.model.eval()
        
        # Get embedding dimension
        with torch.no_grad():
            dummy_text = clip.tokenize(["dummy"]).to(self.device)
            self.embedding_dim = self.model.encode_text(dummy_text).shape[1]
    
    def embed_image(self, image: Union[Image.Image, str]) -> np.ndarray:
        """
        Generate embedding for an image.
        
        Args:
            image: PIL Image or path to image file
            
        Returns:
            Normalized embedding vector as numpy array
        """
        if isinstance(image, str):
            from PIL import Image
            image = Image.open(image)
        
        # Preprocess and encode
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor)
            # Normalize to unit vector for cosine similarity
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        return image_features.cpu().numpy().flatten()
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for text.
        
        Args:
            text: Input text string
            
        Returns:
            Normalized embedding vector as numpy array
        """
        if not text or not text.strip():
            # Return zero vector if text is empty
            return np.zeros(self.embedding_dim)
        
        # Tokenize and encode
        text_tokens = clip.tokenize([text], truncate=True).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            # Normalize to unit vector for cosine similarity
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
        
        return text_features.cpu().numpy().flatten()
    
    def embed_multimodal(
        self,
        image: Optional[Union[Image.Image, str]] = None,
        text: Optional[str] = None,
        fusion_method: str = "average"
    ) -> np.ndarray:
        """
        Generate combined embedding from image and text.
        
        Args:
            image: PIL Image or path to image file
            text: Text description
            fusion_method: How to combine embeddings ('average', 'image_only', 'text_only')
            
        Returns:
            Combined normalized embedding vector
        """
        embeddings = []
        
        if image is not None and fusion_method != "text_only":
            img_emb = self.embed_image(image)
            embeddings.append(img_emb)
        
        if text and text.strip() and fusion_method != "image_only":
            txt_emb = self.embed_text(text)
            embeddings.append(txt_emb)
        
        if not embeddings:
            raise ValueError("At least one of image or text must be provided")
        
        if fusion_method == "average" and len(embeddings) > 1:
            # Average the embeddings and re-normalize
            combined = np.mean(embeddings, axis=0)
            combined = combined / np.linalg.norm(combined)
            return combined
        else:
            # Return the single embedding
            return embeddings[0]
    
    def get_embedding_dim(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        return self.embedding_dim

