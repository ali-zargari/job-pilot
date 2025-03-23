"""
Utility functions for AI processing.
Includes various helper functions used throughout the application.
File operations, formatting, and other utilities.
"""

from ai_processing.utilities.fix_file_encoding import fix_encoding
from ai_processing.utilities.file_utils import (
    read_file_content,
    write_file_content,
    format_text_for_display,
    ensure_directory_exists
)

__all__ = [
    'fix_encoding',
    'read_file_content',
    'write_file_content',
    'format_text_for_display',
    'ensure_directory_exists'
] 