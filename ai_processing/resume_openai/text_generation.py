"""
OpenAI text generation module for resume enhancement.
"""

import logging
import json
from typing import List, Dict, Any, Optional, Union
import re

from .client import get_openai_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def extract_skills(resume_text: str) -> List[str]:
    """
    Extract skills from a resume text.
    
    Args:
        resume_text: The resume text to extract skills from
        
    Returns:
        List of skills extracted from the resume
    """
    skills = []
    
    # Look for a skills section in the resume
    skill_section_match = re.search(r'(?i)SKILLS\s*\n(.*?)(\n\n|\Z)', resume_text, re.DOTALL)
    if skill_section_match:
        # Extract skills text
        skills_text = skill_section_match.group(1)
        
        # Split by common separators
        for separator in [',', '•', '|', '/', ';']:
            if separator in skills_text:
                skills = [skill.strip() for skill in skills_text.split(separator) if skill.strip()]
                break
                
        # If no separators found, try splitting by whitespace
        if not skills:
            skills = [skill.strip() for skill in skills_text.split() if skill.strip()]
    
    return skills

def generate_text(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 1000,
    temperature: float = 0.7,
    api_key: Optional[str] = None,
    as_json: bool = False
) -> Union[str, Dict[str, Any]]:
    """
    Generate text using OpenAI's GPT model.
    
    Args:
        prompt: User prompt for generation
        system_prompt: Optional system prompt
        model: Model to use for generation
        max_tokens: Maximum tokens to generate
        temperature: Temperature for generation
        api_key: Optional API key override
        as_json: Whether to parse response as JSON
        
    Returns:
        Generated text or JSON object if as_json=True
    """
    # Get client
    client = get_openai_client(api_key=api_key)
    
    # Check if client is available
    if not client.is_available or not client.get_client():
        logger.warning("OpenAI client not available for text generation")
        return "" if not as_json else {}
    
    try:
        # Prepare messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Add JSON response format if needed
        response_format = {"type": "json_object"} if as_json else None
        
        # Call OpenAI API
        response = client.get_client().chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format
        )
        
        # Increment API call counter
        client.increment_api_call_count()
        
        # Return generated text
        generated_text = response.choices[0].message.content
        
        # Parse JSON if requested
        if as_json and generated_text:
            try:
                return json.loads(generated_text)
            except json.JSONDecodeError:
                logger.warning("Failed to parse response as JSON")
                return generated_text
        
        return generated_text
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        return "" if not as_json else {}

def enhance_text(
    text: str,
    goal: str = "improve",
    api_key: Optional[str] = None
) -> str:
    """
    Enhance text using OpenAI GPT.
    
    Args:
        text: Text to enhance
        goal: Enhancement goal (improve, formalize, etc.)
        api_key: Optional API key override
        
    Returns:
        Enhanced text
    """
    # Don't process empty text
    if not text:
        return text
    
    # Prepare system prompt
    system_prompt = f"""You are an expert resume writer. 
Your task is to enhance the given text while maintaining facts and truthfulness. 
Focus on: clear communication, active voice, quantifiable achievements, and professional language.
The enhancement goal is to {goal} the text."""
    
    # Generate enhanced text
    return generate_text(
        prompt=f"Text to enhance: {text}",
        system_prompt=system_prompt,
        max_tokens=len(text) * 2,  # Allow for expansion
        temperature=0.6,  # Lower temperature for more predictable results
        api_key=api_key
    )

def rewrite_resume(
    resume_text: str,
    job_description: Optional[str] = None,
    skills: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    use_ai: bool = True,
    avoid_fabricated_metrics: bool = True,
    custom_instructions: Optional[str] = None
) -> Dict[str, Any]:
    """
    Rewrite a resume to improve its quality and job-matching.
    
    Args:
        resume_text: Original resume text
        job_description: Optional job description for targeting
        skills: Optional list of skills to emphasize (if None, will be extracted from resume)
        api_key: Optional API key override
        use_ai: Whether to use AI for enhancement or return only rule-based suggestions
        avoid_fabricated_metrics: Whether to avoid fabricating specific metrics
        custom_instructions: Optional custom instructions to guide the AI rewrite
        
    Returns:
        Dictionary with rewritten resume and metadata
    """
    # Initialize result structure
    result = {
        "rewritten_resume": "",
        "improvements": [],
        "api_used": False,
        "api_calls": 0,
        "suggestions": {}
    }
    
    # Extract skills if not provided
    if skills is None:
        skills = extract_skills(resume_text)
    
    # Perform rule-based analysis regardless of AI usage
    rule_based_suggestions = {}
    
    # Define weak verb replacements
    weak_verb_replacements = {
        "responsible for": "managed",
        "worked on": "developed",
        "helped": "assisted with",
        "part of": "contributed to",
        "developed": "built",
        "maintained": "managed",
        "participated in": "contributed to",
        "assisted": "supported"
    }
    
    # Generate rule-based suggestions
    weak_verbs = []
    for weak_verb, strong_verb in weak_verb_replacements.items():
        # Look for weak verbs at the start of bullet points
        pattern = r'(•\s*)' + weak_verb
        matches = re.finditer(pattern, resume_text, flags=re.IGNORECASE)
        for match in matches:
            original_text = match.group(0)
            suggestion = f"Replace '{weak_verb}' with '{strong_verb}' in '{original_text}'"
            weak_verbs.append(suggestion)
    
    # Find formatting issues
    formatting_issues = []
    # Check for bullet points without spaces
    inconsistent_bullets = re.findall(r'•(\S)', resume_text)
    if inconsistent_bullets:
        formatting_issues.append("Ensure consistent spacing after bullet points")
    
    # Check for excessive line breaks
    if re.search(r'\n{3,}', resume_text):
        formatting_issues.append("Normalize spacing between sections to be consistent")
    
    # Find content improvement opportunities
    content_improvements = []
    bullet_points = re.findall(r'•\s*(.*?)(?=\n•|\n\n|\Z)', resume_text, re.DOTALL)
    for point in bullet_points:
        # Check for bullet points without numbers/metrics
        if not re.search(r'\d+', point):
            content_improvements.append(f"Add quantifiable metrics to: '{point.strip()}'")
        
        # Check for bullet points that are too short
        if len(point.strip()) < 30:
            content_improvements.append(f"Expand on this point to be more descriptive: '{point.strip()}'")
    
    # Store rule-based suggestions
    rule_based_suggestions = {
        "weak_verbs": weak_verbs,
        "formatting_issues": formatting_issues,
        "content_improvements": content_improvements
    }
    
    result["suggestions"] = rule_based_suggestions
    
    # If AI is not requested, just return the rule-based suggestions
    if not use_ai:
        result["rewritten_resume"] = resume_text
        return result
    
    # Try to extract job titles to ensure they aren't changed
    job_titles = []
    job_sections = re.findall(r'([A-Za-z\s]+),\s+([A-Za-z\s]+)\s+\(([^)]+)\)', resume_text)
    for match in job_sections:
        job_titles.append(match[0].strip())  # First group is the job title
    
    # Prepare system prompt for AI enhancement
    system_prompt = """You are an expert resume rewriter. 
Your task is to enhance the given resume while maintaining 100% truthfulness.
Focus on: clear communication, active voice, achievements, and professional language.

CONTEXT PRESERVATION RULES:
1. When you see numerical values or metrics in the original text (e.g., "~100% performance improvement", "30% faster"), 
   you MUST preserve the ENTIRE CONTEXT of the achievement.
2. SPECIFIC EXAMPLES of what must be preserved exactly as written:
   - "Optimized system performance by implementing multi-threading, achieving a ~100% performance improvement"
   - "Developed a PID-driven emotional prediction algorithm, significantly improving readability of feedback"
3. You can enhance surrounding language, but specific technologies (multi-threading, PID-driven algorithm) and 
   the associated metrics MUST remain intact.

CRITICAL: DO NOT REMOVE ANY EXISTING QUANTIFIABLE METRICS. Any numbers, percentages, or specific metrics already present in the original resume MUST be preserved exactly as written.
CRITICAL: DO NOT CHANGE ANY JOB TITLES UNDER ANY CIRCUMSTANCES. Job titles are factual information that must remain exactly as provided.
CRITICAL: DO NOT CHANGE ANY COMPANY NAMES UNDER ANY CIRCUMSTANCES.
CRITICAL: DO NOT CHANGE ANY DATES UNDER ANY CIRCUMSTANCES.
CRITICAL: DO NOT CHANGE ANY EDUCATION DETAILS UNDER ANY CIRCUMSTANCES.

IMPORTANT: Your response MUST include ALL sections from the original resume with the exact same structure and format.
This includes: Name, Title, Contact Information, Work Experience, Education, and Skills sections.
Preserve all original contact information (email, phone, LinkedIn), job titles, companies, dates, and skills.
Use the EXACT same bullet point format (•) as the original resume.

PRESERVING STRENGTHS: The resume already contains excellent elements that should not be changed:
1. If the resume contains quantifiable achievements (numbers, percentages, metrics), preserve them ALL exactly as written
2. If the resume uses strong action verbs, keep those exact verbs
3. Only enhance areas that need improvement - don't change what's already effective

When tailoring for a job description:
1. Analyze which skills and experiences from the resume most closely match the job requirements
2. Emphasize those relevant skills and experiences more prominently
3. Use the same terminology and keywords from the job description where appropriate
4. Focus extra attention on making the resume match the job description closely
"""

    # Add metrics guidance if requested
    if avoid_fabricated_metrics:
        system_prompt += """
IMPORTANT ABOUT METRICS:
1. NEVER remove any existing metrics - preserve ALL numbers, dollar amounts, percentages, and quantifiable achievements
2. DO NOT fabricate specific numbers or percentages if they were not in the original resume
3. If no specific metrics exist in a particular bullet point, use qualitative terms like "significantly improved", 
   "effectively managed", or "consistently delivered" instead of making up numbers
4. If a number or metric is present in the original resume, preserve it exactly as written - do not remove or change it
5. Quantify achievements in general terms only when original metrics are not available
6. Pay special attention to preserving approximate percentages like "~100%" - these must remain exactly as written
"""

    system_prompt += "\nMake the resume more impressive without fabricating details."
    
    # If job titles were extracted, add them to the prompt explicitly
    if job_titles:
        system_prompt += f"\n\nPRESERVE THESE EXACT JOB TITLES: {', '.join(job_titles)}"
    
    # Add custom instructions if provided
    if custom_instructions:
        system_prompt += f"\n\nADDITIONAL INSTRUCTIONS: {custom_instructions}"
    
    # Prepare user prompt
    prompt = f"Original resume:\n{resume_text}\n\n"
    
    # Add job description if provided
    if job_description:
        prompt += f"Target job description:\n{job_description}\n\n"
        system_prompt += "\nOptimize the resume to match the target job description."
    
    # Add skills if provided
    if skills:
        prompt += f"Skills to emphasize: {', '.join(skills)}\n\n"
        system_prompt += "\nEmphasize the listed skills in the resume."
    
    # Complete the prompt with instructions
    prompt += """Instructions: 
1. Rewrite the resume to be more impressive, professional, and effective.
2. Maintain the SAME SECTIONS and FORMAT as the original resume.
3. NEVER CHANGE JOB TITLES, COMPANY NAMES, OR DATES - these must remain exactly as in the original.
4. Preserve ALL contact information (email, phone, LinkedIn).
5. Use active voice and emphasize achievements.
6. Keep all original job titles, companies, dates, education details, and skills.
7. Use the EXACT same bullet point format as the original resume.
"""

    # Add metrics guidance to the prompt if requested
    if avoid_fabricated_metrics:
        prompt += """
8. DO NOT make up specific percentages or numbers unless they were in the original resume.
9. Use qualitative language to imply improvement instead of fabricated metrics.
"""
    
    # Get client
    client = get_openai_client(api_key=api_key)
    
    try:
        # First try getting plain text output for better format preservation
        enhanced_resume = generate_text(
            prompt=prompt,
            system_prompt=system_prompt,
            model="gpt-3.5-turbo",
            max_tokens=2000,
            temperature=0.5,
            api_key=api_key,
            as_json=False
        )
        
        # Validate that job titles were not changed
        for title in job_titles:
            if title not in enhanced_resume:
                # If a job title was changed, insert a warning
                enhanced_resume = f"WARNING: Job titles have been incorrectly modified. Please review.\n\n{enhanced_resume}"
                break
        
        # Generate a list of improvements (in a separate call to keep main output clean)
        improvements_prompt = f"""Given the original resume:
{resume_text}

And the enhanced resume:
{enhanced_resume}

List 3-5 key improvements made in the enhanced version.
Focus on substantive content improvements, not formatting or job title changes.
"""
        
        improvements_response = generate_text(
            prompt=improvements_prompt,
            system_prompt="You are an expert resume analyst. Provide a concise, numbered list of specific improvements made in the enhanced resume.",
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.5,
            api_key=api_key,
            as_json=False
        )
        
        # Process improvements into a list
        improvements = []
        for line in improvements_response.strip().split("\n"):
            if re.match(r'^\d+\.', line.strip()):
                # Filter out any improvements mentioning job title changes
                improvement = line.strip().split(".", 1)[1].strip()
                if not any(term in improvement.lower() for term in ["job title", "position title", "title change"]):
                    improvements.append(improvement)
        
        result.update({
            "rewritten_resume": enhanced_resume,
            "improvements": improvements,
            "api_used": True,
            "api_calls": client.get_api_call_count() if hasattr(client, 'get_api_call_count') else 2
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Error in AI resume rewriting: {str(e)}")
        # In case of failure, fall back to simple text enhancement
        try:
            enhanced_resume = enhance_text(resume_text, "optimize for job applications", api_key)
            if enhanced_resume:
                result.update({
                    "rewritten_resume": enhanced_resume,
                    "api_used": True,
                    "api_calls": client.get_api_call_count() if hasattr(client, 'get_api_call_count') else 1
                })
            return result
        except:
            # If even the fallback fails, return original text
            result["rewritten_resume"] = resume_text
            return result 