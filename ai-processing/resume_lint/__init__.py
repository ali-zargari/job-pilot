"""
Resume linting module for analyzing and improving resumes.
"""

from .rules import (
    check_passive_voice,
    check_weak_phrases,
    check_missing_numbers,
    check_sentence_length,
    check_ats_friendly,
    suggest_alternatives,
    WEAK_PHRASES,
    STRONG_ALTERNATIVES
)

from .preprocess import (
    analyze_resume,
    ResumeAnalyzer,
    preprocess_text,
    extract_bullet_points
)

__all__ = [
    'check_passive_voice',
    'check_weak_phrases',
    'check_missing_numbers',
    'check_sentence_length',
    'check_ats_friendly',
    'suggest_alternatives',
    'analyze_resume',
    'ResumeAnalyzer',
    'preprocess_text',
    'extract_bullet_points',
    'WEAK_PHRASES',
    'STRONG_ALTERNATIVES'
]

__version__ = '0.1.0' 