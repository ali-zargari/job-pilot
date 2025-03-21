"""
Inference module for the fine-tuned T5 model for resume optimization.
This module provides functions to use a pre-trained T5 model to enhance resume bullet points.
"""

import os
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from typing import List, Dict, Union, Optional

# Constants
DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")
DEFAULT_MAX_LENGTH = 100
DEFAULT_NUM_BEAMS = 4
DEFAULT_MODEL_NAME = "t5-small"  # Used if no fine-tuned model is available

class ResumeEnhancer:
    """
    A class to enhance resume bullet points using a fine-tuned T5 model.
    """
    
    def __init__(
        self, 
        model_path: str = DEFAULT_MODEL_PATH,
        model_name: str = DEFAULT_MODEL_NAME,
        device: Optional[str] = None,
        max_length: int = DEFAULT_MAX_LENGTH,
        num_beams: int = DEFAULT_NUM_BEAMS
    ):
        """
        Initialize the ResumeEnhancer.
        
        Args:
            model_path: Path to the fine-tuned model
            model_name: Name of the base model if no fine-tuned model is available
            device: Device to run the model on ('cpu', 'cuda', etc.)
            max_length: Maximum length of generated text
            num_beams: Number of beams for beam search
        """
        self.max_length = max_length
        self.num_beams = num_beams
        
        # Determine device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        # Load tokenizer and model
        try:
            self.tokenizer = T5Tokenizer.from_pretrained(model_path)
            self.model = T5ForConditionalGeneration.from_pretrained(model_path)
            print(f"Loaded fine-tuned model from {model_path}")
        except (OSError, ValueError):
            print(f"Fine-tuned model not found at {model_path}. Using base model {model_name} instead.")
            self.tokenizer = T5Tokenizer.from_pretrained(model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(model_name)
            
        self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode
        
    def enhance_bullet(self, bullet_text: str) -> str:
        """
        Enhance a single resume bullet point.
        
        Args:
            bullet_text: Original bullet point text
            
        Returns:
            Enhanced bullet point text
        """
        # Prepare input
        input_text = f"Optimize resume: {bullet_text}"
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.to(self.device)
        
        # Generate enhanced bullet point
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_length=self.max_length,
                num_beams=self.num_beams,
                early_stopping=True
            )
            
        # Decode and return
        enhanced_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return enhanced_text
        
    def enhance_resume(self, bullet_points: List[str]) -> List[Dict[str, str]]:
        """
        Enhance multiple resume bullet points.
        
        Args:
            bullet_points: List of original bullet point texts
            
        Returns:
            List of dictionaries containing original and enhanced texts
        """
        results = []
        
        for bullet in bullet_points:
            enhanced = self.enhance_bullet(bullet)
            results.append({
                "original": bullet,
                "enhanced": enhanced
            })
            
        return results

# Create singleton instance
enhancer = None

def get_enhancer(
    model_path: str = DEFAULT_MODEL_PATH,
    model_name: str = DEFAULT_MODEL_NAME
) -> ResumeEnhancer:
    """
    Get or create a ResumeEnhancer instance.
    
    Args:
        model_path: Path to the fine-tuned model
        model_name: Name of the base model if no fine-tuned model is available
        
    Returns:
        ResumeEnhancer instance
    """
    global enhancer
    
    if enhancer is None:
        enhancer = ResumeEnhancer(model_path=model_path, model_name=model_name)
        
    return enhancer

def enhance_bullet(bullet_text: str) -> str:
    """
    Enhance a single resume bullet point.
    
    Args:
        bullet_text: Original bullet point text
        
    Returns:
        Enhanced bullet point text
    """
    return get_enhancer().enhance_bullet(bullet_text)

def enhance_resume(bullet_points: List[str]) -> List[Dict[str, str]]:
    """
    Enhance multiple resume bullet points.
    
    Args:
        bullet_points: List of original bullet point texts
        
    Returns:
        List of dictionaries containing original and enhanced texts
    """
    return get_enhancer().enhance_resume(bullet_points)

if __name__ == "__main__":
    # Example usage
    example_bullets = [
        "Responsible for managing a team of developers",
        "Worked on improving system performance",
        "Helped with customer support and troubleshooting"
    ]
    
    enhanced_bullets = enhance_resume(example_bullets)
    
    for item in enhanced_bullets:
        print(f"Original: {item['original']}")
        print(f"Enhanced: {item['enhanced']}")
        print("---")
