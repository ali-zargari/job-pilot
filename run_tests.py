#!/usr/bin/env python3
"""
Script to run comprehensive tests for the ai_processing module and identify redundant files.
"""

import os
import sys
import subprocess
import argparse
import glob
from pathlib import Path


def run_tests(verbose=False, coverage=False):
    """Run pytest on all test files."""
    print("\n🧪 Running tests for ai_processing module...\n")
    
    # Build pytest command
    cmd = ["pytest", "-v"] if verbose else ["pytest"]
    
    if coverage:
        cmd.extend(["--cov=ai_processing", "--cov-report=term"])
    
    # Run tests
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print results
    print(result.stdout)
    
    if result.stderr:
        print("\nErrors:")
        print(result.stderr)
    
    return result.returncode == 0


def identify_redundant_files():
    """Identify redundant files in the codebase."""
    print("\n🔍 Identifying redundant files...\n")
    
    # Path to the ai_processing directory
    base_dir = Path("ai_processing")
    
    # Map to store file sizes
    file_sizes = {}
    
    # Empty files (possible candidates for deletion)
    empty_files = []
    
    # Duplicate files (content-wise)
    duplicate_files = {}
    
    # Test files with no matching implementation
    orphaned_tests = []
    
    # Files with duplicate functionality
    redundant_modules = []
    
    # Scan the directory
    for filepath in glob.glob(str(base_dir / "**" / "*.py"), recursive=True):
        path = Path(filepath)
        
        # Check if file is empty
        if os.path.getsize(filepath) == 0:
            empty_files.append(str(path))
            continue
        
        # Read file content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # If file has only imports and docstrings, consider it redundant
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
            has_code = False
            for line in lines:
                if not (line.startswith('"""') or line.startswith("'''") or 
                        line.endswith('"""') or line.endswith("'''") or
                        line.startswith('import ') or line.startswith('from ')):
                    has_code = True
                    break
            
            if not has_code and len(lines) > 0:
                redundant_modules.append(str(path))
            
            # Check for duplicate content
            if content in file_sizes:
                if content not in duplicate_files:
                    duplicate_files[content] = [file_sizes[content]]
                duplicate_files[content].append(str(path))
            else:
                file_sizes[content] = str(path)
    
    # Special case: check resume_match and resume_refine directories
    if os.path.exists(base_dir / "resume_match") and all(os.path.getsize(f) == 0 for f in glob.glob(str(base_dir / "resume_match" / "*.py"))):
        redundant_modules.append("ai_processing/resume_match (all files are empty)")
    
    if os.path.exists(base_dir / "resume_refine") and all(os.path.getsize(f) == 0 for f in glob.glob(str(base_dir / "resume_refine" / "*.py"))):
        redundant_modules.append("ai_processing/resume_refine (all files are empty)")
    
    # Print results
    if empty_files:
        print("Empty files (candidates for removal):")
        for f in empty_files:
            print(f"  - {f}")
        print()
    
    if duplicate_files:
        print("Duplicate files (same content):")
        for _, files in duplicate_files.items():
            if len(files) > 1:
                print(f"  - Duplicates: {', '.join(files)}")
        print()
    
    if redundant_modules:
        print("Redundant modules (only imports/docstrings or empty directories):")
        for module in redundant_modules:
            print(f"  - {module}")
        print()
    
    # Store results
    results = {
        "empty_files": empty_files,
        "duplicate_files": duplicate_files,
        "redundant_modules": redundant_modules
    }
    
    return results


def cleanup_redundant_files(dry_run=True):
    """Remove redundant files identified during analysis."""
    results = identify_redundant_files()
    
    if dry_run:
        print("\n⚠️ DRY RUN - no files will be deleted\n")
        print("The following files would be deleted:")
    else:
        print("\n🗑️ Cleaning up redundant files...\n")
    
    files_to_delete = []
    
    # Collect empty files
    for filepath in results["empty_files"]:
        files_to_delete.append(filepath)
    
    # Collect duplicate files (keep one copy)
    for content, filepaths in results["duplicate_files"].items():
        if len(filepaths) > 1:
            # Keep the first file, delete the rest
            for filepath in filepaths[1:]:
                files_to_delete.append(filepath)
    
    # Print files that will be deleted
    for filepath in files_to_delete:
        print(f"  - {filepath}")
    
    # Delete the files if not a dry run
    if not dry_run:
        for filepath in files_to_delete:
            try:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            except Exception as e:
                print(f"Error deleting {filepath}: {str(e)}")
    
    # Recommend directories to remove (only if they contain empty files)
    if results["redundant_modules"]:
        dirs_to_consider = []
        for module in results["redundant_modules"]:
            if "all files are empty" in module:
                dirs_to_consider.append(module.split(" (")[0])
        
        if dirs_to_consider:
            print("\nDirectories to consider removing (all files are empty):")
            for directory in dirs_to_consider:
                print(f"  - {directory}")
            
            if not dry_run:
                print("\nThese directories need to be removed manually.")
    
    return files_to_delete


def main():
    """Main function to parse args and run tests/cleanup."""
    parser = argparse.ArgumentParser(description='Run tests and clean up redundant files')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose test output')
    parser.add_argument('-c', '--coverage', action='store_true', help='Calculate test coverage')
    parser.add_argument('--clean', action='store_true', help='Clean up redundant files')
    parser.add_argument('--dry-run', action='store_true', help='Show which files would be removed without deleting them')
    
    args = parser.parse_args()
    
    # Run tests
    tests_passed = run_tests(verbose=args.verbose, coverage=args.coverage)
    
    # Clean up redundant files if requested
    if args.clean or args.dry_run:
        cleanup_redundant_files(dry_run=args.dry_run or not args.clean)
    
    # Return appropriate exit code
    return 0 if tests_passed else 1


if __name__ == "__main__":
    sys.exit(main()) 