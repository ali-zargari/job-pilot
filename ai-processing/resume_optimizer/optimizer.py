"""
Two-tier AI processing system for resume optimization.
Combines fast initial drafting with precision optimization.
"""

import logging
from typing import Dict, List, Optional, Union
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Import other modules - use absolute imports
try:
    from ai_processing.resume_gpt import enhance_resume, enhance_bullet
    from ai_processing.resume_lint import analyze_resume
except ImportError:
    try:
        # Try alternative import if package not installed
        from resume_gpt import enhance_resume, enhance_bullet
        from resume_lint import analyze_resume
    except ImportError:
        logger.warning("Could not import resume_gpt or resume_lint modules. Some functionality may be limited.")

import openai
from openai import OpenAI

class ResumeOptimizer:
    """
    Two-tier AI system for resume optimization.
    Combines fast GPT-4 drafting with precision fine-tuning.
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        embedding_model: str = "text-embedding-ada-002",
        gpt_model: str = "gpt-4",
        use_embeddings: bool = True
    ):
        """
        Initialize the resume optimizer.
        
        Args:
            openai_api_key: OpenAI API key for GPT-4 and embeddings
            embedding_model: Model to use for embeddings
            gpt_model: GPT model to use for initial drafting
            use_embeddings: Whether to use embedding-based matching
        """
        self.openai_api_key = openai_api_key
        self.client = None
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        
        self.embedding_model = embedding_model
        self.gpt_model = gpt_model
        self.use_embeddings = use_embeddings
        
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using OpenAI's API.
        
        Args:
            text: Text to get embedding for
            
        Returns:
            Embedding vector
        """
        if not self.client:
            raise ValueError("OpenAI API key required for embeddings")
            
        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model
        )
        return response.data[0].embedding
        
    def draft_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict:
        """
        First tier: Fast initial draft using GPT-4.
        
        Args:
            resume_text: Original resume text
            job_description: Target job description (optional)
            
        Returns:
            Dictionary with draft improvements
        """
        if not self.client:
            # Fall back to T5 model if no OpenAI API key
            logger.info("No OpenAI API key, using T5 model for drafting")
            return enhance_resume([resume_text])[0]
            
        # Use GPT-4 for initial draft
        prompt = f"Optimize this resume bullet point to be more impactful and achievement-focused:\n\n{resume_text}"
        if job_description:
            prompt += f"\n\nTarget job description:\n{job_description}"
            
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[
                {"role": "system", "content": "You are a professional resume writer. Optimize resume content to be impactful, achievement-focused, and ATS-friendly."},
                {"role": "user", "content": prompt}
            ]
        )
        
        draft_text = response.choices[0].message.content
        
        return {
            "original": resume_text,
            "enhanced": draft_text
        }
        
    def optimize_resume(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        reference_resumes: Optional[List[str]] = None
    ) -> Dict:
        """
        Full two-tier optimization process.
        
        Args:
            resume_text: Original resume text
            job_description: Target job description (optional)
            reference_resumes: List of successful reference resumes (optional)
            
        Returns:
            Dictionary with optimization results
        """
        if not resume_text:
            raise ValueError("Resume text cannot be empty")
            
        # Step 1: Get embeddings if enabled
        if self.use_embeddings and reference_resumes and self.client:
            try:
                resume_embedding = self.get_embedding(resume_text)
                # TODO: Compare with reference resume embeddings
                # This would inform the optimization process
            except Exception as e:
                logger.warning(f"Failed to get embeddings: {str(e)}")
            
        # Step 2: Fast initial draft
        try:
            draft_result = self.draft_resume(resume_text, job_description)
        except Exception as e:
            logger.warning(f"Failed to create draft: {str(e)}. Using original text.")
            draft_result = {"original": resume_text, "enhanced": resume_text}
        
        # Step 3: Precision optimization
        # First, analyze with resume_lint
        lint_result = analyze_resume(draft_result["enhanced"])
        
        # Apply fixes based on lint results
        optimized_text = draft_result["enhanced"]
        if lint_result["issues"]:
            # Try to use T5 model to fix specific issues
            try:
                # Only try to fix issues that have text
                issues_with_text = [issue for issue in lint_result["issues"] if "text" in issue]
                if issues_with_text:
                    fixes = enhance_resume([issue["text"] for issue in issues_with_text])
                    # TODO: Apply fixes to the draft text
            except Exception as e:
                logger.warning(f"Failed to apply fixes with T5: {str(e)}")
            
        return {
            "original": resume_text,
            "draft": draft_result["enhanced"],
            "optimized": optimized_text,
            "lint_results": lint_result,
            "score": lint_result.get("score", 0)
        }
        
    def get_suggestions(
        self,
        resume_text: str,
        job_description: Optional[str] = None
    ) -> List[Dict]:
        """
        Get inline suggestions for resume improvements.
        
        Args:
            resume_text: Original resume text
            job_description: Target job description (optional)
            
        Returns:
            List of suggested improvements
        """
        # First, get lint results
        lint_result = analyze_resume(resume_text)
        
        suggestions = []
        for issue in lint_result["issues"]:
            suggestion = {
                "text": issue.get("text", resume_text[:100] + "..." if len(resume_text) > 100 else resume_text),
                "message": issue["message"],
                "severity": issue["severity"],
                "type": issue["type"]
            }
            
            # Get AI-suggested fix
            if "alternatives" in issue:
                suggestion["alternatives"] = issue["alternatives"]
            else:
                # Try to use OpenAI for alternatives if text exists and we have an API key
                if "text" in issue and self.client:
                    try:
                        # Try to use T5 model, but fallback to OpenAI if it fails
                        try:
                            enhanced = enhance_bullet(issue["text"])
                            suggestion["alternatives"] = [enhanced]
                        except Exception as e:
                            # If T5 enhancement fails, use OpenAI
                            logger.warning(f"T5 enhancement failed: {str(e)}. Using OpenAI fallback.")
                            prompt = f"Make this resume bullet more impactful and achievement-focused: '{issue['text']}'"
                            response = self.client.chat.completions.create(
                                model=self.gpt_model,
                                messages=[
                                    {"role": "system", "content": "You are a professional resume writer. Optimize resume content to be impactful, achievement-focused, and ATS-friendly."},
                                    {"role": "user", "content": prompt}
                                ]
                            )
                            enhanced = response.choices[0].message.content
                            suggestion["alternatives"] = [enhanced]
                    except Exception as e:
                        logger.error(f"Failed to generate alternatives: {str(e)}")
                        suggestion["alternatives"] = ["Could not generate alternatives - try installing sentencepiece or check API key"]
                else:
                    suggestion["alternatives"] = ["Improve format and structure"]
                
            suggestions.append(suggestion)
            
        return suggestions

# Create singleton instance
optimizer = None

def get_optimizer(**kwargs) -> ResumeOptimizer:
    """Get or create a ResumeOptimizer instance."""
    global optimizer
    if optimizer is None:
        optimizer = ResumeOptimizer(**kwargs)
    return optimizer 