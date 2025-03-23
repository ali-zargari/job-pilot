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
    Apply ONLY legitimate rule-based improvements to a resume without fabricating any data.
    Only replaces weak verbs with stronger ones and fixes formatting issues.
    
    Args:
        resume_text: Original resume text
        
    Returns:
        str: Rule-based optimized resume
    """
    optimized = resume_text
    
    # Replace weak verbs with stronger ones
    for weak_verb, strong_verb in WEAK_VERB_REPLACEMENTS.items():
        # Use regex to match only at the start of bullet points
        pattern = r'(•\s*)' + weak_verb
        replacement = r'\1' + strong_verb
        optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
    
    # Fix formatting issues
    # Ensure consistent bullet point format (• with a space after)
    optimized = re.sub(r'•(\S)', r'• \1', optimized)
    
    # Ensure consistent spacing between sections
    optimized = re.sub(r'\n{3,}', r'\n\n', optimized)
    
    return optimized

def format_json_resume(resume_dict):
    """
    Format a structured JSON resume into a readable text format.
    
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
            
            formatted.append(f"• {degree}, {major}, {university} ({dates})")
        elif isinstance(edu, list):
            for school in edu:
                degree = school.get('degree', '')
                major = school.get('major', '')
                university = school.get('university', '')
                dates = school.get('dates', '')
                
                formatted.append(f"• {degree}, {major}, {university} ({dates})")
    
    formatted.append("")  # Blank line
    
    # Skills
    if 'skills' in resume_dict:
        formatted.append("SKILLS")
        formatted.append("")
        
        if isinstance(resume_dict['skills'], list):
            formatted.append(', '.join(resume_dict['skills']))
        else:
            formatted.append(resume_dict['skills'])
    
    return '\n'.join(formatted)

def main():
    """
    Demonstrate resume optimization with both rule-based and AI approaches.
    """
    logger.info("=== RESUME OPTIMIZATION DEMONSTRATION ===")
    
    # Display original resume
    logger.info("\n=== ORIGINAL RESUME ===\n")
    print(SAMPLE_RESUME)
    
    # Step 1: Apply TRULY rule-based optimization only
    logger.info("\n=== APPLYING TRULY RULE-BASED OPTIMIZATION (NO AI) ===\n")
    
    # Apply our custom rule-based optimization that doesn't fabricate data
    rule_based_result = truly_rule_based_optimize(SAMPLE_RESUME)
    
    # Display rule-based optimized resume
    logger.info("\n=== TRULY RULE-BASED OPTIMIZED RESUME (NO AI) ===\n")
    print(rule_based_result)
    
    # Step 2: Apply AI-based optimization (using OpenAI)
    logger.info("\n=== APPLYING AI-BASED OPTIMIZATION ===\n")
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("No OpenAI API key found. Skipping AI optimization.")
        return
    
    # Apply AI rewrite to the original resume
    ai_result = rewrite_resume(
        resume_text=SAMPLE_RESUME,  # Note: using original resume, not rule-based
        job_description=SAMPLE_JOB_DESCRIPTION,
        skills=["Python", "Backend Development", "Database Design", "AWS", "Agile"],
        api_key=api_key
    )
    
    # Display AI-enhanced resume
    logger.info("\n=== AI-ENHANCED RESUME ===\n")
    
    # Handle different return types for rewritten_resume
    rewritten = ai_result.get("rewritten_resume", "")
    
    if isinstance(rewritten, str):
        print(rewritten)
    elif isinstance(rewritten, dict):
        # Format the structured JSON into a proper resume format
        formatted_resume = format_json_resume(rewritten)
        print(formatted_resume)
        
        # Also show the raw JSON for reference
        logger.info("\n=== AI-ENHANCED RESUME (RAW JSON) ===\n")
        print(json.dumps(rewritten, indent=2))
    else:
        logger.warning("Unexpected format for AI-enhanced resume")
    
    # Show improvements made by the AI
    logger.info("\n=== AI IMPROVEMENTS ===\n")
    improvements = ai_result.get("improvements", [])
    if improvements:
        if isinstance(improvements, list):
            for i, improvement in enumerate(improvements, 1):
                print(f"{i}. {improvement}")
        elif isinstance(improvements, dict):
            for category, items in improvements.items():
                print(f"=== {category} ===")
                if isinstance(items, list):
                    for item in items:
                        print(f"• {item}")
                else:
                    print(f"• {items}")
    else:
        print("No specific improvements listed")

if __name__ == "__main__":
    main() 