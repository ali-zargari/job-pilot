"""
Tests for resume matching functionality.
This file tests the ability to match resumes to job descriptions.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Import from the module under test
from ai_processing.resume_optimizer import get_matcher
from ai_processing.resume_optimizer.matcher import ResumeMatcher

# Test data
TECH_RESUME = """
WORK EXPERIENCE

Senior Software Engineer, TechCorp (2019-2022)
• Developed scalable web applications using React and Node.js
• Improved system performance by 40% through code optimization
• Led team of 5 developers on critical projects
• Implemented CI/CD pipelines using Jenkins and Docker

Full Stack Developer, WebSolutions (2016-2019)
• Built RESTful APIs using Python and Flask
• Developed front-end interfaces with Angular
• Managed PostgreSQL database with over 10M records
• Reduced page load time by 60% through caching
"""

TECH_JOB = """
Lead Developer

Requirements:
- 5+ years of experience in web development
- Strong skills in React, Node.js, and cloud services
- Experience leading development teams
- Knowledge of CI/CD practices
- Database optimization expertise

Responsibilities:
- Lead a team of developers
- Design and implement scalable applications
- Optimize system performance
- Mentor junior developers
"""

NON_MATCHING_RESUME = """
WORK EXPERIENCE

Marketing Manager, BrandX (2018-2022)
• Developed marketing campaigns that increased sales by 25%
• Managed a team of 3 marketing specialists
• Created content for social media platforms
• Analyzed market trends and competitor strategies

Social Media Coordinator, MediaCorp (2016-2018)
• Managed company social media accounts
• Created engaging content for various platforms
• Increased follower count by 45% in 12 months
• Collaborated with design team on visual assets
"""

@pytest.fixture
def api_key():
    """Fixture to provide API key."""
    return os.getenv("OPENAI_API_KEY")

@pytest.fixture
def matcher(api_key):
    """Fixture to provide a ResumeMatcher instance."""
    return get_matcher(openai_api_key=api_key)

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not found")
class TestResumeMatcher:
    """Tests for the resume matcher functionality."""
    
    def test_initialization(self, matcher):
        """Test that the matcher initializes correctly."""
        assert isinstance(matcher, ResumeMatcher)
        assert matcher.model is not None
        
    def test_matching_score(self, matcher):
        """Test resume matching score calculation."""
        match_result = matcher.match_resume(
            resume_text=TECH_RESUME,
            job_description=TECH_JOB
        )
        
        assert isinstance(match_result, dict)
        assert "overall_match" in match_result
        assert 0 <= match_result["overall_match"] <= 1
        
        # For a good match, score should be relatively high
        assert match_result["overall_match"] >= 0.5
        
    def test_non_matching_score(self, matcher):
        """Test score for non-matching resume and job."""
        match_result = matcher.match_resume(
            resume_text=NON_MATCHING_RESUME,
            job_description=TECH_JOB
        )
        
        assert isinstance(match_result, dict)
        assert "overall_match" in match_result
        
        # For a poor match, score should be relatively low
        assert match_result["overall_match"] < 0.5
        
    def test_skill_matching(self, matcher):
        """Test skill matching functionality."""
        match_result = matcher.match_resume(
            resume_text=TECH_RESUME,
            job_description=TECH_JOB
        )
        
        if "skill_matches" in match_result:
            skill_matches = match_result["skill_matches"]
            assert isinstance(skill_matches, list)
            
            # Check that key skills are identified
            all_skills = " ".join([skill.get("skill", "") for skill in skill_matches]).lower()
            assert "react" in all_skills or "node.js" in all_skills
        
    def test_comparison(self, matcher):
        """Test comparing two resumes against the same job."""
        match1 = matcher.match_resume(TECH_RESUME, TECH_JOB)
        match2 = matcher.match_resume(NON_MATCHING_RESUME, TECH_JOB)
        
        # Tech resume should match tech job better than marketing resume
        assert match1["overall_match"] > match2["overall_match"]
        
    def test_embedding_generation(self, matcher):
        """Test embedding generation functionality."""
        if hasattr(matcher, "get_embedding"):
            embedding = matcher.get_embedding(TECH_JOB)
            
            assert isinstance(embedding, list)
            assert len(embedding) > 0
            assert all(isinstance(x, float) for x in embedding)
            
    def test_error_handling(self, matcher):
        """Test error handling for invalid inputs."""
        # Test with empty inputs
        with pytest.raises(ValueError):
            matcher.match_resume("", TECH_JOB)
            
        with pytest.raises(ValueError):
            matcher.match_resume(TECH_RESUME, "")
            
    def test_result_structure(self, matcher):
        """Test structure of match results."""
        match_result = matcher.match_resume(
            resume_text=TECH_RESUME,
            job_description=TECH_JOB
        )
        
        # Check structure of result
        assert isinstance(match_result, dict)
        assert "overall_match" in match_result
        
        if "job_match" in match_result:
            assert isinstance(match_result["job_match"], dict)
            assert "score" in match_result["job_match"]
            
        if "skill_matches" in match_result:
            assert isinstance(match_result["skill_matches"], list)
            
            for skill in match_result["skill_matches"]:
                assert isinstance(skill, dict)
                assert "skill" in skill
                assert "found" in skill 