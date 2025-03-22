"""
OpenAI integration module for AI-powered resume enhancements.
"""

from .client import (
    get_openai_client,
    OpenAIClient,
    check_api_key
)

from .embeddings import (
    get_embedding,
    calculate_similarity,
    get_document_similarity
)

from .text_generation import (
    generate_text,
    enhance_text,
    rewrite_resume
)

__all__ = [
    'get_openai_client',
    'OpenAIClient',
    'check_api_key',
    'get_embedding',
    'calculate_similarity',
    'get_document_similarity',
    'generate_text',
    'enhance_text',
    'rewrite_resume'
]

__version__ = '0.1.0' 