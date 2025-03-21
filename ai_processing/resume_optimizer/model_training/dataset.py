"""Dataset creation for resume optimization model training."""

import random
from typing import List, Tuple, Dict
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import PreTrainedTokenizer
import pandas as pd
import numpy as np
from .config import ModelConfig

class ResumeDatasetCreator:
    """Creates training datasets for resume optimization."""
    
    def __init__(self, config: ModelConfig):
        """Initialize dataset creator with configuration."""
        self.config = config
        self.examples = []
        
    def generate_synthetic_examples(self, num_examples: int = 1000) -> List[Dict[str, str]]:
        """Generate synthetic training examples using improvement patterns."""
        examples = []
        
        # Base resume bullet points that we'll transform
        base_bullets = [
            "Managed a team",
            "Responsible for project delivery",
            "Helped with customer service",
            "Was in charge of sales",
            "Assisted in marketing campaigns",
            "Worked on software development",
            "Was responsible for training",
            "Supported business operations",
        ]
        
        for _ in range(num_examples):
            # Randomly select a base bullet
            bullet = random.choice(base_bullets)
            
            # Randomly select an improvement pattern
            pattern_type = random.choice(list(self.config.improvement_patterns.keys()))
            patterns = self.config.improvement_patterns[pattern_type]
            
            # Apply the pattern
            if pattern_type == "add_metrics":
                # Generate random metrics
                size = random.randint(3, 50)
                metric = random.randint(10, 200)
                timeframe = random.choice(["6 months", "1 year", "2 years"])
                amount = random.randint(10, 500)
                
                for before, after in patterns:
                    if before in bullet.lower():
                        improved = after.format(
                            size=size,
                            metric=metric,
                            timeframe=timeframe,
                            amount=amount
                        )
                        examples.append({
                            "input": f"Optimize resume: {bullet}",
                            "output": improved
                        })
                        break
            else:
                # Apply direct replacement patterns
                for before, after in patterns:
                    if before in bullet.lower():
                        examples.append({
                            "input": f"Optimize resume: {bullet}",
                            "output": bullet.replace(before, after)
                        })
                        break
        
        return examples
    
    def create_dataset(self, tokenizer: PreTrainedTokenizer) -> Tuple[Dataset, Dataset, Dataset]:
        """Create train, validation and test datasets."""
        # Generate examples
        examples = self.generate_synthetic_examples(self.config.max_examples)
        
        # Convert to DataFrame for easier splitting
        df = pd.DataFrame(examples)
        
        # Split into train, val, test
        train_size = int(len(df) * self.config.train_split)
        val_size = int(len(df) * self.config.val_split)
        
        train_df = df[:train_size]
        val_df = df[train_size:train_size + val_size]
        test_df = df[train_size + val_size:]
        
        # Create datasets
        train_dataset = ResumeDataset(train_df, tokenizer, self.config)
        val_dataset = ResumeDataset(val_df, tokenizer, self.config)
        test_dataset = ResumeDataset(test_df, tokenizer, self.config)
        
        return train_dataset, val_dataset, test_dataset

class ResumeDataset(Dataset):
    """PyTorch dataset for resume optimization."""
    
    def __init__(self, 
                 data: pd.DataFrame, 
                 tokenizer: PreTrainedTokenizer,
                 config: ModelConfig):
        """Initialize dataset."""
        self.data = data
        self.tokenizer = tokenizer
        self.config = config
        
    def __len__(self) -> int:
        """Get dataset size."""
        return len(self.data)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        """Get dataset item."""
        item = self.data.iloc[idx]
        
        # Tokenize input and output
        input_encoding = self.tokenizer(
            item["input"],
            max_length=self.config.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        output_encoding = self.tokenizer(
            item["output"],
            max_length=self.config.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            "input_ids": input_encoding["input_ids"].squeeze(),
            "attention_mask": input_encoding["attention_mask"].squeeze(),
            "labels": output_encoding["input_ids"].squeeze(),
        } 