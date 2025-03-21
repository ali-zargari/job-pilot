"""
Test script to demonstrate enhanced detailed scoring with multiple components.
Shows the breakdown of ATS, Recruiter, Grammar, and Job Match scores.
"""

import os
import sys
import traceback
from dotenv import load_dotenv

# Example resume data
GOOD_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Developed responsive web applications that improved user engagement by 35%
• Implemented performance optimizations reducing load times by 40%
• Led a team of 5 developers to deliver projects 15% ahead of schedule
• Managed database operations, improving query performance by 20% and reducing storage costs by 15%

Project Manager, StartupX (2017-2019)
• Directed a team of 7 developers delivering 12 successful projects
• Increased client satisfaction ratings by 25% through improved delivery processes
• Generated $500K in additional revenue through process optimization
"""

WEAK_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Responsible for developing web applications
• Helped with improving system performance
• Worked on team projects and fixed bugs
• Was in charge of database operations

Project Manager, StartupX (2017-2019)
• Was responsible for leading team of developers
• In charge of project delivery and was making sure everything was completed according to the requirements that were specified by clients
• Helped with customer support and did everything that was required to make sure customers were satisfied
"""

# Example job description data
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

def format_score_card(scores):
    """Format a nice score card from the detailed scores dictionary."""
    composite = scores.get("composite_score", 0)
    ats = scores.get("ats_score", 0)
    recruiter = scores.get("recruiter_score", 0)
    grammar = scores.get("grammar_score", 0)
    job_match = scores.get("job_match_score", 0)
    
    card = f"""
┌─────────────────────────────────────┐
│         RESUME SCORE CARD           │
├─────────────────┬───────────────────┤
│ OVERALL SCORE   │ {composite:3d}/100{' ★★★★★' if composite >= 90 else ' ★★★★☆' if composite >= 80 else ' ★★★☆☆' if composite >= 70 else ' ★★☆☆☆' if composite >= 60 else ' ★☆☆☆☆'}  │
├─────────────────┼───────────────────┤
│ ATS Score       │ {ats:3d}/100       │
│ Recruiter Score │ {recruiter:3d}/100       │
│ Grammar Score   │ {grammar:3d}/100       │
│ Job Match Score │ {job_match:3d}/100       │
└─────────────────┴───────────────────┘
"""
    return card

def main():
    # Load environment variables
    load_dotenv()
    
    print("🧪 Testing Enhanced Resume Scoring System")
    print("=========================================")
    
    # Setup imports
    try:
        # Add parent directory to path
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from resume_optimizer import get_optimizer
    except ImportError as e:
        print(f"Error importing modules: {str(e)}")
        return
    
    optimizer = get_optimizer(local_mode=True)
    
    # Test with GOOD resume
    print("\n📄 GOOD RESUME ANALYSIS:")
    print("--------------------------------------------------")
    result_good = optimizer.optimize_resume(GOOD_RESUME, EXAMPLE_JOB)
    
    # Extract and display detailed scores
    detailed_scores = result_good.get("detailed_score", {})
    is_ready = detailed_scores.get("is_resume_ready", False)
    
    print(format_score_card(detailed_scores))
    
    if is_ready:
        print("✅ RESUME READY - This resume meets professional standards!")
        print("   No optimization needed.")
    else:
        print("⚠️ RESUME NEEDS IMPROVEMENT - See detailed scores above.")
    
    # Test with WEAK resume
    print("\n📄 WEAK RESUME ANALYSIS:")
    print("--------------------------------------------------")
    result_weak = optimizer.optimize_resume(WEAK_RESUME, EXAMPLE_JOB)
    
    # Extract and display detailed scores for weak resume
    detailed_scores_weak = result_weak.get("detailed_score", {})
    final_scores_weak = result_weak.get("final_detailed_score", {})
    
    print("BEFORE OPTIMIZATION:")
    print(format_score_card(detailed_scores_weak))
    
    print("AFTER OPTIMIZATION:")
    print(format_score_card(final_scores_weak))
    
    # Show what changed
    changes = result_weak.get("changes_made", {})
    print("\n📊 OPTIMIZATION SUMMARY:")
    print("--------------------------------------------------")
    print(f"• Lines changed: {changes.get('lines_changed', 0)} out of {changes.get('total_lines', 0)} ({changes.get('change_percentage', 0)}%)")
    print(f"• Weak phrases replaced: {changes.get('verb_replacements', 0)}")
    print(f"• Metrics added: {changes.get('metric_additions', 0)}")
    
    # Show job match improvement
    job_match_improvement = result_weak.get("job_match_improvement", 0)
    print(f"• Job match improvement: +{job_match_improvement} points")
    
    print("\n✅ OPTIMIZED RESUME:")
    print("--------------------------------------------------")
    print(result_weak.get("optimized", "Error: No optimized resume"))
    
if __name__ == "__main__":
    main() 