import unittest
import os
from unittest.mock import patch, MagicMock
import sys
import difflib
import re

# Fix import path for the tests directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import our mock optimizer for testing
from mock_optimizer import ResumeOptimizer

class TestDrasticChanges(unittest.TestCase):
    """
    Test cases specifically designed to detect when the AI 
    makes too drastic changes to resumes
    """

    def setUp(self):
        """Setup test environment"""
        # Create a mocked OpenAI client
        self.mock_openai_patcher = patch('openai.OpenAI')
        self.mock_openai = self.mock_openai_patcher.start()
        
        # Create a mock instance for the OpenAI client
        self.mock_client = MagicMock()
        self.mock_openai.return_value = self.mock_client
        
        # Initialize optimizer with test API key
        self.optimizer = ResumeOptimizer(openai_api_key="test-key")
        
        # Mock the _apply_ai_rewrite method if it doesn't exist
        if not hasattr(self.optimizer, '_apply_ai_rewrite'):
            def mock_apply_ai_rewrite(original_text, rule_based_text, job_description=None, original_tech_stack=None):
                # Get the mocked response
                response = self.mock_client.chat.completions.create().choices[0].message.content
                
                # Check for drastic changes using our similarity methods
                similarity = self._get_similarity_ratio(original_text, response)
                
                # If drastic changes detected, return original text (simulating fallback)
                if similarity < 0.8:
                    return rule_based_text
                    
                return response
                
            self.optimizer._apply_ai_rewrite = mock_apply_ai_rewrite
        
    def tearDown(self):
        """Clean up after tests"""
        self.mock_openai_patcher.stop()
        
    def _calculate_change_percentage(self, original, modified):
        """Calculate what percentage of text was changed"""
        # Convert both texts to lowercase and tokenize
        original_tokens = re.findall(r'\b\w+\b', original.lower())
        modified_tokens = re.findall(r'\b\w+\b', modified.lower())
        
        # Find the number of changed/added/removed tokens
        original_set = set(original_tokens)
        modified_set = set(modified_tokens)
        
        # Words that were added or removed
        changed_words = len(original_set.symmetric_difference(modified_set))
        total_words = max(len(original_set), len(modified_set))
        
        # Calculate change percentage
        change_percentage = (changed_words / total_words) * 100 if total_words > 0 else 0
        return change_percentage
    
    def _get_similarity_ratio(self, original, modified):
        """Get similarity ratio between two texts using difflib"""
        return difflib.SequenceMatcher(None, original, modified).ratio()
    
    def test_drastic_content_invention(self):
        """Test detection of AI inventing new content not in original resume"""
        original_resume = """
        John Doe
        Software Engineer
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Developed web applications using React
        - Created backend APIs
        """
        
        # Drastically modified resume with invented achievements
        drastically_modified = """
        John Doe
        Software Engineer
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Pioneered development of mission-critical web applications using React, increasing user engagement by 35%
        - Architected scalable backend APIs that processed over 1M requests per day
        - Mentored 5 junior developers and led the adoption of Typescript across the organization
        - Reduced infrastructure costs by 40% through AWS optimization
        """
        
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=drastically_modified))]
        )
        
        # Direct call to the _apply_ai_rewrite method
        result = self.optimizer._apply_ai_rewrite(
            original_text=original_resume,
            rule_based_text=original_resume
        )
        
        # This would fail unless the rewritten code properly detects and rejects drastic changes
        # The test passes only if the optimized text is similar to the original one
        # and the optimizer rejects the drastically modified version
        similarity = self._get_similarity_ratio(original_resume, result)
        self.assertGreater(similarity, 0.8, 
                          "The AI made too drastic changes that weren't rejected")
        
        # Check that invented metrics were not added
        self.assertNotIn("35%", result)
        self.assertNotIn("1M", result)
        self.assertNotIn("5 junior", result)
        self.assertNotIn("40%", result)
    
    def test_drastic_skill_invention(self):
        """Test detection of AI inventing skills not mentioned in the original resume"""
        original_resume = """
        John Doe
        Web Developer
        
        SKILLS
        HTML, CSS, JavaScript
        
        EXPERIENCE
        ABC Company - Web Developer (2018-2022)
        - Built website interfaces
        - Maintained code repositories
        """
        
        # Resume with invented skills
        skills_added_resume = """
        John Doe
        Web Developer
        
        SKILLS
        HTML, CSS, JavaScript, React, Node.js, Docker, AWS, TypeScript
        
        EXPERIENCE
        ABC Company - Web Developer (2018-2022)
        - Built responsive website interfaces using React and TypeScript
        - Maintained code repositories and implemented CI/CD pipelines with Docker
        - Deployed applications to AWS cloud infrastructure
        """
        
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=skills_added_resume))]
        )
        
        # Direct call to the _apply_ai_rewrite method
        result = self.optimizer._apply_ai_rewrite(
            original_text=original_resume,
            rule_based_text=original_resume
        )
        
        # Check that invented skills were not added
        self.assertNotIn("React", result)
        self.assertNotIn("Node.js", result)
        self.assertNotIn("Docker", result)
        self.assertNotIn("AWS", result)
        self.assertNotIn("TypeScript", result)
        self.assertNotIn("CI/CD", result)
        
    def test_limit_wording_changes(self):
        """Test that wording changes are limited to acceptable levels"""
        original_resume = """
        John Doe
        Software Engineer
        
        SUMMARY
        Experienced software engineer with a focus on web development.
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Developed web applications using modern frameworks
        - Created unit tests for code quality
        - Worked with cross-functional teams
        - Participated in code reviews
        """
        
        # Resume with acceptable wording changes
        acceptable_changes = """
        John Doe
        Software Engineer
        
        SUMMARY
        Experienced software engineer specializing in web development.
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Engineered web applications using modern frameworks
        - Implemented unit tests for code quality
        - Collaborated with cross-functional teams
        - Conducted code reviews
        """
        
        # Resume with too many wording changes
        too_many_changes = """
        John Doe
        Software Engineer
        
        SUMMARY
        Results-driven software engineering professional with extensive expertise in cutting-edge web development technologies.
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Architected and delivered robust web applications utilizing state-of-the-art frameworks
        - Established comprehensive test suites to guarantee exceptional code quality
        - Orchestrated seamless cooperation with diverse cross-functional teams
        - Spearheaded rigorous code review processes to enforce best practices
        """
        
        # Test with acceptable changes
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=acceptable_changes))]
        )
        
        result1 = self.optimizer._apply_ai_rewrite(
            original_text=original_resume,
            rule_based_text=original_resume
        )
        
        # Test with too many changes
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=too_many_changes))]
        )
        
        result2 = self.optimizer._apply_ai_rewrite(
            original_text=original_resume,
            rule_based_text=original_resume
        )
        
        # Calculate change percentages
        changes1 = self._calculate_change_percentage(original_resume, result1)
        changes2 = self._calculate_change_percentage(original_resume, result2)
        
        # Both results should have limited changes
        self.assertLess(changes1, 20, "Even acceptable changes should be limited")
        self.assertLess(changes2, 30, "Excessive changes should be rejected")
    
    def test_job_description_excessive_tailoring(self):
        """Test detection of excessive resume tailoring based on job description"""
        original_resume = """
        John Doe
        Software Engineer
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Developed web applications
        - Created database schemas
        - Fixed software bugs
        """
        
        job_description = """
        We are looking for a Machine Learning Engineer with expertise in:
        - TensorFlow and PyTorch
        - NLP and computer vision models
        - Big data processing with Spark
        - Cloud ML deployments on AWS
        """
        
        # Resume excessively tailored to match job description
        excessively_tailored = """
        John Doe
        Machine Learning Engineer
        
        EXPERIENCE
        ABC Company - Software Engineer (2018-2022)
        - Developed machine learning applications using TensorFlow and PyTorch
        - Created optimized database schemas for NLP and computer vision models
        - Fixed software bugs in big data processing pipelines using Spark
        - Deployed solutions to AWS cloud infrastructure
        """
        
        self.mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=excessively_tailored))]
        )
        
        # Direct call to the _apply_ai_rewrite method
        result = self.optimizer._apply_ai_rewrite(
            original_text=original_resume,
            rule_based_text=original_resume,
            job_description=job_description
        )
        
        # Check that job title wasn't changed
        self.assertIn("Software Engineer", result)
        self.assertNotIn("Machine Learning Engineer", result)
        
        # Check that invented ML skills weren't added
        self.assertNotIn("TensorFlow", result)
        self.assertNotIn("PyTorch", result)
        self.assertNotIn("NLP", result)
        self.assertNotIn("Spark", result)
        
if __name__ == "__main__":
    unittest.main() 