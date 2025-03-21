"""
Test script to demonstrate improved resume optimizations.
Shows how both weak phrase suggestions and metric additions are applied.
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Example resume data
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

# Example job description data
EXAMPLE_JOB = """
Software Engineering Position

Responsibilities:
- Design and develop robust web applications using modern technologies
- Collaborate with cross-functional teams to define, design, and ship new features
- Troubleshoot and fix bugs in existing applications
- Work with databases and API integrations

Requirements:
- Proficiency in web development technologies
- Experience with databases and optimization
- Strong problem-solving skills
- Team collaboration experience
"""

def main():
    # Load environment variables
    load_dotenv()
    
    print("🧪 Testing Improved Resume Optimizer")
    print("====================================")
    
    # Check if OpenAI API key is available (for tracking only)
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key Available: {'Yes' if api_key else 'No'}")
    
    # Setup imports
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from resume_optimizer import get_optimizer
        from resume_lint import analyze_resume
    except ImportError as e:
        print(f"Error importing modules: {str(e)}")
        return
    
    # Print original resume
    print("\n📄 ORIGINAL RESUME:")
    print("--------------------------------------------------")
    print(EXAMPLE_RESUME)
    print("--------------------------------------------------")
    
    # Initialize analyzer to get suggestions
    try:
        # Get suggestions first
        print("\n🔍 IDENTIFYING ISSUES:")
        print("--------------------------------------------------")
        
        # Initialize optimizer
        optimizer = get_optimizer(local_mode=True)
        suggestions = optimizer.get_suggestions(EXAMPLE_RESUME, EXAMPLE_JOB)
        
        # Print individual issues
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion.get('message', 'No message')}")
        
        # Now optimize the resume
        print("\n🔧 APPLYING ALL SUGGESTED IMPROVEMENTS:")
        print("--------------------------------------------------")
        
        result = optimizer.optimize_resume(EXAMPLE_RESUME, EXAMPLE_JOB)
        
        # Get scores
        original_score = result.get("score", 0)
        final_score = result.get("final_score", original_score)
        
        # Print the optimized resume
        print("\n📝 OPTIMIZED RESUME:")
        print("--------------------------------------------------")
        print(result.get("optimized", "Error: No optimized resume"))
        print("--------------------------------------------------")
        
        # Print analysis
        print("\n📊 RESULTS:")
        print("--------------------------------------------------")
        print(f"• Original Score: {original_score}/100")
        print(f"• Final Score: {final_score}/100") 
        print(f"• Improvement: +{final_score - original_score} points")
        print(f"• API Calls: {result.get('api_usage', 0)}")
        
        # Show what improvements were made
        print("\n✅ IMPROVEMENTS MADE:")
        print("--------------------------------------------------")
        print("1. Replaced weak phrases with stronger action verbs")
        print("2. Added quantifiable achievements to bullet points")
        print("3. Enhanced overall impact through specific metrics")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 