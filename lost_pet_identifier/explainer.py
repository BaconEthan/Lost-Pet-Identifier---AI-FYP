"""
LLaMA-based explanation generation for search results.
"""

from typing import List, Dict, Any
from .llm_extractor import LLMFeatureExtractor


class ResultExplainer:
    """Generates natural language explanations for search results."""
    
    def __init__(self, llm_extractor: LLMFeatureExtractor):
        """
        Initialize result explainer.
        
        Args:
            llm_extractor: LLM feature extractor instance (reused for API calls)
        """
        self.llm_extractor = llm_extractor
    
    def explain_results(
        self,
        query_description: str,
        results: List[Dict[str, Any]],
        top_n: int = 3
    ) -> str:
        """
        Generate explanation for why certain results were ranked highly.
        
        Args:
            query_description: Original query description
            results: List of search results
            top_n: Number of top results to explain
            
        Returns:
            Natural language explanation
        """
        if not results:
            return "No matches found in the database."
        
        top_results = results[:top_n]
        
        # Build explanation prompt
        prompt = self._create_explanation_prompt(query_description, top_results)
        
        # Get explanation from LLM
        explanation = self.llm_extractor._call_ollama(prompt)
        
        # Fallback if LLM fails
        if not explanation or len(explanation.strip()) < 10:
            explanation = self._generate_fallback_explanation(top_results)
        
        return explanation.strip()
    
    def _create_explanation_prompt(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> str:
        """Create prompt for explanation generation."""
        results_text = ""
        for i, result in enumerate(results, 1):
            similarity = result.get("similarity_score", 0)
            desc = result.get("description", "No description")
            results_text += f"\n{i}. Similarity: {similarity:.3f} - {desc}\n"
        
        return f"""Explain why these pet matches were ranked as the most similar to the query. 
Be concise (2-3 sentences) and focus on shared visual or descriptive features.

Query: "{query}"

Top Matches:
{results_text}

Explanation:"""
    
    def _generate_fallback_explanation(self, results: List[Dict[str, Any]]) -> str:
        """Generate a basic explanation if LLM fails."""
        if not results:
            return "No matches found."
        
        top_result = results[0]
        similarity = top_result.get("similarity_score", 0)
        
        explanation = f"The top match has a similarity score of {similarity:.2f}. "
        
        if similarity > 0.7:
            explanation += "This indicates a strong visual or descriptive similarity."
        elif similarity > 0.5:
            explanation += "This indicates moderate similarity - please review carefully."
        else:
            explanation += "This indicates low similarity - consider expanding your search."
        
        return explanation

