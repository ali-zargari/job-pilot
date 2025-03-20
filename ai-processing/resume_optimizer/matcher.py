"""
Resume matching module using embeddings.
Compares resumes against job descriptions and reference resumes.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import logging
from sklearn.metrics.pairwise import cosine_similarity
import openai
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class ResumeMatcher:
    """
    Class for matching resumes using embeddings.
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        embedding_model: str = "text-embedding-ada-002",
        similarity_threshold: float = 0.75
    ):
        """
        Initialize the resume matcher.
        
        Args:
            openai_api_key: OpenAI API key for embeddings
            embedding_model: Model to use for embeddings
            similarity_threshold: Threshold for considering matches
        """
        self.openai_api_key = openai_api_key
        self.client = None
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
            
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        
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
        # Reshape for sklearn
        e1 = np.array(embedding1).reshape(1, -1)
        e2 = np.array(embedding2).reshape(1, -1)
        
        return float(cosine_similarity(e1, e2)[0][0])
        
    def match_resume(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        reference_resumes: Optional[List[str]] = None
    ) -> Dict:
        """
        Match a resume against a job description and reference resumes.
        
        Args:
            resume_text: Resume text to match
            job_description: Job description to match against
            reference_resumes: List of successful reference resumes
            
        Returns:
            Dictionary with match results
        """
        # Get resume embedding
        resume_embedding = self.get_embedding(resume_text)
        
        results = {
            "overall_match": 0.0,
            "job_match": None,
            "reference_matches": [],
            "missing_keywords": []
        }
        
        # Match against job description
        if job_description:
            job_embedding = self.get_embedding(job_description)
            job_similarity = self.calculate_similarity(resume_embedding, job_embedding)
            
            results["job_match"] = {
                "score": job_similarity,
                "is_good_match": job_similarity >= self.similarity_threshold
            }
            
            # Extract missing keywords if match is low
            if job_similarity < self.similarity_threshold:
                # TODO: Implement keyword extraction and comparison
                pass
                
        # Match against reference resumes
        if reference_resumes:
            for ref_resume in reference_resumes:
                ref_embedding = self.get_embedding(ref_resume)
                similarity = self.calculate_similarity(resume_embedding, ref_embedding)
                
                results["reference_matches"].append({
                    "score": similarity,
                    "is_good_match": similarity >= self.similarity_threshold
                })
                
        # Calculate overall match score
        scores = []
        if results["job_match"]:
            scores.append(results["job_match"]["score"])
        scores.extend([m["score"] for m in results["reference_matches"]])
        
        if scores:
            results["overall_match"] = sum(scores) / len(scores)
            
        return results
        
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

# Create singleton instance
matcher = None

def get_matcher(**kwargs) -> ResumeMatcher:
    """Get or create a ResumeMatcher instance."""
    global matcher
    if matcher is None:
        matcher = ResumeMatcher(**kwargs)
    return matcher 