"""
Test script to demonstrate resume optimizer functionality.
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Fix imports for direct execution
if __name__ == "__main__":
    # Add the current directory's parent to the path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

try:
    # Try standard import first (if resume_optimizer is installed)
    from resume_optimizer import get_optimizer, get_matcher
except ImportError:
    try:
        # Try relative import if running as part of a package
        from . import get_optimizer, get_matcher
    except ImportError:
        # Try direct import from current directory as last resort
        from optimizer import get_optimizer
        from matcher import get_matcher

# Load environment variables
load_dotenv()

# Example resume text
EXAMPLE_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Responsible for developing web applications
• Helped with improving system performance
• Worked on team projects and fixed bugs
• Managed database operations

Project Manager, StartupX (2017-2019)
• Led team of developers
• Responsible for project delivery
• Helped with customer support
"""

# Example job description
EXAMPLE_JOB = """
Senior Software Engineer

We're looking for an experienced Software Engineer with:
- 5+ years of experience in web development
- Strong background in Python, JavaScript, and cloud technologies
- Experience leading development teams
- Track record of improving system performance and scalability
- Strong problem-solving skills

Responsibilities:
- Lead development of web applications
- Optimize system performance
- Manage database operations
- Mentor junior developers
"""

def main():
    """Run a test of the resume optimization system."""
    
    print("🚀 Starting Resume Optimization Test\n")
    
    # Initialize optimizer with OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No OpenAI API key found. Will use T5 model only.")
    else:
        print("✅ Found OpenAI API key")
    
    try:
        optimizer = get_optimizer(openai_api_key=api_key)
        matcher = get_matcher(openai_api_key=api_key)
        
        print("\n📝 Original Resume:")
        print("-" * 50)
        print(EXAMPLE_RESUME)
        print("-" * 50 + "\n")
        
        # Step 1: Match resume with job
        print("🎯 Matching Resume with Job Description...")
        match_result = matcher.match_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB
        )
        
        print(f"Match Score: {match_result['overall_match']:.2%}")
        if match_result['job_match']:
            print(f"Job Match Score: {match_result['job_match']['score']:.2%}")
        print()
        
        # Step 2: Get improvement suggestions
        print("💡 Getting Improvement Suggestions...")
        suggestions = optimizer.get_suggestions(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB
        )
        
        print(f"Found {len(suggestions)} suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. Issue ({suggestion['severity']}): {suggestion['message']}")
            if suggestion.get('alternatives'):
                print(f"   Suggestion: {suggestion['alternatives'][0]}")
        print()
        
        # Step 3: Full optimization
        print("✨ Performing Full Resume Optimization...")
        result = optimizer.optimize_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB
        )
        
        print(f"Resume Score: {result['score']}/100\n")
        
        print("📈 Optimized Resume:")
        print("-" * 50)
        print(result['optimized'])
        print("-" * 50)
        
        # Print analysis
        print("\n📊 Analysis:")
        print(f"- Found {len(result['lint_results']['issues'])} issues")
        initial_score = result['lint_results'].get('initial_score', 0)
        print(f"- Score improved by {result['score'] - initial_score} points")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTraceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 