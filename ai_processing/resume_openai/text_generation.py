"""
OpenAI text generation module for resume enhancement.
"""

import logging
import json
from typing import List, Dict, Any, Optional, Union

from .client import get_openai_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

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
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Rewrite a resume to improve its quality and job-matching.
    
    Args:
        resume_text: Original resume text
        job_description: Optional job description for targeting
        skills: Optional list of skills to emphasize
        api_key: Optional API key override
        
    Returns:
        Dictionary with rewritten resume and metadata
    """
    # Prepare system prompt
    system_prompt = """You are an expert resume rewriter. 
Your task is to enhance the given resume while maintaining 100% truthfulness.
Focus on: clear communication, active voice, quantifiable achievements, and professional language.
Preserve all original skills, job titles, dates, and companies.
Make the resume more impressive without fabricating details."""
    
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
    
    # Complete the prompt
    prompt += "Instructions: Rewrite the resume to be more impressive, professional, and effective."
    
    # Get client
    client = get_openai_client(api_key=api_key)
    
    # Get enhanced resume as JSON with structure
    response = generate_text(
        prompt=prompt,
        system_prompt=system_prompt + "\nRespond in JSON format with 'enhanced_resume' and 'improvements' fields.",
        max_tokens=2000,
        temperature=0.5,
        api_key=api_key,
        as_json=True
    )
    
    # Handle response
    if isinstance(response, dict):
        return {
            "rewritten_resume": response.get("enhanced_resume", ""),
            "improvements": response.get("improvements", []),
            "api_used": True,
            "api_calls": client.get_api_call_count()
        }
    else:
        # Fallback to simple text enhancement if JSON parsing failed
        enhanced_resume = enhance_text(resume_text, "optimize for job applications", api_key)
        return {
            "rewritten_resume": enhanced_resume or resume_text,
            "improvements": [],
            "api_used": bool(enhanced_resume),
            "api_calls": client.get_api_call_count()
        } 