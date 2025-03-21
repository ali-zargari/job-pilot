"""
Tests for the resume optimizer module.
"""

import os
import pytest
from dotenv import load_dotenv

# Import from the local package
try:
    from resume_optimizer.optimizer import get_optimizer, ResumeOptimizer
    from resume_optimizer.matcher import get_matcher
except ImportError:
    # For cases where the module isn't properly installed
    # Use relative imports
    from .optimizer import get_optimizer, ResumeOptimizer
    from .matcher import get_matcher

# Load environment variables
load_dotenv()

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

@pytest.fixture
def optimizer():
    """Fixture to provide a ResumeOptimizer instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    return get_optimizer(openai_api_key=api_key)

@pytest.fixture
def matcher():
    """Fixture to provide a ResumeMatcher instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    return get_matcher(openai_api_key=api_key)

def test_optimizer_initialization(optimizer):
    """Test that the optimizer initializes correctly."""
    assert isinstance(optimizer, ResumeOptimizer)
    assert optimizer.gpt_model == "gpt-4"
    assert optimizer.embedding_model == "text-embedding-ada-002"
    assert optimizer.use_embeddings is True

def test_get_suggestions(optimizer):
    """Test getting improvement suggestions."""
    suggestions = optimizer.get_suggestions(EXAMPLE_RESUME)
    
    assert isinstance(suggestions, list)
    assert len(suggestions) > 0
    
    for suggestion in suggestions:
        assert "text" in suggestion
        assert "message" in suggestion
        assert "severity" in suggestion
        assert "type" in suggestion
        assert "alternatives" in suggestion

def test_optimize_resume(optimizer):
    """Test full resume optimization."""
    result = optimizer.optimize_resume(
        resume_text=EXAMPLE_RESUME,
        job_description=EXAMPLE_JOB
    )
    
    assert isinstance(result, dict)
    assert "original" in result
    assert "draft" in result
    assert "optimized" in result
    assert "lint_results" in result
    assert "score" in result
    
    assert result["score"] >= 0
    assert len(result["optimized"]) > 0

def test_resume_matching(matcher):
    """Test resume matching functionality."""
    match_result = matcher.match_resume(
        resume_text=EXAMPLE_RESUME,
        job_description=EXAMPLE_JOB
    )
    
    assert isinstance(match_result, dict)
    assert "overall_match" in match_result
    assert match_result["overall_match"] >= 0.0
    assert match_result["overall_match"] <= 1.0
    
    if match_result["job_match"]:
        assert "score" in match_result["job_match"]
        assert match_result["job_match"]["score"] >= 0.0
        assert match_result["job_match"]["score"] <= 1.0

def test_draft_resume(optimizer):
    """Test resume drafting functionality."""
    draft_result = optimizer.draft_resume(EXAMPLE_RESUME)
    
    assert isinstance(draft_result, dict)
    assert "original" in draft_result
    assert "enhanced" in draft_result
    assert len(draft_result["enhanced"]) > 0
    assert draft_result["original"] == EXAMPLE_RESUME

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not found")
def test_embeddings(optimizer):
    """Test embedding functionality (only if API key is available)."""
    text = "Test embedding generation"
    embedding = optimizer.get_embedding(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) > 0
    assert all(isinstance(x, float) for x in embedding)

def test_error_handling(optimizer):
    """Test error handling for invalid inputs."""
    with pytest.raises(ValueError):
        optimizer.optimize_resume("")
        
    # Testing with empty string for get_suggestions doesn't raise ValueError anymore
    # It should run without errors
    suggestions = optimizer.get_suggestions("")
    assert isinstance(suggestions, list)
    
    # Empty string for draft_resume doesn't raise error as it's handled gracefully
    draft_result = optimizer.draft_resume("")
    assert isinstance(draft_result, dict)
    assert "original" in draft_result
    assert "enhanced" in draft_result 