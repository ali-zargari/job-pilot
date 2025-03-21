"""
Test script to demonstrate local mode optimization without API usage.
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
    
    print("🚀 Starting Resume Optimization Test (Local Mode)")
    
    # Check if OpenAI API key is available (for comparison only)
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("ℹ️ OpenAI API key found, but we'll run in local mode anyway")
    else:
        print("ℹ️ No OpenAI API key found - local mode is ideal for this scenario")
    
    # Print original resume
    print("\n📝 Original Resume:")
    print("--------------------------------------------------")
    print(EXAMPLE_RESUME)
    print("--------------------------------------------------")
    
    try:
        # Import the optimizer after environment is set up
        try:
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from resume_optimizer import get_optimizer
            from resume_lint import analyze_resume
        except ImportError as e:
            print(f"Error importing modules: {str(e)}")
            return
            
        # Initialize optimizer in local mode
        optimizer = get_optimizer(local_mode=True)
        
        # Run analysis
        print("\n🔍 Analyzing Resume for Improvements...")
        suggestions = optimizer.get_suggestions(EXAMPLE_RESUME, EXAMPLE_JOB)
        
        print(f"Found {len(suggestions)} suggestions:")
        print()
        for i, suggestion in enumerate(suggestions, 1):
            severity = suggestion.get("severity", "low")
            message = suggestion.get("message", "No message")
            
            # Get the first alternative if available
            alt = suggestion.get("alternatives", ["No suggestion"])[0]
            
            print(f"{i}. Issue ({severity}): {message}")
            print(f"   Suggestion: {alt}\n")
        
        # Optimize resume without API calls
        print("✨ Performing Resume Optimization (Local Mode)...")
        result = optimizer.optimize_resume(EXAMPLE_RESUME, EXAMPLE_JOB)
        
        # Get original and final scores directly from the result
        original_score = result.get("lint_results", {}).get("score", 0)
        final_score = result.get("final_score", original_score)
        
        print(f"Original Score: {original_score}/100")
        print(f"Final Score: {final_score}/100")
        print(f"API Calls Made: {result.get('api_usage', 0)}")
        
        # Print optimized resume
        print("\n📈 Optimized Resume (Local Mode):")
        print("--------------------------------------------------")
        print(result.get("optimized", "No optimized resume generated"))
        print("--------------------------------------------------")
        
        # Print analysis
        print("\n📊 Analysis:")
        if result.get("no_changes_needed", False):
            print("- Your resume is already well-optimized!")
        else:
            print(f"- Found {len(suggestions)} issues")
            if final_score > original_score:
                improvement = final_score - original_score
                print(f"- Score improved by {improvement} points (from {original_score} to {final_score})")
            elif final_score < original_score:
                print(f"- ⚠️ Score decreased by {original_score - final_score} points - manual review recommended")
            else:
                print("- Score remained the same - consider reviewing the optimized version")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        
if __name__ == "__main__":
    main() 