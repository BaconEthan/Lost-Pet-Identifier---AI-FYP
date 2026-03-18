"""
LLaMA integration for semantic feature extraction from unstructured text.
"""

import json
import requests
from typing import Dict, Any, Optional
import os


class LLMFeatureExtractor:
    """Extracts structured features from unstructured text using LLaMA via Ollama."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama2",
        timeout: int = 60
    ):
        """
        Initialize LLM feature extractor.
        
        Args:
            base_url: Base URL for Ollama API
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        self.api_url = f"{self.base_url}/api/generate"
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API to generate response.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text response
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for more deterministic extraction
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except requests.exceptions.RequestException as e:
            print(f"Warning: Ollama API call failed: {e}")
            print("Falling back to basic text normalization.")
            return ""
    
    def extract_features(self, description: str) -> Dict[str, Any]:
        """
        Extract structured features from unstructured pet description.
        
        Args:
            description: Free-text description of the pet
            
        Returns:
            Dictionary with structured features
        """
        if not description or not description.strip():
            return self._default_features()
        
        prompt = self._create_extraction_prompt(description)
        llm_response = self._call_ollama(prompt)
        
        # Try to parse JSON from response
        features = self._parse_json_response(llm_response, description)
        
        return features
    
    def _create_extraction_prompt(self, description: str) -> str:
        """Create prompt for feature extraction."""
        return f"""Extract structured information about a pet from the following description. 
Return ONLY a valid JSON object with no additional text, comments, or markdown formatting.

Description: "{description}"

Extract the following information and return as JSON:
{{
  "species": "dog" | "cat" | "bird" | "other" | null,
  "size": "small" | "medium" | "large" | null,
  "color": ["array", "of", "colors"],
  "breed": "breed name or null",
  "distinctive_features": ["array", "of", "distinctive", "features"],
  "temperament": "temperament description or null",
  "age": "age estimate or null"
}}

JSON:"""
    
    def _parse_json_response(self, response: str, original_description: str) -> Dict[str, Any]:
        """
        Parse JSON from LLM response, with fallback to basic extraction.
        
        Args:
            response: LLM response text
            original_description: Original description for fallback
            
        Returns:
            Parsed features dictionary
        """
        # Try to extract JSON from response
        response = response.strip()
        
        # Remove markdown code blocks if present
        if response.startswith("```"):
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1]) if len(lines) > 2 else response
        
        # Try to parse as JSON
        try:
            features = json.loads(response)
            # Validate structure
            return self._validate_features(features)
        except json.JSONDecodeError:
            # Fallback to basic extraction
            return self._basic_extraction(original_description)
    
    def _validate_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize feature structure."""
        default = self._default_features()
        
        # Ensure all required keys exist
        for key in default.keys():
            if key not in features:
                features[key] = default[key]
        
        # Normalize types
        if not isinstance(features.get("color"), list):
            features["color"] = [features["color"]] if features.get("color") else []
        
        if not isinstance(features.get("distinctive_features"), list):
            features["distinctive_features"] = (
                [features["distinctive_features"]] 
                if features.get("distinctive_features") else []
            )
        
        return features
    
    def _default_features(self) -> Dict[str, Any]:
        """Return default feature structure."""
        return {
            "species": None,
            "size": None,
            "color": [],
            "breed": None,
            "distinctive_features": [],
            "temperament": None,
            "age": None
        }
    
    def _basic_extraction(self, description: str) -> Dict[str, Any]:
        """
        Basic keyword-based extraction as fallback.
        
        Args:
            description: Original description
            
        Returns:
            Basic features dictionary
        """
        description_lower = description.lower()
        features = self._default_features()
        
        # Simple keyword matching
        if any(word in description_lower for word in ["dog", "puppy", "canine"]):
            features["species"] = "dog"
        elif any(word in description_lower for word in ["cat", "kitten", "feline"]):
            features["species"] = "cat"
        elif any(word in description_lower for word in ["bird", "parrot", "canary"]):
            features["species"] = "bird"
        
        # Size detection
        if any(word in description_lower for word in ["small", "tiny", "little"]):
            features["size"] = "small"
        elif any(word in description_lower for word in ["large", "big", "huge"]):
            features["size"] = "large"
        elif any(word in description_lower for word in ["medium", "mid"]):
            features["size"] = "medium"
        
        # Color detection (basic)
        color_keywords = ["brown", "black", "white", "gray", "grey", "golden", "red", "orange", "yellow"]
        detected_colors = [color for color in color_keywords if color in description_lower]
        if detected_colors:
            features["color"] = detected_colors
        
        return features
    
    def features_to_text(self, features: Dict[str, Any]) -> str:
        """
        Convert structured features back to normalized text string.
        
        Args:
            features: Structured features dictionary
            
        Returns:
            Normalized text description
        """
        parts = []
        
        if features.get("size"):
            parts.append(features["size"])
        
        if features.get("color"):
            parts.extend(features["color"])
        
        if features.get("species"):
            parts.append(features["species"])
        
        if features.get("breed"):
            parts.append(features["breed"])
        
        if features.get("distinctive_features"):
            parts.extend(features["distinctive_features"])
        
        if features.get("temperament"):
            parts.append(features["temperament"])
        
        return ", ".join(parts) if parts else ""

