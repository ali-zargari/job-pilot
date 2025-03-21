"""Main training script for resume optimization model."""

import argparse
from .config import ModelConfig
from .trainer import ResumeModelTrainer

def main():
    """Main training function."""
    parser = argparse.ArgumentParser(description="Train resume optimization model")
    
    # Model parameters
    parser.add_argument("--model_name", type=str, default="t5-small",
                       help="Base model to use for fine-tuning")
    parser.add_argument("--max_length", type=int, default=512,
                       help="Maximum sequence length")
    parser.add_argument("--batch_size", type=int, default=8,
                       help="Training batch size")
    parser.add_argument("--num_epochs", type=int, default=3,
                       help="Number of training epochs")
    parser.add_argument("--learning_rate", type=float, default=2e-5,
                       help="Learning rate")
    
    # Training parameters
    parser.add_argument("--output_dir", type=str, default="models/resume_optimizer",
                       help="Directory to save model checkpoints")
    parser.add_argument("--use_wandb", action="store_true",
                       help="Whether to use Weights & Biases for logging")
    parser.add_argument("--seed", type=int, default=42,
                       help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    # Create config
    config = ModelConfig(
        model_name=args.model_name,
        max_length=args.max_length,
        batch_size=args.batch_size,
        num_epochs=args.num_epochs,
        learning_rate=args.learning_rate,
        output_dir=args.output_dir,
        seed=args.seed
    )
    
    # Create trainer and train
    trainer = ResumeModelTrainer(config)
    trainer.train(use_wandb=args.use_wandb)
    
    # Test the model on some example bullets
    test_bullets = [
        "Responsible for managing team projects",
        "Helped with customer service operations",
        "Was in charge of marketing campaigns",
        "Worked on software development tasks"
    ]
    
    print("\nTesting model on example bullets:")
    for bullet in test_bullets:
        optimized = trainer.optimize_resume_bullet(bullet)
        print(f"\nOriginal: {bullet}")
        print(f"Optimized: {optimized}")

if __name__ == "__main__":
    main() 