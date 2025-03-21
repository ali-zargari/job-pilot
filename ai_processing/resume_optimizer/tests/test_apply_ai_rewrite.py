import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)

class TestApplyAIRewrite(unittest.TestCase):
    """Test the _apply_ai_rewrite function we modified"""
    
    def test_prompt_constraints(self):
        """
        Test that the prompt for rewriting resumes includes constraints
        to prevent drastic changes
        """
        # Create a mock version of the original function
        original_text = "John Doe\nDeveloper\n- Created websites"
        rule_based_text = "John Doe\nDeveloper\n- Created responsive websites"
        job_description = "Looking for a frontend developer"
        
        # These are the key phrases that should be in the prompt to prevent drastic changes
        required_constraint_phrases = [
            "Make MINIMAL and SUBTLE improvements",
            "DO NOT invent new experiences",
            "DO NOT add metrics that weren't already present",
            "KEEP exact same job titles",
            "PRESERVE every bullet point's core meaning",
            "ABSOLUTELY AVOID"
        ]
        
        # Mock the client and capture the prompt
        with patch('openai.OpenAI') as mock_openai:
            # Setup the OpenAI client mock
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            # Mock the completion response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock(message=MagicMock(content="Enhanced content"))]
            mock_client.chat.completions.create.return_value = mock_response
            
            # Import the optimizer here to use the patched OpenAI
            from ai_processing.resume_optimizer.optimizer import ResumeOptimizer
            
            # Create an instance of ResumeOptimizer
            optimizer = ResumeOptimizer(openai_api_key="test-key")
            
            # Call the _apply_ai_rewrite method
            optimizer._apply_ai_rewrite(
                original_text=original_text, 
                rule_based_text=rule_based_text,
                job_description=job_description
            )
            
            # Get the prompt from the call arguments
            call_args = mock_client.chat.completions.create.call_args
            prompt = call_args[1]['messages'][1]['content']
            
            # Check that all required constraint phrases are in the prompt
            for phrase in required_constraint_phrases:
                self.assertIn(phrase, prompt, 
                             f"Constraint phrase '{phrase}' not found in prompt")
            
            # Verify temperature is set low for consistency
            self.assertLessEqual(call_args[1]['temperature'], 0.3, 
                               "Temperature should be 0.3 or lower for consistency")
            
            # Verify the system message emphasizes minimal changes
            system_message = call_args[1]['messages'][0]['content']
            self.assertIn("extremely minimal", system_message.lower(),
                         "System message should emphasize extremely minimal changes")

if __name__ == "__main__":
    unittest.main() 