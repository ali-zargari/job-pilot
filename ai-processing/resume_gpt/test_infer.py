"""
Tests for the inference module of the resume_gpt package.
"""

import unittest
import os
from . import infer

class TestResumeEnhancer(unittest.TestCase):
    """Test cases for the ResumeEnhancer class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Use t5-small to avoid loading a large model for testing
        self.enhancer = infer.ResumeEnhancer(model_name="t5-small")
        
        self.test_bullets = [
            "Responsible for managing a team of developers",
            "Worked on improving system performance",
            "Helped with customer support and troubleshooting"
        ]
    
    def test_init(self):
        """Test initialization of the ResumeEnhancer class."""
        self.assertIsNotNone(self.enhancer)
        self.assertIsNotNone(self.enhancer.tokenizer)
        self.assertIsNotNone(self.enhancer.model)
        
    def test_enhance_bullet(self):
        """Test enhancing a single bullet point."""
        bullet = self.test_bullets[0]
        enhanced = self.enhancer.enhance_bullet(bullet)
        
        # Enhanced text should be a string
        self.assertIsInstance(enhanced, str)
        
        # Enhanced text should not be empty
        self.assertTrue(len(enhanced) > 0)
        
    def test_enhance_resume(self):
        """Test enhancing multiple bullet points."""
        enhanced_bullets = self.enhancer.enhance_resume(self.test_bullets)
        
        # Should return a list of dictionaries
        self.assertIsInstance(enhanced_bullets, list)
        self.assertEqual(len(enhanced_bullets), len(self.test_bullets))
        
        for i, item in enumerate(enhanced_bullets):
            # Each item should have 'original' and 'enhanced' keys
            self.assertIn('original', item)
            self.assertIn('enhanced', item)
            
            # Original text should match input
            self.assertEqual(item['original'], self.test_bullets[i])
            
            # Enhanced text should be a string
            self.assertIsInstance(item['enhanced'], str)
            
            # Enhanced text should not be empty
            self.assertTrue(len(item['enhanced']) > 0)
            
class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions in the infer module."""
    
    def test_get_enhancer(self):
        """Test the get_enhancer function."""
        # First call should create a new enhancer
        enhancer1 = infer.get_enhancer(model_name="t5-small")
        self.assertIsNotNone(enhancer1)
        
        # Second call should return the same enhancer
        enhancer2 = infer.get_enhancer()
        self.assertIs(enhancer1, enhancer2)
        
    def test_enhance_bullet_function(self):
        """Test the enhance_bullet function."""
        bullet = "Managed a team of 5 developers"
        enhanced = infer.enhance_bullet(bullet)
        
        # Enhanced text should be a string
        self.assertIsInstance(enhanced, str)
        
        # Enhanced text should not be empty
        self.assertTrue(len(enhanced) > 0)
        
    def test_enhance_resume_function(self):
        """Test the enhance_resume function."""
        bullets = [
            "Led a product redesign initiative",
            "Optimized database queries for better performance"
        ]
        
        enhanced_bullets = infer.enhance_resume(bullets)
        
        # Should return a list of dictionaries
        self.assertIsInstance(enhanced_bullets, list)
        self.assertEqual(len(enhanced_bullets), len(bullets))
        
        for i, item in enumerate(enhanced_bullets):
            # Each item should have 'original' and 'enhanced' keys
            self.assertIn('original', item)
            self.assertIn('enhanced', item)
            
            # Original text should match input
            self.assertEqual(item['original'], bullets[i])

if __name__ == '__main__':
    unittest.main() 