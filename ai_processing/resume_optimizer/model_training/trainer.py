"""Model trainer for resume optimization."""

import os
from typing import Tuple, Dict, Any
import torch
from torch.utils.data import DataLoader
from transformers import (
    T5ForConditionalGeneration,
    T5Tokenizer,
    AdamW,
    get_linear_schedule_with_warmup
)
from tqdm.auto import tqdm
import wandb
from .config import ModelConfig
from .dataset import ResumeDatasetCreator, ResumeDataset

class ResumeModelTrainer:
    """Trainer for the resume optimization model."""
    
    def __init__(self, config: ModelConfig):
        """Initialize trainer with configuration."""
        self.config = config
        self.device = config.device
        
        # Initialize model and tokenizer
        self.tokenizer = T5Tokenizer.from_pretrained(config.model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(config.model_name)
        self.model.to(self.device)
        
        # Initialize dataset creator
        self.dataset_creator = ResumeDatasetCreator(config)
        
    def create_dataloaders(self) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """Create train, validation and test dataloaders."""
        # Create datasets
        train_dataset, val_dataset, test_dataset = self.dataset_creator.create_dataset(
            self.tokenizer
        )
        
        # Create dataloaders
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.config.batch_size,
            shuffle=True
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.config.batch_size,
            shuffle=False
        )
        
        test_loader = DataLoader(
            test_dataset,
            batch_size=self.config.batch_size,
            shuffle=False
        )
        
        return train_loader, val_loader, test_loader
    
    def train(self, use_wandb: bool = True) -> None:
        """Train the model."""
        if use_wandb:
            wandb.init(project="resume-optimizer", config=self.config.__dict__)
        
        # Create dataloaders
        train_loader, val_loader, _ = self.create_dataloaders()
        
        # Setup optimizer and scheduler
        optimizer = AdamW(
            self.model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay
        )
        
        num_training_steps = len(train_loader) * self.config.num_epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=self.config.warmup_steps,
            num_training_steps=num_training_steps
        )
        
        # Training loop
        best_val_loss = float('inf')
        for epoch in range(self.config.num_epochs):
            print(f"\nEpoch {epoch + 1}/{self.config.num_epochs}")
            
            # Training
            self.model.train()
            train_loss = 0
            train_pbar = tqdm(train_loader, desc="Training")
            
            for batch in train_pbar:
                # Move batch to device
                batch = {k: v.to(self.device) for k, v in batch.items()}
                
                # Forward pass
                outputs = self.model(**batch)
                loss = outputs.loss
                
                # Backward pass
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                
                # Update progress bar
                train_loss += loss.item()
                train_pbar.set_postfix({"loss": loss.item()})
                
                if use_wandb:
                    wandb.log({"train_loss": loss.item()})
            
            avg_train_loss = train_loss / len(train_loader)
            
            # Validation
            val_loss = self.evaluate(val_loader)
            
            print(f"Average train loss: {avg_train_loss:.4f}")
            print(f"Average validation loss: {val_loss:.4f}")
            
            if use_wandb:
                wandb.log({
                    "epoch": epoch,
                    "avg_train_loss": avg_train_loss,
                    "avg_val_loss": val_loss
                })
            
            # Save best model
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_model("best_model")
        
        # Save final model
        self.save_model("final_model")
    
    @torch.no_grad()
    def evaluate(self, dataloader: DataLoader) -> float:
        """Evaluate the model on a dataloader."""
        self.model.eval()
        total_loss = 0
        
        for batch in tqdm(dataloader, desc="Evaluating"):
            batch = {k: v.to(self.device) for k, v in batch.items()}
            outputs = self.model(**batch)
            total_loss += outputs.loss.item()
        
        return total_loss / len(dataloader)
    
    def save_model(self, name: str) -> None:
        """Save model and tokenizer."""
        save_path = os.path.join(self.config.output_dir, name)
        os.makedirs(save_path, exist_ok=True)
        
        self.model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)
    
    @torch.no_grad()
    def optimize_resume_bullet(self, bullet: str) -> str:
        """Optimize a single resume bullet point."""
        self.model.eval()
        
        # Prepare input
        inputs = self.tokenizer(
            f"Optimize resume: {bullet}",
            return_tensors="pt",
            max_length=self.config.max_length,
            padding="max_length",
            truncation=True
        ).to(self.device)
        
        # Generate output
        outputs = self.model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=self.config.max_length,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )
        
        # Decode output
        optimized = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return optimized 