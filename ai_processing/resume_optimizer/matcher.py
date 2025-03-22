"""
Resume matching module using embeddings.
Compares resumes against job descriptions and reference resumes.
"""

import logging
import os
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from sklearn.metrics.pairwise import cosine_similarity

# Replace direct OpenAI imports with our new module
from ai_processing.resume_openai import get_embedding, calculate_similarity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ResumeMatcher:
    """
    Matches resumes with job descriptions and reference resumes.
    Uses embeddings and keyword matching.
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        similarity_threshold: float = 0.7,
        embedding_model: str = "text-embedding-ada-002",
        use_embeddings: bool = True
    ):
        """
        Initialize the resume matcher.
        
        Args:
            openai_api_key: OpenAI API key for embeddings
            similarity_threshold: Threshold for good matching
            embedding_model: Model to use for embeddings
            use_embeddings: Whether to use embedding-based matching (vs keywords only)
        """
        self.openai_api_key = openai_api_key
        self.similarity_threshold = similarity_threshold
        self.embedding_model = embedding_model
        self.use_embeddings = use_embeddings
        
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text using OpenAI's API.
        
        Args:
            text: Text to get embedding for
            
        Returns:
            Embedding vector
        """
        # Use the new module's get_embedding function
        return get_embedding(text, model=self.embedding_model, api_key=self.openai_api_key)
        
    def calculate_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """
        Calculate cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score (0-1)
        """
        # Use the new module's calculate_similarity function
        return calculate_similarity(embedding1, embedding2)
        
    def match_resume(self, resume_text, job_description):
        """
        Match a resume against a job description.
        
        Args:
            resume_text: The resume text
            job_description: The job description
            
        Returns:
            float: Match score between 0-1
        """
        try:
            if self.use_embeddings:
                # Get embeddings
                resume_embedding = self.get_embedding(resume_text)
                job_embedding = self.get_embedding(job_description)
                
                if not resume_embedding or not job_embedding:
                    # Fall back to keyword matching if embeddings fail
                    logger.warning("Embeddings not available, falling back to keyword matching")
                    return self._keyword_match(resume_text, job_description)
                
                # Calculate cosine similarity
                similarity = self.calculate_similarity(resume_embedding, job_embedding)
                
                # Convert to percentage
                match_percent = 0.5 + (similarity * 0.5)  # Scale from -1,1 to 0,1 with midpoint bias
                
                return match_percent  # Return as a float between 0-1
            else:
                # Use keyword matching
                return self._keyword_match(resume_text, job_description)
        except Exception as e:
            logger.error(f"Error matching resume: {str(e)}")
            return 0.5  # Default to middle score on error
    
    def _keyword_match(self, resume_text, job_description):
        """Simple keyword matching fallback"""
        job_keywords = self.extract_keywords(job_description)
        resume_keywords = self.extract_keywords(resume_text)
        
        # Calculate matches
        matches = set(job_keywords) & set(resume_keywords)
        match_percent = len(matches) / max(len(job_keywords), 1)
        
        return match_percent
        
    def find_best_matches(
        self,
        resume_text: str,
        job_descriptions: List[str],
        match_threshold: float = 0.8,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Find the best matching jobs for a resume.
        
        Args:
            resume_text: Resume text to match
            job_descriptions: List of job descriptions to match against
            match_threshold: Minimum match score to consider
            top_k: Number of top matches to return
            
        Returns:
            List of best matching jobs with scores
        """
        # Get resume embedding
        resume_embedding = self.get_embedding(resume_text)
        
        matches = []
        for job in job_descriptions:
            job_embedding = self.get_embedding(job)
            similarity = self.calculate_similarity(resume_embedding, job_embedding)
            
            if similarity >= match_threshold:
                matches.append({
                    "job_description": job,
                    "match_score": similarity
                })
                
        # Sort by match score and get top k
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        return matches[:top_k]

    def extract_keywords(self, text):
        """
        Extract important keywords from text.
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of keywords
        """
        if not text:
            return []
            
        # Remove common stop words
        stop_words = {
            "a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "be", "been", "being",
            "in", "on", "at", "to", "for", "with", "by", "about", "against", "between", "into", "through",
            "during", "before", "after", "above", "below", "from", "up", "down", "of", "off", "over", "under",
            "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any",
            "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own",
            "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "don't", "should",
            "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn", "didn", "doesn", "hadn",
            "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren",
            "won", "wouldn", "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
            "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself",
            "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "this", "that", "these",
            "those", "am", "have", "has", "had", "do", "does", "did", "doing", "would", "should", "could",
            "ought", "i'm", "you're", "he's", "she's", "it's", "we're", "they're", "i've", "you've", "we've",
            "they've", "i'd", "you'd", "he'd", "she'd", "we'd", "they'd", "i'll", "you'll", "he'll", "she'll",
            "we'll", "they'll", "isn't", "aren't", "wasn't", "weren't", "hasn't", "haven't", "hadn't", "doesn't",
            "don't", "didn't", "won't", "wouldn't", "shan't", "shouldn't", "can't", "cannot", "couldn't", "mustn't",
            "let's", "that's", "who's", "what's", "here's", "there's", "when's", "where's", "why's", "how's"
        }
        
        # Normalize text
        text = text.lower()
        text = ''.join([c if c.isalnum() or c.isspace() else ' ' for c in text])
        
        # Split and filter
        words = text.split()
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Extract tech stack
        try:
            from resume_gpt import extract_tech_stack
            tech_stack = extract_tech_stack(text)
            if tech_stack:
                keywords.extend([tech.lower() for tech in tech_stack])
        except ImportError:
            pass
        
        # Remove duplicates but preserve order
        seen = set()
        keywords = [x for x in keywords if not (x in seen or seen.add(x))]
        
        return keywords

# Keep the utility functions
def extract_resume_bullets(resume_text):
    """
    Extract bullet points from a resume
    
    Args:
        resume_text (str): The resume text
    
    Returns:
        list: List of bullet points
    """
    bullets = []
    
    # Split the resume into lines
    lines = resume_text.split('\n')
    
    # Process each line
    for line in lines:
        line = line.strip()
        
        # Check if this line starts with a bullet character
        if line.startswith(('•', '-', '*', '>', '+', '→', '▪', '▫', '◦', '◆', '◇', '○', '◎', '◉')):
            bullets.append(line)
        
        # Check for numbered bullets
        elif len(line) >= 2 and line[0].isdigit() and line[1] in ['.', ')', ']']:
            bullets.append(line)
    
    return bullets

# Create singleton instance
matcher = None

def get_matcher(**kwargs) -> ResumeMatcher:
    """Get or create a ResumeMatcher instance."""
    global matcher
    if matcher is None:
        matcher = ResumeMatcher(**kwargs)
    return matcher 