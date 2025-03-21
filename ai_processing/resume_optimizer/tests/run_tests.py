#!/usr/bin/env python
"""
Test runner for resume optimizer tests.
This script runs all test cases for the resume optimizer.
"""

import unittest
import os
import sys
import importlib

# Fix the import path to work with the current directory structure
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    # Create test suite from all test files
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add tests from each test module
    test_modules = [
        f[:-3] for f in os.listdir(current_dir) 
        if f.startswith('test_') and f.endswith('.py') and not f == 'run_tests.py'
    ]
    
    for module in test_modules:
        try:
            # Just use the direct module import
            module_path = os.path.join(current_dir, f"{module}.py")
            spec = importlib.util.spec_from_file_location(module, module_path)
            module_obj = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_obj)
            
            # Add tests from this module
            test_suite.addTest(unittest.TestLoader().loadTestsFromModule(module_obj))
            print(f"Added tests from {module}")
        except Exception as e:
            print(f"Error loading tests from {module}: {e}")
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\nTest Results:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    # Exit with non-zero status if there were failures or errors
    sys.exit(len(result.failures) + len(result.errors)) 