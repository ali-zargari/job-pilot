"""
Tests for the resume_lint module.
This file tests the rule-based linting functionality for resumes.
"""

import pytest
from ai_processing.resume_lint import (
    analyze_resume, 
    ResumeAnalyzer,
    check_passive_voice,
    check_weak_phrases,
    check_missing_numbers,
    check_sentence_length,
    check_ats_friendly,
    WEAK_PHRASES
)
from ai_processing.resume_lint.preprocess import extract_bullet_points, preprocess_text

# Test resume samples with specific issues to test against
WEAK_VERBS_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Was responsible for developing web applications
• Helped with improving system performance
• Assisted with team projects and fixed bugs
• Was in charge of database operations
"""

QUANTIFICATION_ISSUES = """
WORK EXPERIENCE

Project Manager, StartupX (2017-2019)
• Led team of developers
• Delivered projects
• Improved customer satisfaction
• Reduced development time
"""

BULLETS_FORMAT_ISSUES = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
- Developed web applications 
- Improved system performance
- Fixed bugs in the codebase
- Managed database operations

Project Manager, StartupX (2017-2019)
* Led team of developers
* Delivered projects on time
* Supported customers
"""

PASSIVE_VOICE_ISSUES = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Web applications were developed by me
• System performance was improved
• Bugs were fixed in the codebase
• Database operations were managed efficiently
"""

@pytest.fixture
def analyzer():
    """Fixture to provide a ResumeAnalyzer instance."""
    return ResumeAnalyzer()

class TestResumeAnalyzer:
    """Tests for the resume analyzer functionality."""
    
    def test_weak_verbs_detection(self):
        """Test detection of weak verbs in resume bullets."""
        lint_results = analyze_resume(WEAK_VERBS_RESUME)
        
        # Filter for weak verb issues
        weak_verb_issues = [r for r in lint_results if r.get("type") == "weak_verb"]
        
        # Should find at least 3 weak verb issues in the test resume
        assert len(weak_verb_issues) >= 3
        
        # Check specific phrases
        weak_phrases = [r.get("text", "").lower() for r in weak_verb_issues]
        assert any("was responsible" in phrase for phrase in weak_phrases)
        assert any("helped with" in phrase for phrase in weak_phrases)
        assert any("assisted with" in phrase for phrase in weak_phrases)
    
    def test_quantification_detection(self):
        """Test detection of non-quantified achievements."""
        lint_results = analyze_resume(QUANTIFICATION_ISSUES)
        
        # Filter for quantification issues
        quant_issues = [r for r in lint_results if r.get("type") == "no_metrics"]
        
        # Should find quantification issues in the test resume
        assert len(quant_issues) > 0
        
        # Check that correct bullets are flagged
        flagged_texts = [r.get("text", "") for r in quant_issues]
        assert any("Delivered projects" in text for text in flagged_texts)
        assert any("Improved customer satisfaction" in text for text in flagged_texts)
    
    def test_passive_voice_detection(self):
        """Test detection of passive voice in resume bullets."""
        lint_results = analyze_resume(PASSIVE_VOICE_ISSUES)
        
        # Filter for passive voice issues
        passive_issues = [r for r in lint_results if r.get("type") == "passive_voice"]
        
        # Should find passive voice issues in the test resume
        assert len(passive_issues) > 0
        
        # Check that correct bullets are flagged
        flagged_texts = [r.get("text", "") for r in passive_issues]
        assert any("were developed" in text for text in flagged_texts)
        assert any("was improved" in text for text in flagged_texts)
        assert any("were fixed" in text for text in flagged_texts)
    
    def test_preprocess_functions(self):
        """Test resume preprocessing functions."""
        # Test extract_bullet_points
        bullet_points = extract_bullet_points(WEAK_VERBS_RESUME)
        assert len(bullet_points) >= 4
        
        # Test preprocess_text
        preprocessed = preprocess_text(BULLETS_FORMAT_ISSUES)
        assert isinstance(preprocessed, str)
        assert len(preprocessed) > 0
    
    def test_standalone_rule_functions(self):
        """Test the individual rule check functions."""
        # Extract bullet points for testing
        bullets = extract_bullet_points(WEAK_VERBS_RESUME)
        passive_bullets = extract_bullet_points(PASSIVE_VOICE_ISSUES)
        
        # Test weak phrases check
        weak_results = check_weak_phrases("\n".join(bullets))
        assert isinstance(weak_results, list)
        assert len(weak_results) > 0
        
        # Test passive voice check
        passive_results = check_passive_voice("\n".join(passive_bullets))
        assert isinstance(passive_results, list)
        assert len(passive_results) > 0
        
        # Test missing numbers check
        metrics_results = check_missing_numbers("\n".join(bullets))
        assert isinstance(metrics_results, list)
        
        # Test sentence length check
        length_results = check_sentence_length("\n".join(bullets))
        assert isinstance(length_results, list)
        
        # Test ATS-friendly check
        ats_results = check_ats_friendly(BULLETS_FORMAT_ISSUES)
        assert isinstance(ats_results, list)
    
    def test_analyzer_class(self, analyzer):
        """Test the ResumeAnalyzer class methods."""
        # Test analyze method
        analysis = analyzer.analyze(WEAK_VERBS_RESUME)
        assert isinstance(analysis, list)
        assert len(analysis) > 0
        
        # Check result structure
        for result in analysis:
            assert isinstance(result, dict)
            assert "text" in result
            assert "message" in result
            assert "severity" in result
            assert "type" in result
            assert "alternatives" in result
            
    def test_weak_phrases_dictionary(self):
        """Test that the weak phrases dictionary is properly defined."""
        assert isinstance(WEAK_PHRASES, dict)
        assert len(WEAK_PHRASES) > 0
        
        # Check structure
        for phrase, alternatives in WEAK_PHRASES.items():
            assert isinstance(phrase, str)
            assert isinstance(alternatives, list)
            assert len(alternatives) > 0 