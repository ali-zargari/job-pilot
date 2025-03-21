"""
Test script to demonstrate the ability to recognize already optimized resumes.
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
    from resume_optimizer import get_optimizer
except ImportError:
    try:
        # Try relative import if running as part of a package
        from . import get_optimizer
    except ImportError:
        # Try direct import from current directory as last resort
        from optimizer import get_optimizer

# Load environment variables
load_dotenv()

# Example of an already optimized resume with strong action verbs and quantifiable achievements
OPTIMIZED_RESUME = """
PROFESSIONAL EXPERIENCE

Senior Software Engineer, TechCorp (2019-2022)
• Developed and launched a customer-facing mobile app that increased user engagement by 45%
• Improved API response times by 60% through implementing efficient caching strategies
• Led a team of 5 developers to deliver 3 major product releases on time and under budget
• Reduced cloud infrastructure costs by 30% by optimizing resource allocation

Software Development Lead, InnovateTech (2017-2019)
• Spearheaded the redesign of the company's flagship product, resulting in 28% revenue growth
• Implemented CI/CD pipelines that reduced deployment time from 2 days to 20 minutes
• Mentored 8 junior developers, with 4 receiving promotions within their first year
• Created an automated testing framework that increased code coverage from 65% to 92%
"""

# Example of a resume that needs improvement
WEAK_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Responsible for coding web applications
• Helped with testing and debugging
• Worked on various projects as assigned
• Was in charge of some database tasks

Developer, StartupX (2017-2019)
• Duties included writing code
• Assisted in maintaining websites
• Helped other team members
"""

def main():
    """Run a test to demonstrate recognition of already optimized resumes."""
    
    print("🚀 Testing Resume Optimization Recognition\n")
    
    # Initialize optimizer with OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No OpenAI API key found. Will use T5 model only.")
    else:
        print("✅ Found OpenAI API key")
    
    try:
        optimizer = get_optimizer(openai_api_key=api_key)
        
        # Test 1: Optimized Resume
        print("\n📝 Testing Already Optimized Resume:")
        print("-" * 50)
        print(OPTIMIZED_RESUME)
        print("-" * 50 + "\n")
        
        print("💡 Getting Suggestions for Optimized Resume...")
        optimized_suggestions = optimizer.get_suggestions(
            resume_text=OPTIMIZED_RESUME
        )
        
        print(f"Found {len(optimized_suggestions)} suggestions:")
        for i, suggestion in enumerate(optimized_suggestions, 1):
            print(f"\n{i}. Type: {suggestion.get('type', suggestion.get('severity', 'unknown'))}")
            print(f"   Message: {suggestion['message']}")
            if suggestion.get('details'):
                print(f"   Details: {suggestion['details']}")
            if suggestion.get('alternatives'):
                print(f"   Suggestion: {suggestion['alternatives'][0]}")
        print()
        
        print("✨ Full Resume Analysis for Optimized Resume...")
        optimized_result = optimizer.optimize_resume(
            resume_text=OPTIMIZED_RESUME
        )
        
        print(f"Resume Score: {optimized_result.get('score', 0)}/100")
        print(f"Is Already Optimized: {optimized_result.get('no_changes_needed', False)}")
        if optimized_result.get('message'):
            print(f"Message: {optimized_result['message']}")
        print()
        
        # Test 2: Weak Resume
        print("\n📝 Testing Resume That Needs Improvement:")
        print("-" * 50)
        print(WEAK_RESUME)
        print("-" * 50 + "\n")
        
        print("💡 Getting Suggestions for Weak Resume...")
        weak_suggestions = optimizer.get_suggestions(
            resume_text=WEAK_RESUME
        )
        
        print(f"Found {len(weak_suggestions)} suggestions:")
        for i, suggestion in enumerate(weak_suggestions, 1):
            print(f"\n{i}. Type: {suggestion.get('type', suggestion.get('severity', 'unknown'))}")
            print(f"   Message: {suggestion['message']}")
            if suggestion.get('details'):
                print(f"   Details: {suggestion['details']}")
            if suggestion.get('alternatives'):
                print(f"   Suggestion: {suggestion['alternatives'][0]}")
        print()
        
        print("✨ Full Resume Analysis for Weak Resume...")
        weak_result = optimizer.optimize_resume(
            resume_text=WEAK_RESUME
        )
        
        print(f"Resume Score: {weak_result.get('score', 0)}/100")
        print(f"Is Already Optimized: {weak_result.get('no_changes_needed', False)}")
        if weak_result.get('message'):
            print(f"Message: {weak_result['message']}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTraceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 