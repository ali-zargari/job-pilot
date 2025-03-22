"""
OpenAI client module for handling API connections and client management.
"""

import os
import logging
from typing import Optional, Dict, Any
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class OpenAIClient:
    """
    A wrapper for the OpenAI client with error handling and configuration.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        default_model: str = "gpt-3.5-turbo",
        embedding_model: str = "text-embedding-ada-002",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ):
        """
        Initialize the OpenAI client.
        
        Args:
            api_key: OpenAI API key (optional if set in environment)
            default_model: Default model for text generation
            embedding_model: Model to use for embeddings
            max_tokens: Default max tokens for generation
            temperature: Default temperature for generation
        """
        self.default_model = default_model
        self.embedding_model = embedding_model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = None
        self.api_calls_count = 0
        self.api_call_cache = {}  # Cache API calls to avoid redundant requests
        self.is_available = False
        
        # Initialize the client
        self._init_client(api_key)
    
    def _init_client(self, api_key: Optional[str]) -> None:
        """Initialize the OpenAI client with error handling."""
        try:
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                # Try to use environment variable
                self.client = OpenAI()
            self.is_available = True
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize OpenAI client: {str(e)}")
            self.is_available = False
            self.client = None
    
    def check_availability(self) -> bool:
        """
        Test the OpenAI connection to verify it's working.
        
        Returns:
            bool: True if the connection is working, False otherwise
        """
        if not self.client:
            return False
            
        try:
            # Simple API test
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello in one word."}
                ],
                max_tokens=10
            )
            
            # If we got here, the API is working
            self.is_available = True
            return True
        except Exception as e:
            logger.warning(f"OpenAI API test failed: {str(e)}")
            self.is_available = False
            return False
    
    def get_client(self) -> Optional[OpenAI]:
        """
        Get the OpenAI client instance.
        
        Returns:
            OpenAI client or None if not available
        """
        return self.client
    
    def increment_api_call_count(self) -> int:
        """
        Increment the API call counter.
        
        Returns:
            int: New API call count
        """
        self.api_calls_count += 1
        return self.api_calls_count
    
    def get_api_call_count(self) -> int:
        """
        Get the current API call count.
        
        Returns:
            int: API call count
        """
        return self.api_calls_count

# Singleton instance
_client_instance = None

def get_openai_client(
    api_key: Optional[str] = None,
    default_model: str = "gpt-3.5-turbo",
    embedding_model: str = "text-embedding-ada-002",
    force_new: bool = False
) -> OpenAIClient:
    """
    Get or create a singleton OpenAIClient instance.
    
    Args:
        api_key: OpenAI API key (optional if set in environment)
        default_model: Default model for text generation
        embedding_model: Model to use for embeddings
        force_new: Force creation of a new instance
        
    Returns:
        OpenAIClient: Configured OpenAI client wrapper
    """
    global _client_instance
    
    # Create new instance if needed
    if _client_instance is None or force_new:
        _client_instance = OpenAIClient(
            api_key=api_key,
            default_model=default_model,
            embedding_model=embedding_model
        )
        
    return _client_instance

def check_api_key(api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Check if the OpenAI API key is valid and working.
    
    Args:
        api_key: OpenAI API key to check
        
    Returns:
        Dict with status information
    """
    client = get_openai_client(api_key=api_key, force_new=True)
    is_working = client.check_availability()
    
    return {
        "is_valid": is_working,
        "client_available": client.is_available,
        "client_initialized": client.client is not None,
        "message": "API key is valid and working" if is_working else "API key is invalid or API not accessible"
    } 