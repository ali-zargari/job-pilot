"""
Comprehensive integration tests for the ai_processing module.
This file tests the integration and functionality of all submodules in the ai_processing package.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Import modules under test
from ai_processing.resume_optimizer import get_optimizer, get_matcher
from ai_processing.resume_lint import analyze_resume, ResumeAnalyzer
from ai_processing.resume_gpt import enhance_resume, enhance_bullet, extract_tech_stack

# Test data
EXAMPLE_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Responsible for developing web applications
• Helped with improving system performance
• Worked on team projects and fixed bugs
• Managed database operations

Project Manager, StartupX (2017-2019)
• Led team of developers
• Responsible for project delivery
• Helped with customer support
"""

EXAMPLE_JOB = """
Senior Software Engineer

We're looking for an experienced Software Engineer with:
- 5+ years of experience in web development
- Strong background in Python, JavaScript, and cloud technologies
- Experience leading development teams
- Track record of improving system performance and scalability
- Strong problem-solving skills

Responsibilities:
- Lead development of web applications
- Optimize system performance
- Manage database operations
- Mentor junior developers
"""

# Fixtures
@pytest.fixture
def api_key():
    """Fixture to provide API key."""
    return os.getenv("OPENAI_API_KEY")

@pytest.fixture
def optimizer(api_key):
    """Fixture to provide a ResumeOptimizer instance."""
    return get_optimizer(openai_api_key=api_key)

@pytest.fixture
def matcher(api_key):
    """Fixture to provide a ResumeMatcher instance."""
    return get_matcher(openai_api_key=api_key)

@pytest.fixture
def analyzer():
    """Fixture to provide a ResumeAnalyzer instance."""
    return ResumeAnalyzer()

# Tests for Phase 1 functionality (rule-based)
class TestPhase1:
    """Tests for Phase 1 functionality (rule-based optimization)."""
    
    def test_lint_analysis(self, analyzer):
        """Test that resume analysis works correctly."""
        results = analyze_resume(EXAMPLE_RESUME)
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        # Verify result structure
        for result in results:
            assert "text" in result
            assert "message" in result
            assert "severity" in result
            assert "type" in result
    
    def test_optimize_local_mode(self):
        """Test resume optimization in local mode (no API calls)."""
        local_optimizer = get_optimizer(local_mode=True)
        result = local_optimizer.optimize_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB
        )
        
        assert isinstance(result, dict)
        assert "original" in result
        assert "optimized" in result
        assert "lint_results" in result
        assert "score" in result
        assert result["score"] >= 0
        
        # Ensure optimized resume is different from original
        assert result["optimized"] != result["original"]

# Tests for Phase 2 functionality (AI-enhanced)
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not found")
class TestPhase2:
    """Tests for Phase 2 functionality (AI-enhanced optimization)."""
    
    def test_ai_enhancement(self, optimizer):
        """Test AI enhancement of resume."""
        result = optimizer.optimize_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB,
            apply_ai_rewrite=True
        )
        
        assert isinstance(result, dict)
        assert "original" in result
        assert "optimized" in result
        
        # The AI enhancement may not always be applied depending on the implementation
        if "optimized_with_ai" in result:
            assert isinstance(result["optimized_with_ai"], bool)
        
        # Check that result has a score
        assert "score" in result or "final_score" in result
    
    def test_matcher_functionality(self, matcher):
        """Test resume matching functionality."""
        match_result = matcher.match_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB
        )
        
        assert isinstance(match_result, dict)
        assert "overall_match" in match_result
        assert 0 <= match_result["overall_match"] <= 1
        
        if "skill_matches" in match_result:
            assert isinstance(match_result["skill_matches"], list)
    
    def test_gpt_enhancement(self):
        """Test GPT enhancement for resume bullets."""
        # This may be a direct function call or API call depending on implementation
        enhanced = enhance_bullet("Responsible for developing web applications")
        
        # Verify the enhancement returns something valid
        assert isinstance(enhanced, str)
        assert len(enhanced) > 0

# Integration tests that exercise the full pipeline
class TestIntegration:
    """Integration tests for the full resume processing pipeline."""
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not found")
    def test_full_pipeline(self, optimizer, matcher):
        """Test the full resume optimization and matching pipeline."""
        # First optimize the resume
        optimize_result = optimizer.optimize_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB,
            apply_ai_rewrite=True
        )
        
        # Then match the optimized resume with the job
        optimized_resume = optimize_result["optimized"]
        match_result = matcher.match_resume(
            resume_text=optimized_resume,
            job_description=EXAMPLE_JOB
        )
        
        # Compare with original resume match
        original_match = matcher.match_resume(
            resume_text=EXAMPLE_RESUME,
            job_description=EXAMPLE_JOB
        )
        
        # Optimized resume should have a better match score
        assert match_result["overall_match"] >= original_match["overall_match"]
    
    def test_error_handling(self, optimizer):
        """Test error handling with invalid inputs."""
        # Test with empty resume
        with pytest.raises(ValueError):
            optimizer.optimize_resume(resume_text="", job_description=EXAMPLE_JOB)
        
        # Test with empty job description
        result = optimizer.optimize_resume(resume_text=EXAMPLE_RESUME, job_description="")
        assert isinstance(result, dict)
        assert "optimized" in result
        
        # The optimizer should still work with just the resume
        assert len(result["optimized"]) > 0 