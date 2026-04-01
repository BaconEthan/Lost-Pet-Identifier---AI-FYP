"""
Data ingestion module for processing images, text, and audio inputs.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from PIL import Image
import json


class DataIngestion:
    """Handles ingestion and preprocessing of multimodal data."""
    
    def __init__(self, max_image_size: tuple = (512, 512)):
        """
        Initialize the data ingestion module.
        
        Args:
            max_image_size: Maximum dimensions for image resizing (width, height)
        """
        self.max_image_size = max_image_size
    
    def load_image(self, image_path: str) -> Image.Image:
        """
        Load and preprocess an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            PIL Image object
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large (maintain aspect ratio)
        image.thumbnail(self.max_image_size, Image.Resampling.LANCZOS)
        
        return image
    
    def validate_text(self, text: Optional[str]) -> str:
        """
        Validate and normalize text input.
        
        Args:
            text: Input text description
            
        Returns:
            Normalized text string (empty string if None)
        """
        if text is None:
            return ""
        
        # Basic normalization
        text = text.strip()
        return text
    
    def create_metadata(
        self,
        image_path: Optional[str] = None,
        audio_path: Optional[str] = None,
        description: Optional[str] = None,
        location: Optional[str] = None,
        date: Optional[str] = None,
        additional_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create metadata dictionary for a pet post.
        
        Args:
            image_path: Path to the image
            description: Text description
            location: Location information
            date: Date information
            additional_info: Additional metadata fields
            
        Returns:
            Metadata dictionary
        """
        metadata = {
            "image_path": image_path,
            "audio_path": audio_path,
            "description": description or "",
            "location": location,
            "date": date,
            "has_image": image_path is not None and os.path.exists(image_path) if image_path else False,
            "has_audio": audio_path is not None and os.path.exists(audio_path) if audio_path else False,
            "has_text": bool(description and description.strip())
        }
        
        if additional_info:
            metadata.update(additional_info)
        
        return metadata
    
    def save_metadata(self, metadata: Dict[str, Any], output_path: str):
        """
        Save metadata to a JSON file.
        
        Args:
            metadata: Metadata dictionary
            output_path: Path to save the JSON file
        """
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

