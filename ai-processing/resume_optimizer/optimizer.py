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
        
        # Step 1: First analyze with resume_lint to check if it's already optimized
        lint_result = analyze_resume(resume_text)
        
        # If the resume is already well-optimized, return early with validation
        if lint_result.get("is_already_optimized", False):
            logger.info("Resume is already well-optimized, skipping optimization")
            return {
                "original": resume_text,
                "draft": resume_text,  # No changes needed
                "optimized": resume_text,  # No changes needed
                "lint_results": lint_result,
                "score": lint_result.get("score", 95),
                "no_changes_needed": True,
                "message": "Your resume is already well-optimized! It has strong action verbs, quantifiable achievements, and proper formatting."
            }
            
        # Step 2: Get embeddings if enabled
        if self.use_embeddings and reference_resumes and self.client:
            try:
                resume_embedding = self.get_embedding(resume_text)
                # TODO: Compare with reference resume embeddings
                # This would inform the optimization process
            except Exception as e:
                logger.warning(f"Failed to get embeddings: {str(e)}")
            
        # Step 3: Fast initial draft
        try:
            draft_result = self.draft_resume(resume_text, job_description)
        except Exception as e:
            logger.warning(f"Failed to create draft: {str(e)}. Using original text.")
            draft_result = {"original": resume_text, "enhanced": resume_text}
        
        # Step 4: Precision optimization
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
        
        # Count positive vs. negative issues
        positive_issues = [i for i in lint_result.get("issues", []) if i.get("severity") == "positive"]
        negative_issues = [i for i in lint_result.get("issues", []) if i.get("severity") != "positive"]
        
        # If there are more positive than negative issues, consider the resume strong
        is_strong_resume = len(positive_issues) > len(negative_issues)
        
        # If the resume is already strong but not fully optimized, make only minimal changes
        if is_strong_resume and lint_result.get("score", 0) >= 85:
            # Use a more conservative approach
            return {
                "original": resume_text,
                "draft": draft_result["enhanced"],
                "optimized": optimized_text,
                "lint_results": lint_result,
                "score": lint_result.get("score", 0),
                "minimal_changes": True,
                "message": "Your resume is already strong. We've suggested only minimal improvements to maintain your personal style."
            }
            
        # Regular case - need optimization
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
        
        # If the resume is already optimized, return a special "validation" suggestion
        # instead of trying to find issues that don't exist
        if lint_result.get("is_already_optimized", False):
            # Return positive validation instead of suggestions
            evidence = lint_result.get("optimization_evidence", {})
            strong_verbs = evidence.get('strong_verbs', [])[:5]  # Get up to 5 strong verbs to highlight
            
            validation_points = []
            if strong_verbs:
                validation_points.append(f"Strong action verbs like {', '.join(strong_verbs)}")
            if evidence.get('bullet_points'):
                validation_points.append("Well-structured bullet points")
            if evidence.get('quantifiable_achievements'):
                validation_points.append("Quantifiable achievements")
            
            return [{
                "type": "validation",
                "severity": "positive",
                "message": "✅ Your resume is already well-optimized! No changes needed.",
                "details": f"Your resume demonstrates best practices including: {'; '.join(validation_points)}.",
                "alternatives": ["Keep your resume as is - it's already strong."]
            }]
        
        suggestions = []
        
        # First add any positive feedback that might exist
        positive_issues = [issue for issue in lint_result["issues"] if issue.get("severity") == "positive"]
        for issue in positive_issues:
            suggestion = {
                "text": issue.get("text", ""),
                "message": issue["message"],
                "severity": "positive",
                "type": issue["type"]
            }
            suggestions.append(suggestion)
            
        # Then add constructive suggestions for improvement
        improvement_issues = [issue for issue in lint_result["issues"] if issue.get("severity") != "positive"]
        
        for issue in improvement_issues:
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
                        # First check if we can safely use T5 model (without causing error)
                        t5_available = True
                        try:
                            # Try to import sentencepiece to check if it's available
                            import sentencepiece
                        except ImportError:
                            t5_available = False
                            logger.warning("SentencePiece library not available. Will use OpenAI for suggestions.")
                        
                        # Only try T5 if sentencepiece is available
                        if t5_available:
                            try:
                                enhanced = enhance_bullet(issue["text"])
                                suggestion["alternatives"] = [enhanced]
                            except Exception as e:
                                # If T5 enhancement fails for any other reason, use OpenAI
                                logger.warning(f"T5 enhancement failed: {str(e)}. Using OpenAI fallback.")
                                t5_available = False
                        
                        # Use OpenAI if T5 is not available or failed
                        if not t5_available:
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
        
        # If we have very few suggestions and the score is high, add reassurance
        if len(improvement_issues) <= 2 and lint_result.get("score", 0) >= 85 and not lint_result.get("is_already_optimized", False):
            suggestions.append({
                "type": "reassurance",
                "severity": "positive",
                "message": "✅ Your resume is already quite strong, with just a few minor improvements suggested above.",
                "alternatives": ["Focus on the few suggestions above to make your already strong resume even better."]
            })
            
        return suggestions

# Create singleton instance
optimizer = None

def get_optimizer(**kwargs) -> ResumeOptimizer:
    """Get or create a ResumeOptimizer instance."""
    global optimizer
    if optimizer is None:
        optimizer = ResumeOptimizer(**kwargs)
    return optimizer 

def enhance_bullet(bullet_text):
    """
    Enhance a bullet point using T5 model.
    
    Args:
        bullet_text (str): The bullet text to enhance
        
    Returns:
        str: Enhanced bullet
    """
    try:
        from transformers import T5ForConditionalGeneration, T5Tokenizer
        
        # Use a simpler tokenizer prefix
        tokenizer = T5Tokenizer.from_pretrained("t5-small")
        model = T5ForConditionalGeneration.from_pretrained("t5-small")
        
        # Normalize input - ensure it doesn't contain special tokens
        bullet_text = bullet_text.strip()
        
        # Simple prefix prompt
        input_text = f"enhance resume bullet: {bullet_text}"
        
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        
        # Generate with stricter constraints to avoid nonsense outputs
        outputs = model.generate(
            input_ids, 
            max_length=100,  # Limit to avoid repetitive outputs
            min_length=10,   # Ensure it's not too short
            length_penalty=1.0,  # Moderate length penalty
            num_beams=4,     # Beam search for better results
            early_stopping=True,
            no_repeat_ngram_size=3  # Avoid repeating 3-grams (prevents OptiOptiOpti...)
        )
        
        enhanced = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Validate the output isn't garbage or repetitive
        if enhanced and len(enhanced) > 10 and "Opti" not in enhanced:
            return enhanced
        else:
            # Use a simple fallback when T5 gives nonsense
            return f"{bullet_text} [Add numbers and specifics here]"
    except Exception as e:
        logger.error(f"Error in T5 enhancement: {str(e)}")
        return f"{bullet_text} [Add numbers and specifics here]" 