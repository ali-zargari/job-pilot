"""
File utilities for the resume optimizer.

This module contains functions for reading and writing files,
as well as utility functions for working with directories.
"""

import os
from pathlib import Path


def read_file_content(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()


def write_file_content(file_path, content):
    """Write content to a file, creating directories if needed."""
    file_path = Path(file_path)
    os.makedirs(file_path.parent, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def format_text_for_display(text):
    """Format text for better display in console or reports."""
    lines = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if not line:
            lines.append("")
        else:
            # Wrap long lines
            if len(line) > 80:
                chunks = [line[i:i+80] for i in range(0, len(line), 80)]
                lines.extend(chunks)
            else:
                lines.append(line)
    return '\n'.join(lines)


def ensure_directory_exists(directory_path):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory_path, exist_ok=True)
    return directory_path 