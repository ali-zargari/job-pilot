"""Configuration for model training."""

from dataclasses import dataclass
from typing import Optional, List, Dict
import os

@dataclass
class ModelConfig:
    """Configuration for the resume optimization model."""
    
    # Model parameters
    model_name: str = "t5-small"  # Base model to use
    max_length: int = 512  # Maximum sequence length
    batch_size: int = 8
    num_epochs: int = 3
    learning_rate: float = 2e-5
    warmup_steps: int = 500
    weight_decay: float = 0.01
    
    # Training parameters
    train_split: float = 0.8
    val_split: float = 0.1
    test_split: float = 0.1
    seed: int = 42
    
    # Dataset parameters
    min_examples: int = 1000  # Minimum number of examples needed
    max_examples: int = 10000  # Maximum number of examples to use
    
    # Output parameters
    output_dir: str = "models/resume_optimizer"
    
    # Resume improvement patterns
    improvement_patterns: Dict[str, List[str]] = {
        "weak_to_strong": [
            ("responsible for managing", "Led and directed"),
            ("helped with", "Spearheaded"),
            ("worked on", "Executed"),
            ("assisted in", "Coordinated"),
        ],
        "add_metrics": [
            ("managed team", "Managed team of {size} achieving {metric}% improvement"),
            ("increased sales", "Increased sales by {metric}% over {timeframe}"),
            ("improved efficiency", "Improved efficiency by {metric}%, saving {amount}k annually"),
        ],
        "passive_to_active": [
            ("was promoted", "Earned promotion"),
            ("was responsible", "Led"),
            ("was selected", "Won selection"),
        ]
    }
    
    def __post_init__(self):
        """Create output directory if it doesn't exist."""
        os.makedirs(self.output_dir, exist_ok=True)
        
    @property
    def device(self) -> str:
        """Get the device to use for training."""
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu" 