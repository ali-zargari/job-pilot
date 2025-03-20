"""
ResumeGPT module for enhancing resume bullets with fine-tuned T5 model.
This module provides functionality to transform resume bullet points into more impactful statements.
"""

from .infer import (
    ResumeEnhancer,
    enhance_bullet,
    enhance_resume,
    get_enhancer
)

__all__ = [
    'ResumeEnhancer',
    'enhance_bullet',
    'enhance_resume',
    'get_enhancer'
]

__version__ = '0.1.0' 