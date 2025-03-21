"""
Training script for fine-tuning a T5 model on resume data.
This script fine-tunes a T5 model to enhance resume bullet points.
"""

import os
import argparse
import logging
import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    Trainer,
    TrainingArguments,
    set_seed
)
from datasets import load_dataset, Dataset as HFDataset
from typing import Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_MODEL_NAME = "t5-small"
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "model")
DEFAULT_MAX_SEQ_LENGTH = 128
DEFAULT_TRAIN_BATCH_SIZE = 8
DEFAULT_EVAL_BATCH_SIZE = 8
DEFAULT_NUM_EPOCHS = 5
DEFAULT_LEARNING_RATE = 5e-5
DEFAULT_WARMUP_STEPS = 100
DEFAULT_WEIGHT_DECAY = 0.01

class ResumeBulletDataset(Dataset):
    """Dataset for fine-tuning T5 on resume bullet points."""
    
    def __init__(
        self, 
        data: Union[pd.DataFrame, List[Dict]],
        tokenizer: T5Tokenizer,
        max_seq_length: int = DEFAULT_MAX_SEQ_LENGTH,
        is_training: bool = True
    ):
        """
        Initialize the dataset.
        
        Args:
            data: DataFrame or list of dictionaries containing 'original' and 'enhanced' bullet points
            tokenizer: T5 tokenizer
            max_seq_length: Maximum sequence length
            is_training: Whether this dataset is for training
        """
        self.data = data
        self.tokenizer = tokenizer
        self.max_seq_length = max_seq_length
        self.is_training = is_training
        
        if isinstance(data, pd.DataFrame):
            self.original_bullets = data["original"].tolist()
            self.enhanced_bullets = data["enhanced"].tolist() if "enhanced" in data.columns else None
        else:
            self.original_bullets = [item["original"] for item in data]
            self.enhanced_bullets = [item["enhanced"] for item in data] if "enhanced" in data[0] else None
            
        if is_training and self.enhanced_bullets is None:
            raise ValueError("Training data must contain 'enhanced' bullet points")
            
    def __len__(self) -> int:
        return len(self.original_bullets)
        
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        original_bullet = self.original_bullets[idx]
        
        # Prefix for T5
        input_text = f"Optimize resume: {original_bullet}"
        
        # Tokenize input
        inputs = self.tokenizer(
            input_text,
            padding="max_length",
            max_length=self.max_seq_length,
            truncation=True,
            return_tensors="pt"
        )
        
        item = {
            "input_ids": inputs["input_ids"].squeeze(),
            "attention_mask": inputs["attention_mask"].squeeze()
        }
        
        # For training, also tokenize the target
        if self.is_training:
            enhanced_bullet = self.enhanced_bullets[idx]
            
            targets = self.tokenizer(
                enhanced_bullet,
                padding="max_length",
                max_length=self.max_seq_length,
                truncation=True,
                return_tensors="pt"
            )
            
            item["labels"] = targets["input_ids"].squeeze()
            
        return item

def load_data_from_csv(
    train_path: str,
    val_path: Optional[str] = None,
    test_path: Optional[str] = None
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Load data from CSV files.
    
    Args:
        train_path: Path to training data CSV
        val_path: Path to validation data CSV (optional)
        test_path: Path to test data CSV (optional)
        
    Returns:
        Tuple of (train_df, val_df, test_df)
    """
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path) if val_path else None
    test_df = pd.read_csv(test_path) if test_path else None
    
    return train_df, val_df, test_df

def train_model(
    train_data: Union[pd.DataFrame, List[Dict]],
    val_data: Optional[Union[pd.DataFrame, List[Dict]]] = None,
    model_name: str = DEFAULT_MODEL_NAME,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    max_seq_length: int = DEFAULT_MAX_SEQ_LENGTH,
    train_batch_size: int = DEFAULT_TRAIN_BATCH_SIZE,
    eval_batch_size: int = DEFAULT_EVAL_BATCH_SIZE,
    num_epochs: int = DEFAULT_NUM_EPOCHS,
    learning_rate: float = DEFAULT_LEARNING_RATE,
    warmup_steps: int = DEFAULT_WARMUP_STEPS,
    weight_decay: float = DEFAULT_WEIGHT_DECAY,
    seed: int = 42
) -> None:
    """
    Train a T5 model on resume bullet points.
    
    Args:
        train_data: Training data (DataFrame or list of dictionaries)
        val_data: Validation data (optional)
        model_name: Base model name
        output_dir: Directory to save the model
        max_seq_length: Maximum sequence length
        train_batch_size: Training batch size
        eval_batch_size: Evaluation batch size
        num_epochs: Number of epochs
        learning_rate: Learning rate
        warmup_steps: Warmup steps
        weight_decay: Weight decay
        seed: Random seed
    """
    # Set seed for reproducibility
    set_seed(seed)
    
    # Load tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    
    # Create datasets
    train_dataset = ResumeBulletDataset(
        train_data,
        tokenizer,
        max_seq_length=max_seq_length,
        is_training=True
    )
    
    val_dataset = None
    if val_data is not None:
        val_dataset = ResumeBulletDataset(
            val_data,
            tokenizer,
            max_seq_length=max_seq_length,
            is_training=True
        )
    
    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        warmup_steps=warmup_steps,
        weight_decay=weight_decay,
        learning_rate=learning_rate,
        logging_dir=os.path.join(output_dir, "logs"),
        logging_steps=100,
        save_strategy="epoch",
        evaluation_strategy="epoch" if val_dataset else "no",
        load_best_model_at_end=True if val_dataset else False,
        report_to="none",
        seed=seed
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )
    
    # Train the model
    logger.info("Starting training...")
    trainer.train()
    
    # Save the final model
    logger.info(f"Saving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    logger.info("Training complete!")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Fine-tune T5 model on resume data")
    
    parser.add_argument(
        "--train_data",
        type=str,
        required=True,
        help="Path to training data CSV"
    )
    
    parser.add_argument(
        "--val_data",
        type=str,
        help="Path to validation data CSV"
    )
    
    parser.add_argument(
        "--model_name",
        type=str,
        default=DEFAULT_MODEL_NAME,
        help="Base model name"
    )
    
    parser.add_argument(
        "--output_dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save the model"
    )
    
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=DEFAULT_MAX_SEQ_LENGTH,
        help="Maximum sequence length"
    )
    
    parser.add_argument(
        "--train_batch_size",
        type=int,
        default=DEFAULT_TRAIN_BATCH_SIZE,
        help="Training batch size"
    )
    
    parser.add_argument(
        "--eval_batch_size",
        type=int,
        default=DEFAULT_EVAL_BATCH_SIZE,
        help="Evaluation batch size"
    )
    
    parser.add_argument(
        "--num_epochs",
        type=int,
        default=DEFAULT_NUM_EPOCHS,
        help="Number of epochs"
    )
    
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=DEFAULT_LEARNING_RATE,
        help="Learning rate"
    )
    
    parser.add_argument(
        "--warmup_steps",
        type=int,
        default=DEFAULT_WARMUP_STEPS,
        help="Warmup steps"
    )
    
    parser.add_argument(
        "--weight_decay",
        type=float,
        default=DEFAULT_WEIGHT_DECAY,
        help="Weight decay"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed"
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    # Load data
    train_df, val_df, _ = load_data_from_csv(
        args.train_data,
        args.val_data
    )
    
    # Train model
    train_model(
        train_data=train_df,
        val_data=val_df,
        model_name=args.model_name,
        output_dir=args.output_dir,
        max_seq_length=args.max_seq_length,
        train_batch_size=args.train_batch_size,
        eval_batch_size=args.eval_batch_size,
        num_epochs=args.num_epochs,
        learning_rate=args.learning_rate,
        warmup_steps=args.warmup_steps,
        weight_decay=args.weight_decay,
        seed=args.seed
    )
