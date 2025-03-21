"""
Test script to demonstrate Phase 2 AI enhancement functionality.
Shows the difference between local rule-based optimization and AI-enhanced optimization.
"""

import os
import sys
import traceback
from dotenv import load_dotenv
import textwrap

# Example resume that needs significant improvement
SAMPLE_RESUME = """
WORK EXPERIENCE

Junior Software Developer, TechStart Inc. (2021-2023)
• Was responsible for coding on the frontend team
• Helped with fixing bugs and issues in the codebase
• Worked on some features for the mobile application
• Assisted in testing and quality assurance procedures

Web Development Intern, WebSolutions Corp (2020-2021)
• Was in charge of making HTML and CSS updates to the company website
• Responsible for helping senior developers with tasks
• Helped with setting up development environments for new team members
• Assisted in documenting code and creating user manuals
"""

# Example job description for targeting
SAMPLE_JOB = """
Senior Frontend Developer

We're looking for a talented Frontend Developer with:
- 3+ years of experience with React, Angular, or similar frameworks
- Strong JavaScript skills and experience with modern ES6+ features
- Experience with responsive design and mobile-first approaches
- Knowledge of frontend build tools and CI/CD pipelines

Responsibilities:
- Develop and maintain responsive web applications
- Collaborate with UX/UI designers to implement modern interfaces
- Optimize applications for maximum speed and scalability
- Ensure code quality through testing and code reviews
"""

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f" {text}")
    print("=" * 70)

def print_score_comparison(score_before, rule_based_score, ai_score):
    """Print a formatted score comparison table."""
    print("\n┌─────────────────────┬────────┬────────┬────────┐")
    print("│      Category       │ Before │ Phase 1 │ Phase 2 │")
    print("├─────────────────────┼────────┼────────┼────────┤")
    print(f"│ Overall Score       │   {score_before:2d}    │   {rule_based_score:2d}    │   {ai_score:2d}    │")
    print("└─────────────────────┴────────┴────────┴────────┘")

def format_resume(resume_text):
    """Format resume text for display."""
    return textwrap.indent(resume_text.strip(), '  ')

def main():
    """Run the Phase 2 test demonstration."""
    load_dotenv()
    
    print_header("RESUME ENHANCEMENT SYSTEM - PHASE 1 & 2 DEMONSTRATION")
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n⚠️ No OpenAI API key found. Only Phase 1 (rule-based) optimization will be shown.")
        print("   Set the OPENAI_API_KEY in your .env file to see Phase 2 AI enhancement.")
    else:
        print("\n✅ OpenAI API key found. Both Phase 1 and Phase 2 optimizations will be shown.")
    
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from resume_optimizer import get_optimizer
    except ImportError as e:
        print(f"\n❌ Error importing modules: {str(e)}")
        return
    
    # Original resume analysis
    print_header("ORIGINAL RESUME")
    print(format_resume(SAMPLE_RESUME))
    
    # Phase 1: Rule-based optimization only
    print_header("PHASE 1: RULE-BASED OPTIMIZATION")
    optimizer = get_optimizer(local_mode=True)
    rule_based_result = optimizer.optimize_resume(SAMPLE_RESUME, SAMPLE_JOB)
    
    print(format_resume(rule_based_result.get("optimized", "")))
    
    # Phase 2: AI-enhanced optimization
    print_header("PHASE 2: AI-ENHANCED OPTIMIZATION")
    
    if api_key:
        # Run with AI enhancement if API key is available
        optimizer = get_optimizer(openai_api_key=api_key, local_mode=False)
        ai_result = optimizer.optimize_resume(SAMPLE_RESUME, SAMPLE_JOB, apply_ai_rewrite=True)
        
        print(format_resume(ai_result.get("optimized", "")))
        
        # Show score comparison
        original_score = rule_based_result.get("score", 0)
        rule_based_score = rule_based_result.get("final_score", 0)
        ai_score = ai_result.get("final_score", 0)
        
        print_score_comparison(original_score, rule_based_score, ai_score)
        
        # Show API usage
        print(f"\nℹ️ API Calls: {ai_result.get('api_usage', 0)}")
        print(f"ℹ️ AI Enhancement Applied: {'Yes' if ai_result.get('optimized_with_ai', False) else 'No'}")
        
        # Show differences between versions
        print_header("KEY DIFFERENCES BETWEEN PHASE 1 AND PHASE 2")
        print("  1. Phase 1 (Rule-Based):")
        print("     - Applies syntax-based transformations")
        print("     - Replaces weak phrases with stronger verbs")
        print("     - Adds generic quantifiable metrics")
        print("     - Requires no API calls (works offline)")
        print("\n  2. Phase 2 (AI-Enhanced):")
        print("     - Refines language for better clarity and impact")
        print("     - Contextualizes metrics based on job description")
        print("     - Enhances overall resume coherence")
        print("     - Requires API access (uses 1 API call)")
    else:
        # If no API key, explain what Phase 2 would do
        print("\n  API key not available. In Phase 2, an AI model would:")
        print("  - Further refine the language for more natural flow")
        print("  - Adjust metrics to be more relevant to the job context")
        print("  - Improve overall narrative coherence while preserving structure")
        print("  - Ensure all achievements are presented optimally")
        print("\n  To experience Phase 2 enhancement, add your OpenAI API key to the .env file.")

if __name__ == "__main__":
    main() 