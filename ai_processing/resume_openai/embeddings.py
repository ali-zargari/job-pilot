"""
OpenAI embeddings module for generating and comparing text embeddings.
"""

import logging
import numpy as np
from typing import List, Optional, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity

from .client import get_openai_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def get_embedding(
    text: str,
    model: str = "text-embedding-ada-002",
    api_key: Optional[str] = None
) -> List[float]:
    """
    Get embedding vector for text using OpenAI's API.
    
    Args:
        text: Text to get embedding for
        model: Embedding model to use
        api_key: Optional API key override
        
    Returns:
        Embedding vector or empty list if API unavailable
    """
    if not text:
        return []
        
    # Get client
    client = get_openai_client(api_key=api_key)
    
    # Check if client is available
    if not client.is_available or not client.get_client():
        logger.warning("OpenAI client not available for embeddings")
        return []
    
    try:
        # Call OpenAI API
        response = client.get_client().embeddings.create(
            input=text,
            model=model
        )
        
        # Increment API call counter
        client.increment_api_call_count()
        
        # Return embedding vector
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        return []

def calculate_similarity(
    embedding1: List[float],
    embedding2: List[float]
) -> float:
    """
    Calculate cosine similarity between two embeddings.
    
    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector
        
    Returns:
        Similarity score (0-1)
    """
    # Check for valid embeddings
    if not embedding1 or not embedding2:
        return 0.0
        
    try:
        # Reshape for sklearn
        e1 = np.array(embedding1).reshape(1, -1)
        e2 = np.array(embedding2).reshape(1, -1)
        
        # Calculate cosine similarity
        return float(cosine_similarity(e1, e2)[0][0])
    except Exception as e:
        logger.error(f"Error calculating similarity: {str(e)}")
        return 0.0

def get_document_similarity(
    doc1: str,
    doc2: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate similarity between two text documents.
    
    Args:
        doc1: First document text
        doc2: Second document text
        api_key: Optional API key override
        
    Returns:
        Dictionary with similarity score and stats
    """
    # Get embeddings
    embedding1 = get_embedding(doc1, api_key=api_key)
    embedding2 = get_embedding(doc2, api_key=api_key)
    
    # Calculate similarity
    similarity = calculate_similarity(embedding1, embedding2)
    
    return {
        "similarity": similarity,
        "embedding1_length": len(embedding1) if embedding1 else 0,
        "embedding2_length": len(embedding2) if embedding2 else 0,
        "has_valid_embeddings": bool(embedding1 and embedding2)
    } 