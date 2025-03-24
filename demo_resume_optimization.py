import os
import logging
import json
import re
from pprint import pprint
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables (for OpenAI API key)
load_dotenv()

# Import the resume optimizer
from ai_processing.resume_openai import rewrite_resume

# Sample resume for testing (intentionally simplified with areas to improve)
SAMPLE_RESUME = """
John Doe
Software Developer
johndoe@example.com | (555) 123-4567 | linkedin.com/in/johndoe

WORK EXPERIENCE

Software Developer, ABC Tech (2020-Present)
• Responsible for backend development using Python
• Worked on database systems
• Helped solve customer issues
• Part of the agile team for product development

Junior Developer, XYZ Solutions (2018-2020)
• Developed web applications
• Maintained code repositories
• Participated in team meetings
• Assisted senior developers

EDUCATION
• Bachelor of Science, Computer Science, State University (2014-2018)

SKILLS
Python, JavaScript, HTML, CSS, SQL, Git
"""

# Sample job description
SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer

We're seeking an experienced Software Engineer to join our growing team. The ideal candidate will:

- Have 3+ years of experience in backend development with Python
- Be proficient in database design and optimization
- Have experience with cloud platforms (AWS preferred)
- Be able to work in an agile environment
- Possess excellent problem-solving and communication skills

You'll be working on our core product, collaborating with a team of talented engineers to build scalable and efficient solutions.
"""

# Weak action verb replacements - truly rule-based improvement
WEAK_VERB_REPLACEMENTS = {
    "responsible for": "managed",
    "worked on": "developed",
    "helped": "assisted with",
    "part of": "contributed to",
    "developed": "built",
    "maintained": "managed",
    "participated in": "contributed to",
    "assisted": "supported"
}

def truly_rule_based_optimize(resume_text):
    """
    Find suggestions for resume improvement rather than making changes directly.
    This is a purely rule-based approach that doesn't use AI.
    
    Args:
        resume_text: Original resume text
        
    Returns:
        dict: Dictionary of suggestions for resume improvement
    """
    suggestions = {
        "weak_verbs": [],
        "formatting_issues": [],
        "content_improvements": []
    }
    
    # Find weak verbs that could be replaced
    for weak_verb, strong_verb in WEAK_VERB_REPLACEMENTS.items():
        # Look for weak verbs at the start of bullet points
        pattern = r'(•\s*)' + weak_verb
        matches = re.finditer(pattern, resume_text, flags=re.IGNORECASE)
        for match in matches:
            original_text = match.group(0)
            suggestion = f"Replace '{weak_verb}' with '{strong_verb}' in '{original_text}'"
            suggestions["weak_verbs"].append(suggestion)
    
    # Find formatting issues
    # Check for bullet points without spaces
    inconsistent_bullets = re.findall(r'•(\S)', resume_text)
    if inconsistent_bullets:
        suggestions["formatting_issues"].append("Ensure consistent spacing after bullet points")
    
    # Check for excessive line breaks
    if re.search(r'\n{3,}', resume_text):
        suggestions["formatting_issues"].append("Normalize spacing between sections to be consistent")
    
    # Content improvement suggestions (basic rule-based checks)
    bullet_points = re.findall(r'•\s*(.*?)(?=\n•|\n\n|\Z)', resume_text, re.DOTALL)
    for point in bullet_points:
        # Check for bullet points without numbers/metrics
        if not re.search(r'\d+', point):
            suggestions["content_improvements"].append(f"Add quantifiable metrics to: '{point.strip()}'")
        
        # Check for bullet points that are too short
        if len(point.strip()) < 30:
            suggestions["content_improvements"].append(f"Expand on this point to be more descriptive: '{point.strip()}'")
    
    # Return dictionary of suggestions
    return suggestions

def format_json_resume(resume_dict):
    """
    Format a structured JSON resume into a readable text format.
    Ensures all standard resume sections are included.
    
    Args:
        resume_dict: Dictionary containing structured resume data
        
    Returns:
        str: Formatted resume text
    """
    formatted = []
    
    # Handle case where the name is a key that contains the entire resume
    if len(resume_dict) == 1 and next(iter(resume_dict)) and isinstance(resume_dict[next(iter(resume_dict))], dict):
        name = next(iter(resume_dict))
        content = resume_dict[name]
        
        # Header
        formatted.append(name)
        
        if "Title" in content:
            formatted.append(content["Title"])
        
        # Contact info
        if "Contact" in content and isinstance(content["Contact"], dict):
            contact_items = []
            for key, value in content["Contact"].items():
                contact_items.append(value)
            formatted.append(" | ".join(contact_items))
        
        formatted.append("")  # Blank line
        
        # Work Experience
        if "Work Experience" in content and isinstance(content["Work Experience"], list):
            formatted.append("WORK EXPERIENCE")
            formatted.append("")
            
            for job in content["Work Experience"]:
                position = job.get("Position", "")
                company = job.get("Company", "")
                date = job.get("Date", "")
                
                formatted.append(f"{position}, {company} ({date})")
                
                if "Responsibilities" in job and isinstance(job["Responsibilities"], list):
                    for resp in job["Responsibilities"]:
                        formatted.append(f"• {resp}")
                
                formatted.append("")  # Space between jobs
        
        # Education
        if "Education" in content and isinstance(content["Education"], dict):
            formatted.append("EDUCATION")
            formatted.append("")
            
            edu = content["Education"]
            degree = edu.get("Degree", "")
            school = edu.get("School", "")
            date = edu.get("Date", "")
            
            formatted.append(f"• {degree}, {school} ({date})")
            formatted.append("")
        
        # Skills
        if "Skills" in content and isinstance(content["Skills"], list):
            formatted.append("SKILLS")
            formatted.append("")
            formatted.append(", ".join(content["Skills"]))
        
        return "\n".join(formatted)
    
    # Handle standard resume format
    # Header section
    if 'name' in resume_dict:
        formatted.append(resume_dict['name'])
    
    if 'title' in resume_dict:
        formatted.append(resume_dict['title'])
    
    # Contact info
    contact_info = []
    if 'email' in resume_dict:
        contact_info.append(resume_dict['email'])
    if 'phone' in resume_dict:
        contact_info.append(resume_dict['phone'])
    if 'linkedin' in resume_dict:
        contact_info.append(resume_dict['linkedin'])
    
    if contact_info:
        formatted.append(' | '.join(contact_info))
    
    formatted.append("")  # Blank line
    
    # Work Experience
    formatted.append("WORK EXPERIENCE")
    formatted.append("")
    
    if 'work_experience' in resume_dict and isinstance(resume_dict['work_experience'], list):
        for job in resume_dict['work_experience']:
            job_title = job.get('position', '')
            company = job.get('company', '')
            dates = job.get('dates', '')
            
            formatted.append(f"{job_title}, {company} ({dates})")
            
            if 'highlights' in job and isinstance(job['highlights'], list):
                for highlight in job['highlights']:
                    formatted.append(f"• {highlight}")
            
            formatted.append("")  # Space between jobs
    
    # Education
    formatted.append("EDUCATION")
    formatted.append("")
    
    if 'education' in resume_dict:
        edu = resume_dict['education']
        if isinstance(edu, dict):
            degree = edu.get('degree', '')
            major = edu.get('major', '')
            university = edu.get('university', '')
            dates = edu.get('dates', '')
            
            if major:
                formatted.append(f"• {degree}, {major}, {university} ({dates})")
            else:
                formatted.append(f"• {degree}, {university} ({dates})")
        elif isinstance(edu, list):
            for school in edu:
                degree = school.get('degree', '')
                major = school.get('major', '')
                university = school.get('university', '')
                dates = school.get('dates', '')
                
                if major:
                    formatted.append(f"• {degree}, {major}, {university} ({dates})")
                else:
                    formatted.append(f"• {degree}, {university} ({dates})")
    
    formatted.append("")  # Blank line
    
    # Skills
    formatted.append("SKILLS")
    formatted.append("")
    
    if 'skills' in resume_dict:
        if isinstance(resume_dict['skills'], list):
            formatted.append(', '.join(resume_dict['skills']))
        else:
            formatted.append(resume_dict['skills'])
    
    return '\n'.join(formatted)

def display_rule_based_suggestions(suggestions):
    """
    Format and display rule-based suggestions in a human-readable format.
    
    Args:
        suggestions: Dictionary containing rule-based suggestions
    """
    print("=== WEAK VERBS SUGGESTIONS ===")
    if suggestions["weak_verbs"]:
        for i, suggestion in enumerate(suggestions["weak_verbs"], 1):
            print(f"{i}. {suggestion}")
    else:
        print("No weak verb suggestions found.")
    
    print("\n=== FORMATTING SUGGESTIONS ===")
    if suggestions["formatting_issues"]:
        for i, suggestion in enumerate(suggestions["formatting_issues"], 1):
            print(f"{i}. {suggestion}")
    else:
        print("No formatting suggestions found.")
    
    print("\n=== CONTENT IMPROVEMENT SUGGESTIONS ===")
    if suggestions["content_improvements"]:
        for i, suggestion in enumerate(suggestions["content_improvements"], 1):
            print(f"{i}. {suggestion}")
    else:
        print("No content improvement suggestions found.")

def main():
    """
    Demonstrate resume optimization with both rule-based and AI approaches.
    """
    logger.info("=== RESUME OPTIMIZATION DEMONSTRATION ===")
    
    # Display original resume
    logger.info("\n=== ORIGINAL RESUME ===\n")
    print(SAMPLE_RESUME)
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("No OpenAI API key found. Using rule-based optimization only.")
        use_ai = False
    else:
        use_ai = True
    
    # Step 1: Rule-based suggestions
    logger.info("\n=== RULE-BASED SUGGESTIONS ===\n")
    rule_based_result = rewrite_resume(
        resume_text=SAMPLE_RESUME,
        job_description=SAMPLE_JOB_DESCRIPTION,
        api_key=api_key,
        use_ai=False  # Only use rule-based optimization
    )
    
    # Display rule-based suggestions
    display_rule_based_suggestions(rule_based_result["suggestions"])
    
    # Step 2: If API key is available, also run with AI
    if use_ai:
        logger.info("\n=== AI-BASED OPTIMIZATION ===\n")
        
        # Run the AI-based optimization with explicit settings to prevent job title changes
        ai_result = rewrite_resume(
            resume_text=SAMPLE_RESUME,
            job_description=SAMPLE_JOB_DESCRIPTION,
            api_key=api_key,
            use_ai=True,  # Use AI-based optimization
            avoid_fabricated_metrics=True  # Don't fabricate metrics
        )
        
        # Display AI-enhanced resume
        logger.info("\n=== AI-ENHANCED RESUME ===\n")
        print(ai_result["rewritten_resume"])
        
        # Show improvements made by the AI
        logger.info("\n=== AI IMPROVEMENTS ===\n")
        improvements = ai_result.get("improvements", [])
        if improvements:
            for i, improvement in enumerate(improvements, 1):
                print(f"{i}. {improvement}")
        else:
            print("No specific improvements listed")
    
    logger.info("\n=== OPTIMIZATION COMPLETE ===\n")

if __name__ == "__main__":
    main() 