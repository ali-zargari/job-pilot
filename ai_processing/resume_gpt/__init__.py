"""
Resume GPT module for resume enhancement and generation.
"""

# Import API functions
try:
    from .api import enhance_resume, enhance_bullet, extract_tech_stack
except ImportError:
    # Handle import errors more gracefully
    import logging
    logging.warning("Could not import from resume_gpt.api. Some functionality may be limited.")
    
    # Define fallback functions
    def enhance_resume(resume_texts):
        return resume_texts
        
    def enhance_bullet(bullet_text):
        return bullet_text
    
    def extract_tech_stack(text):
        return []

__all__ = [
    'enhance_resume',
    'enhance_bullet',
    'extract_tech_stack'
]

__version__ = '0.1.0' 