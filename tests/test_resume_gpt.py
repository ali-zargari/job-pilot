"""
Tests for the resume_gpt module.
This file tests the GPT-based resume enhancement functionality.
"""

import os
import pytest
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

# Import from the module under test
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

@pytest.fixture
def api_key():
    """Fixture to provide API key."""
    return os.getenv("OPENAI_API_KEY")

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not found")
class TestResumeGPT:
    """Tests for the resume GPT module."""
    
    def test_resume_enhancement(self, api_key):
        """Test full resume enhancement."""
        # This function might fail if the API isn't available
        if not api_key:
            pytest.skip("API key not available")
            
        enhanced_resume = enhance_resume(EXAMPLE_RESUME)
        
        assert isinstance(enhanced_resume, str)
        assert len(enhanced_resume) > 0
        assert enhanced_resume != EXAMPLE_RESUME
        
    def test_bullet_enhancement(self, api_key):
        """Test enhancement of individual bullets."""
        if not api_key:
            pytest.skip("API key not available")
            
        original_bullet = "Responsible for developing web applications"
        enhanced_bullet = enhance_bullet(original_bullet)
        
        assert isinstance(enhanced_bullet, str)
        assert len(enhanced_bullet) > 0
        assert enhanced_bullet != original_bullet
        
        # The enhanced bullet should contain stronger language
        assert "Developed" in enhanced_bullet or "Created" in enhanced_bullet or "Built" in enhanced_bullet
        
    def test_tech_stack_extraction(self, api_key):
        """Test technology stack extraction from job description."""
        if not api_key:
            pytest.skip("API key not available")
            
        tech_stack = extract_tech_stack(EXAMPLE_JOB)
        
        assert isinstance(tech_stack, list)
        assert len(tech_stack) > 0
        
        # Check that key technologies are extracted
        extracted_techs = " ".join(tech_stack).lower()
        assert "python" in extracted_techs or "javascript" in extracted_techs
        
    def test_empty_input_handling(self, api_key):
        """Test handling of empty inputs."""
        if not api_key:
            pytest.skip("API key not available")
            
        # Should return empty string or raise ValueError
        try:
            result = enhance_bullet("")
            assert result == "" or len(result) == 0
        except ValueError:
            # This is also acceptable behavior
            pass
    
    def test_api_fallback(self, monkeypatch):
        """Test fallback behavior when API is not available."""
        # Simulate API failure by setting API key to None
        monkeypatch.setenv("OPENAI_API_KEY", "")
        
        # The module should have fallbacks for when API is not available
        original_text = "Test bullet point"
        result = enhance_bullet(original_text)
        
        # Fallback should return original text or some variation
        assert isinstance(result, str)
        assert len(result) > 0 