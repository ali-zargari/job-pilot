"""
Mock ResumeOptimizer class for testing purposes.
This allows tests to run without requiring the full implementation.
"""

class ResumeOptimizer:
    """Mock ResumeOptimizer for testing purposes"""
    
    def __init__(self, openai_api_key=None, local_mode=False, gpt_model="gpt-3.5-turbo", use_embeddings=True, max_tokens=1000):
        self.local_mode = local_mode
        self.gpt_model = gpt_model
        self.use_embeddings = use_embeddings
        self.max_tokens = max_tokens
        self.api_calls_count = 0
        self.api_call_cache = {}
        self.client = None
        
    def optimize_resume(self, resume_text, job_description=None, reference_resumes=None, apply_ai_rewrite=False):
        """Mock implementation for optimize_resume"""
        if not resume_text:
            raise ValueError("Resume text cannot be empty")
            
        # Return a basic result
        return {
            "optimized_text": "Enhanced " + resume_text,
            "score": 85,
            "issues": [],
            "detailed_score": {
                "composite_score": 85,
                "ats_score": 80,
                "recruiter_score": 90
            }
        }
        
    def _contains_metrics(self, text):
        """Check if text contains metrics"""
        import re
        # Look for % signs or numbers with context
        has_percentages = "%" in text
        has_numbers = bool(re.search(r'\b\d+\b', text))
        return has_percentages or has_numbers
        
    def _apply_ai_rewrite(self, original_text, rule_based_text, job_description=None, original_tech_stack=None):
        """Mock implementation of the AI rewrite functionality"""
        # Simply return the rule_based_text with some minor enhancements
        return rule_based_text.replace("Developed", "Engineered").replace("Created", "Built")
        
    def get_embedding(self, text):
        """Mock implementation for get_embedding"""
        return [0.1] * 10 