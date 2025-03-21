#!/usr/bin/env python
"""
Script to test running the resume optimizer with our modified code.
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

try:
    # Try to import the OpenAI key from .env file
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed, using environment variables directly")

# Import the resume optimizer
from ai_processing.resume_optimizer.optimizer import ResumeOptimizer

def main():
    """Run a test of the optimizer"""
    # Check if we have an API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Warning: No OPENAI_API_KEY found in environment variables.")
        print("Running in local mode without API calls.")
        local_mode = True
    else:
        print(f"Using OpenAI API key: {api_key[:5]}...")
        local_mode = False
    
    # Create a sample resume with NO metrics
    resume_no_metrics = """
    John Doe
    Software Engineer
    
    EXPERIENCE
    ABC Company - Software Engineer (2018-2022)
    - Developed web applications using React
    - Created backend APIs with Node.js
    - Improved page load times
    
    EDUCATION
    University of Technology - B.S. Computer Science (2014-2018)
    """
    
    # Create a sample resume WITH metrics
    resume_with_metrics = """
    John Doe
    Software Engineer
    
    EXPERIENCE
    ABC Company - Software Engineer (2018-2022)
    - Developed web applications using React for 5 client projects
    - Created backend APIs with Node.js, supporting 1000+ users
    - Improved page load times by 40%
    
    EDUCATION
    University of Technology - B.S. Computer Science (2014-2018)
    """
    
    job_description = """
    We're looking for a Frontend Developer with experience in:
    - React and modern JavaScript
    - Creating responsive UI components
    - Implementing web performance optimizations
    - Working with RESTful APIs
    """
    
    # Initialize the optimizer
    optimizer = ResumeOptimizer(openai_api_key=api_key, local_mode=local_mode)
    
    # Test with no metrics
    print("\n\n=============== TESTING RESUME WITH NO METRICS ===============")
    print("\nOptimizing resume without metrics...")
    result_no_metrics = optimizer.optimize_resume(
        resume_text=resume_no_metrics,
        job_description=job_description,
        apply_ai_rewrite=True
    )
    
    # Print results - NO METRICS
    print("\nOriginal Resume (NO METRICS):")
    print("-" * 40)
    print(resume_no_metrics)
    
    print("\nOptimized Resume (NO METRICS):")
    print("-" * 40)
    if "optimized_text" in result_no_metrics:
        print(result_no_metrics["optimized_text"])
    elif "optimized" in result_no_metrics:
        print(result_no_metrics["optimized"])
    else:
        print("No optimized text found in result")
    
    # Test WITH metrics
    print("\n\n=============== TESTING RESUME WITH METRICS ===============")
    print("\nOptimizing resume with metrics...")
    result_with_metrics = optimizer.optimize_resume(
        resume_text=resume_with_metrics,
        job_description=job_description,
        apply_ai_rewrite=True
    )
    
    # Print results - WITH METRICS
    print("\nOriginal Resume (WITH METRICS):")
    print("-" * 40)
    print(resume_with_metrics)
    
    print("\nOptimized Resume (WITH METRICS):")
    print("-" * 40)
    if "optimized_text" in result_with_metrics:
        print(result_with_metrics["optimized_text"])
    elif "optimized" in result_with_metrics:
        print(result_with_metrics["optimized"])
    else:
        print("No optimized text found in result")
    
    print("\nOptimization complete.")

if __name__ == "__main__":
    main() 