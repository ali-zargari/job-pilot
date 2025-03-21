"""
Test script to demonstrate improvements in phrase handling and verb optimization.
Shows before and after examples with different types of weak phrases.
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Define test cases with various problematic phrases
TEST_CASES = [
    {
        "name": "Passive voice",
        "before": "• Was responsible for developing and maintaining the company website",
        "expected": "• Managed developing and maintaining the company website",
    },
    {
        "name": "Redundant verbs",
        "before": "• Managed leading a team of developers for the project",
        "expected": "• Led a team of developers for the project",
    },
    {
        "name": "Weak action verbs",
        "before": "• Helped with designing the new user interface",
        "expected": "• Contributed to designing the new user interface",
    },
    {
        "name": "Complex passive construction",
        "before": "• Was making sure all deliverables were completed on time",
        "expected": "• Ensured all deliverables were completed on time",
    },
    {
        "name": "Verbose phrases",
        "before": "• Responsible for making sure that the team adhered to guidelines",
        "expected": "• Managed ensuring the team adhered to guidelines",
    },
    {
        "name": "Mixed issues",
        "before": "• Was in charge of coordinating activities and was making sure everything ran smoothly",
        "expected": "• Led coordinating activities and ensured everything ran smoothly",
    }
]

# Example resume with weak phrasing
WEAK_RESUME = """
WORK EXPERIENCE

Senior Software Engineer, TechCorp (2020-2023)
• Was responsible for leading the backend development team
• In charge of designing and implementing new features
• Helped with improving system performance and reliability
• Worked on troubleshooting and fixing critical bugs

Project Manager, Innovatech (2017-2020)
• Was making sure that all project deadlines were met
• Responsible for coordinating between different teams
• Assisted in client communications and reporting
• Was in charge of budget planning and resource allocation
"""

def test_phrases():
    """Test individual phrase replacements."""
    print("\n🧪 TESTING INDIVIDUAL PHRASE REPLACEMENTS")
    print("==========================================")
    
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from resume_optimizer import get_optimizer
    except ImportError as e:
        print(f"Error importing modules: {str(e)}")
        return
        
    optimizer = get_optimizer(local_mode=True)
    
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\nTest Case {i}: {case['name']}")
        print(f"Before: {case['before']}")
        
        # Simulate the text replacement logic
        bullets_needing_metrics = []
        result = optimizer._add_quantifiable_achievements(case['before'], bullets_needing_metrics)
        
        print(f"After:  {result}")
        print(f"Expected: {case['expected']}")
        
        if result.strip() == case['expected'].strip():
            print("✅ PASS")
        else:
            print("❌ FAIL")

def test_full_resume():
    """Test optimization of a full resume."""
    print("\n\n🧪 TESTING FULL RESUME OPTIMIZATION")
    print("====================================")
    
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from resume_optimizer import get_optimizer
    except ImportError as e:
        print(f"Error importing modules: {str(e)}")
        return
        
    optimizer = get_optimizer(local_mode=True)
    
    print("\n📄 WEAK RESUME (BEFORE):")
    print("--------------------------------------------------")
    print(WEAK_RESUME)
    print("--------------------------------------------------")
    
    # Process the resume
    result = optimizer.optimize_resume(WEAK_RESUME)
    
    print("\n📄 OPTIMIZED RESUME (AFTER):")
    print("--------------------------------------------------")
    print(result.get("optimized", "Error: No optimized resume"))
    print("--------------------------------------------------")
    
    # Print analysis
    score_before = result.get("score", 0)
    score_after = result.get("final_score", 0)
    
    print(f"\n📊 SCORES: {score_before}/100 → {score_after}/100 (+{score_after - score_before} points)")
    
    # Show what changes were made
    changes = result.get("changes_made", {})
    if changes:
        print("\n📝 CHANGES MADE:")
        print(f"• Lines modified: {changes.get('lines_changed', 0)} of {changes.get('total_lines', 0)} ({changes.get('change_percentage', 0)}%)")
        print(f"• Weak phrases replaced: {changes.get('verb_replacements', 0)}")
        print(f"• Metrics added: {changes.get('metric_additions', 0)}")

def main():
    """Run the tests."""
    load_dotenv()
    
    print("🚀 TESTING VERB OPTIMIZATION FUNCTIONALITY")
    print("=========================================")
    
    try:
        test_phrases()
        test_full_resume()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 