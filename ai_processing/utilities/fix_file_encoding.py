#!/usr/bin/env python3
"""
Utility script to fix encoding issues in Python files.

This script can:
1. Remove null bytes from files
2. Fix UTF-8 BOM markers
3. Fix unterminated string literals
4. Remove non-printable characters
5. Fix specific problematic lines

Usage:
    python -m ai_processing.utilities.fix_file_encoding <filename> [--line <line_number>]
"""

import os
import re
import sys
import shutil
import argparse
from typing import Tuple, Optional

def fix_null_bytes(file_path: str, create_backup: bool = True) -> Tuple[int, str]:
    """
    Remove null bytes from a file and save it with proper encoding.
    
    Args:
        file_path: Path to the file to fix
        create_backup: Whether to create a backup of the original file
        
    Returns:
        Tuple of (count of null bytes removed, path to backup file or empty string)
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return 0, ""
    
    backup_path = ""
    if create_backup:
        backup_path = f"{file_path}.bak"
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    try:
        # Read the binary content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Count and remove null bytes
        null_count = content.count(b'\x00')
        if null_count > 0:
            content = content.replace(b'\x00', b'')
            print(f"Removed {null_count} null bytes")
        
        # Write back the clean content
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return null_count, backup_path
    
    except Exception as e:
        print(f"Error processing file: {e}")
        # Restore from backup if we failed
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print(f"Restored original file from backup due to error")
        return 0, ""

def fix_encoding(file_path: str, create_backup: bool = True) -> Tuple[bool, str]:
    """
    Fix encoding issues in a file, including BOM markers and non-printable characters.
    
    Args:
        file_path: Path to the file to fix
        create_backup: Whether to create a backup of the original file
        
    Returns:
        Tuple of (success status, path to backup file or empty string)
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False, ""
    
    backup_path = ""
    if create_backup:
        backup_path = f"{file_path}.encoding.bak"
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    try:
        # Read the binary content
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Remove BOM if present
        if content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
            content = content[3:]
            print(f"Removed UTF-8 BOM marker")
        
        # Count null bytes
        null_count = content.count(b'\x00')
        if null_count > 0:
            content = content.replace(b'\x00', b'')
            print(f"Removed {null_count} null bytes")
        
        # Try to decode as UTF-8 first, then fallback to Latin-1
        try:
            decoded = content.decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            decoded = content.decode('latin-1')
            print("Used Latin-1 fallback encoding")
        
        # Remove any non-printable ASCII characters except whitespace
        cleaned = ''.join(c for c in decoded if c.isprintable() or c.isspace())
        if len(cleaned) != len(decoded):
            print(f"Removed {len(decoded) - len(cleaned)} non-printable characters")
        
        # Write back the clean content as UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"Successfully cleaned and saved file as UTF-8")
        return True, backup_path
    
    except Exception as e:
        print(f"Error processing file: {e}")
        # Restore from backup if we failed
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print(f"Restored original file from backup due to error")
        return False, ""

def fix_specific_line(file_path: str, line_number: int, create_backup: bool = True) -> Tuple[bool, str, str, str]:
    """
    Fix a specific line in a file (particularly useful for syntax errors).
    
    Args:
        file_path: Path to the file to fix
        line_number: Line number to fix (1-indexed)
        create_backup: Whether to create a backup of the original file
        
    Returns:
        Tuple of (success status, backup path, original line, fixed line)
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False, "", "", ""
    
    backup_path = ""
    if create_backup:
        backup_path = f"{file_path}.line.bak"
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    try:
        # Read all lines
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Check if line number is valid
        if line_number < 1 or line_number > len(lines):
            print(f"Error: Line number {line_number} is out of range (file has {len(lines)} lines)")
            return False, backup_path, "", ""
        
        # Get and display the original line
        original_line = lines[line_number - 1].rstrip()
        print(f"Original line {line_number}: {original_line}")
        
        # Try to fix the line - here we handle common issues
        fixed_line = original_line
        
        # Check for unterminated string literals
        if re.search(r'(["\'])(.*?)(?<!\\\1)(\1|$)', original_line):
            # Comment out the line
            fixed_line = f"# Line removed due to syntax error: {original_line.strip()}"
            print(f"Fixing unterminated string literal by commenting out the line")
        
        # Update the line in the file
        lines[line_number - 1] = fixed_line + '\n'
        
        # Write the file back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print(f"Updated line {line_number}")
        return True, backup_path, original_line, fixed_line
    
    except Exception as e:
        print(f"Error processing file: {e}")
        # Restore from backup if we failed
        if backup_path and os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print(f"Restored original file from backup due to error")
        return False, backup_path, "", ""

def main():
    """Command line interface for the encoding fix utilities."""
    parser = argparse.ArgumentParser(description="Fix encoding issues in Python files")
    parser.add_argument("file", help="Path to the file to fix")
    parser.add_argument("--line", type=int, help="Specific line number to fix")
    parser.add_argument("--no-backup", action="store_true", help="Don't create backup files")
    parser.add_argument("--null-bytes-only", action="store_true", help="Only remove null bytes")
    
    args = parser.parse_args()
    create_backup = not args.no_backup
    
    if args.null_bytes_only:
        count, backup = fix_null_bytes(args.file, create_backup)
        if count > 0:
            print(f"Fixed {count} null bytes in {args.file}")
    elif args.line:
        success, backup, orig, fixed = fix_specific_line(args.file, args.line, create_backup)
        if success:
            print(f"Successfully fixed line {args.line} in {args.file}")
    else:
        success, backup = fix_encoding(args.file, create_backup)
        if success:
            print(f"Successfully fixed encoding in {args.file}")

if __name__ == "__main__":
    main() 