#!/usr/bin/env python
"""
Command-line interface for resume optimization.

This module provides the command-line functionality for optimizing resumes.
It handles argument parsing, file I/O, and displays results.
"""

import os
import sys
import argparse
import logging
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from ai_processing.resume_optimizer import get_optimizer
from ai_processing.utilities import (
    read_file_content,
    write_file_content,
    format_text_for_display,
    ensure_directory_exists
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def improved_rule_based_optimization(resume, job_description=None):
    """Apply enhanced rule-based optimization with grammar fixes."""
    logger.info("Running improved rule-based optimization...")
    
    # Track the section we're in to apply context-specific rules
    current_section = "UNKNOWN"
    bullet_point_pattern = r'^\s*[•●■◦○◆▪▫-]\s*'
    
    # Split the resume into lines for processing
    lines = resume.strip().split('\n')
    optimized_lines = []
    
    # First stage: Section and context detection
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            optimized_lines.append("")
            continue
            
        # Detect sections (typically uppercase)
        if line.isupper() and len(line) > 3 and not line.startswith('•'):
            current_section = line
            optimized_lines.append(line)
            continue
        
        # Specific handling based on section
        if current_section == "WORK EXPERIENCE" or "EXPERIENCE" in current_section:
            # Handle job titles and company info
            if "(" in line and ")" in line and not line.startswith('•'):
                optimized_lines.append(line)
                continue
                
            # Process bullet points
            import re
            is_bullet = bool(re.match(bullet_point_pattern, line))
            
            if is_bullet:
                # Remove the bullet for processing
                text = re.sub(bullet_point_pattern, '', line)
                
                # First, apply targeted exact replacements
                replacements = {
                    "responsible for": "managed",
                    "was responsible for": "managed",
                    "duties included": "delivered",
                    "helped with": "contributed to",
                    "worked on": "developed",
                    "assisted in": "collaborated on",
                    "helped in": "supported",
                    "tasked with": "executed",
                    "was tasked with": "executed",
                    "was in charge of": "led",
                    "in charge of": "led",
                    "was making sure": "ensured",
                    "making sure": "ensuring",
                    "designed team": "design team",
                    "was involved in": "contributed to"
                }
                
                for old, new in replacements.items():
                    text = text.replace(old, new)
                    # Also try with capitalized first letter
                    text = text.replace(old.capitalize(), new.capitalize())
                
                # Second, apply grammar fixes
                # Fix capitalization
                if text and text[0].islower():
                    text = text[0].upper() + text[1:]
                
                # Ensure periods at the end of bullet points
                if text and not text.endswith(('.', '!', '?')):
                    text += '.'
                    
                # Remove unnecessary "that" in certain contexts
                text = text.replace(" that improved", " improving")
                text = text.replace(" that increased", " increasing")
                text = text.replace(" that decreased", " decreasing")
                text = text.replace(" that reduced", " reducing")
                text = text.replace(" that enhanced", " enhancing")
                
                # Fix verb tense issues (ensure past tense for work experience)
                present_to_past = {
                    "develop": "developed",
                    "create": "created",
                    "implement": "implemented",
                    "design": "designed",
                    "manage": "managed",
                    "lead": "led",
                    "build": "built",
                    "coordinate": "coordinated",
                    "ensure": "ensured",
                    "improve": "improved",
                    "increase": "increased",
                    "decrease": "decreased",
                    "reduce": "reduced",
                    "enhance": "enhanced",
                    "maintain": "maintained",
                    "optimize": "optimized",
                    "collaborate": "collaborated",
                    "contribute": "contributed",
                    "execute": "executed",
                    "deliver": "delivered",
                    "support": "supported"
                }
                
                # Only replace at the beginning of the bullet or after auxiliaries
                words = text.split()
                for i, word in enumerate(words):
                    # Clean word from punctuation for comparison
                    clean_word = word.lower().rstrip(',.;:')
                    if clean_word in present_to_past:
                        if i == 0 or words[i-1].lower() in ('to', 'and', 'or'):
                            # Replace while preserving capitalization
                            if word[0].isupper():
                                words[i] = present_to_past[clean_word].capitalize()
                            else:
                                words[i] = present_to_past[clean_word]
                
                text = ' '.join(words)
                
                # Restore the bullet point
                optimized_lines.append(f"• {text}")
            else:
                optimized_lines.append(line)
        
        elif current_section == "EDUCATION":
            # Fix capitalization in degree names
            if "bachelor" in line.lower() or "master" in line.lower() or "phd" in line.lower():
                words = line.split()
                for i, word in enumerate(words):
                    if word.lower() in ("bachelor", "master", "bachelor's", "master's", "phd", "doctorate", "associate"):
                        words[i] = word.capitalize()
                    elif word.lower() in ("of", "in", "and", "the"):
                        continue
                    elif i > 0 and words[i-1].lower() in ("bachelor", "master", "bachelor's", "master's", "phd", "doctorate", "associate", "of", "in"):
                        words[i] = word.capitalize()
                optimized_lines.append(" ".join(words))
            else:
                optimized_lines.append(line)
        
        elif current_section == "SKILLS" or "SKILLS" in current_section:
            # Properly capitalize technical terms
            tech_terms = {
                "javascript": "JavaScript",
                "typescript": "TypeScript",
                "html": "HTML",
                "css": "CSS",
                "react": "React",
                "node.js": "Node.js",
                "nodejs": "Node.js",
                "python": "Python",
                "java": "Java",
                "c#": "C#",
                "c++": "C++",
                "php": "PHP",
                "ruby": "Ruby",
                "aws": "AWS",
                "azure": "Azure",
                "gcp": "GCP",
                "docker": "Docker",
                "kubernetes": "Kubernetes",
                "mongodb": "MongoDB",
                "mysql": "MySQL",
                "postgresql": "PostgreSQL",
                "sql": "SQL",
                "nosql": "NoSQL",
                "git": "Git",
                "jenkins": "Jenkins",
                "jira": "Jira",
                "agile": "Agile",
                "scrum": "Scrum",
                "devops": "DevOps",
                "ci/cd": "CI/CD"
            }
            
            words = []
            for word in line.split():
                word_clean = word.lower().rstrip(',.;:')
                if word_clean in tech_terms:
                    # Replace while preserving any trailing punctuation
                    suffix = word[len(word_clean):]
                    words.append(tech_terms[word_clean] + suffix)
                else:
                    words.append(word)
            
            optimized_lines.append(" ".join(words))
        
        else:
            # General processing for other sections
            optimized_lines.append(line)
    
    # Join the optimized lines back into a resume
    optimized_resume = "\n".join(optimized_lines)
    
    return optimized_resume


def get_direct_openai_optimization(resume, job_description, api_key, job_tailored=False):
    """Get AI optimization directly using OpenAI API."""
    if not api_key:
        logger.warning("No API key provided for OpenAI. Can't perform AI optimization.")
        return resume
    
    optimization_type = "job-tailored" if job_tailored else "general"
    logger.info(f"Running OpenAI optimization ({optimization_type})...")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Base system prompt emphasizing factual content and grammar cleanup
    system_prompt = """
    You are a professional resume editor with expertise in optimizing resumes.
    
    IMPORTANT RULES:
    1. DO NOT INVENT or ADD any achievements, metrics, or skills that aren't mentioned in the original
    2. DO NOT CHANGE job titles, company names, or timeframes
    3. Your primary task is to IMPROVE GRAMMAR and WORDING, not to add fabricated content
    4. NEVER add specific percentages or numbers if they don't exist in the original
    5. Start each bullet point with a STRONG ACTION VERB in the PAST TENSE (for Work Experience)
    6. Capitalize the first letter of every bullet point and ensure proper grammar
    7. Maintain the original length of bullet points - don't make sentences much longer
    8. Make sure all technical terms are properly capitalized (JavaScript, HTML, CSS, etc.)
    
    Specifically focus on:
    - Correcting grammar and syntax errors
    - Replacing weak phrases with stronger alternatives
    - Ensuring consistent tense and formatting
    - Improving clarity and readability
    - Using appropriate professional language
    """
    
    # Add job-tailored guidance if needed
    if job_tailored:
        system_prompt += """
    For job-tailored optimization:
    - Reorganize bullet points to prioritize experiences most relevant to the job description
    - Highlight existing skills that match the job requirements
    - Use terminology from the job description ONLY IF it accurately reflects existing experience
    - Emphasize transferable skills relevant to the job posting
    - Maintain factual integrity - do not add skills or experience not in the original resume
    """
    
    user_prompt = f"""
    Please optimize the following resume text. Remember to follow the rules about not inventing content.
    
    {"I also want you to consider this job description for targeted optimization:\n" + job_description if job_tailored else ""}
    
    RESUME TO OPTIMIZE:
    {resume}
    
    Remember, ONLY improve grammar, wording, and structure. DO NOT add any achievements or metrics that aren't mentioned in the original.
    """
    
    start_time = time.time()
    
    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4" if "gpt-4" in os.getenv("GPT_MODEL", "") else "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,  # Lower temperature for more conservative output
            max_tokens=2000
        )
        
        # Extract the optimized resume
        optimized_resume = response.choices[0].message.content.strip()
        elapsed_time = time.time() - start_time
        
        logger.info(f"OpenAI optimization ({optimization_type}) completed in {elapsed_time:.2f} seconds")
        
        return optimized_resume
        
    except Exception as e:
        logger.error(f"Error in OpenAI optimization: {str(e)}")
        return resume


def print_optimization_results(resume, optimized, method, output_file=None):
    """Print a comparison of original and optimized resumes."""
    output = []
    output.append("\n" + "="*100)
    output.append(f"RESUME OPTIMIZATION USING {method}".center(100))
    output.append("="*100)
    
    # Format resumes for better display
    formatted_original = format_text_for_display(resume)
    formatted_optimized = format_text_for_display(optimized)
    
    output.append("\nORIGINAL RESUME:")
    output.append("-"*100)
    output.append(formatted_original)
    
    output.append("\nOPTIMIZED RESUME:")
    output.append("-"*100)
    output.append(formatted_optimized)
    
    output.append("="*100)
    
    result = "\n".join(output)
    print(result)
    
    # Write to file if specified
    if output_file:
        write_file_content(output_file, result)
        logger.info(f"Results saved to {output_file}")


def print_side_by_side_comparison(versions, output_file=None):
    """Print a side-by-side comparison of multiple resume versions."""
    output = []
    output.append("\n" + "="*100)
    output.append("RESUME OPTIMIZATION COMPARISON".center(100))
    output.append("="*100 + "\n")
    
    # Get all resume versions and format them
    formatted_versions = {}
    for name, content in versions.items():
        formatted_versions[name] = format_text_for_display(content).split('\n')
    
    # Find the maximum length of any version
    max_length = max(len(lines) for lines in formatted_versions.values())
    
    # Pad all versions to the same length
    for name in formatted_versions:
        formatted_versions[name].extend([''] * (max_length - len(formatted_versions[name])))
    
    # Prepare table headers
    headers = list(formatted_versions.keys())
    column_width = 50
    header_row = " | ".join(name.center(column_width) for name in headers)
    
    output.append(header_row)
    output.append('-' * len(header_row))
    
    # Create the side-by-side comparison
    for i in range(max_length):
        row = []
        for name in headers:
            cell = formatted_versions[name][i]
            # Cut long cells to fit in column
            if len(cell) > column_width:
                cell = cell[:column_width-3] + "..."
            row.append(cell.ljust(column_width))
        output.append(" | ".join(row))
    
    output.append("="*100)
    
    result = "\n".join(output)
    print(result)
    
    # Write to file if specified
    if output_file:
        write_file_content(output_file, result)
        logger.info(f"Comparison saved to {output_file}")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Resume Optimization Tool')
    
    parser.add_argument('--resume', required=True, help='Path to the resume file')
    parser.add_argument('--job', required=False, help='Path to the job description file')
    parser.add_argument('--output', required=False, default='optimized_resumes', help='Output directory')
    parser.add_argument('--method', choices=['rule-based', 'ai', 'job-tailored', 'all'], default='rule-based', 
                        help='Optimization method to use')
    parser.add_argument('--compare', action='store_true', help='Show side-by-side comparison')
    
    return parser.parse_args()


def compare_all(original, rule_based, ai=None, job_tailored=None, output_dir=None):
    """Compare all optimization versions."""
    # Prepare versions dictionary
    versions = {
        "Original": original,
        "Rule-Based": rule_based
    }
    
    if ai:
        versions["AI Optimized"] = ai
    
    if job_tailored:
        versions["Job-Tailored"] = job_tailored
    
    # Print side-by-side comparison
    output_file = None
    if output_dir:
        output_file = os.path.join(output_dir, "comparison.txt")
    
    print_side_by_side_comparison(versions, output_file)


def main():
    """Main function for resume optimization."""
    args = parse_arguments()
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if args.method in ('ai', 'job-tailored', 'all') and not api_key:
        logger.warning("No OpenAI API key found. AI methods will be skipped.")
        if args.method in ('ai', 'job-tailored'):
            logger.error("Cannot continue without API key for selected method.")
            sys.exit(1)
    
    # Read input files
    resume = read_file_content(args.resume)
    job_description = read_file_content(args.job) if args.job else None
    
    # Create output directory
    output_dir = args.output
    ensure_directory_exists(output_dir)
    
    # Stage 1: Improved rule-based optimization
    rule_based_resume = improved_rule_based_optimization(resume, job_description)
    
    # Save rule-based optimization result
    rule_based_output = os.path.join(output_dir, "rule_based_resume.txt")
    write_file_content(rule_based_output, rule_based_resume)
    
    # Print rule-based optimization results
    if args.method in ('rule-based', 'all'):
        print_optimization_results(
            resume, 
            rule_based_resume, 
            "RULE-BASED OPTIMIZATION (NO AI)"
        )
    
    # Initialize variables for other optimization methods
    ai_resume = None
    job_tailored_resume = None
    
    # Stage 2: AI optimization if requested
    if args.method in ('ai', 'all') and api_key:
        ai_resume = get_direct_openai_optimization(
            rule_based_resume,  # Use the rule-based result as input
            job_description,
            api_key
        )
        
        # Save AI optimization result
        ai_output = os.path.join(output_dir, "ai_optimized_resume.txt")
        write_file_content(ai_output, ai_resume)
        
        # Print AI optimization results
        print_optimization_results(
            resume,  # Still compare to original
            ai_resume,
            "STANDARD OPENAI OPTIMIZATION (general)"
        )
    
    # Stage 3: Job-tailored optimization if requested
    if args.method in ('job-tailored', 'all') and api_key and job_description:
        job_tailored_resume = get_direct_openai_optimization(
            rule_based_resume,  # Use the rule-based result as input
            job_description,
            api_key,
            job_tailored=True
        )
        
        # Save job-tailored optimization result
        job_tailored_output = os.path.join(output_dir, "job_tailored_resume.txt")
        write_file_content(job_tailored_output, job_tailored_resume)
        
        # Print job-tailored optimization results
        print_optimization_results(
            resume,  # Still compare to original
            job_tailored_resume,
            "JOB-TAILORED OPENAI OPTIMIZATION (job-tailored)"
        )
    
    # Show side-by-side comparison if requested
    if args.compare:
        compare_all(
            original=resume,
            rule_based=rule_based_resume,
            ai=ai_resume,
            job_tailored=job_tailored_resume,
            output_dir=output_dir
        )
    
    logger.info(f"All optimization results saved to directory: {output_dir}")
    
    # Provide a summary of what was done
    print("\nOptimization complete!")
    print(f"- Rule-based optimization: {'✓ Done' if args.method in ('rule-based', 'all') else '✗ Skipped'}")
    print(f"- AI optimization: {'✓ Done' if args.method in ('ai', 'all') and ai_resume else '✗ Skipped'}")
    print(f"- Job-tailored optimization: {'✓ Done' if args.method in ('job-tailored', 'all') and job_tailored_resume else '✗ Skipped'}")
    print(f"\nAll results saved to: {output_dir}")


if __name__ == "__main__":
    main() 