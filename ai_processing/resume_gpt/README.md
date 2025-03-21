# ResumeGPT

A machine learning module for optimizing resume bullet points. This module fine-tunes T5 models to transform resume bullet points into more impactful, achievement-focused statements.

## Features

- **Text Optimization**: Transform generic resume bullet points into stronger, more impactful statements
- **Pre-trained Models**: Uses T5 transformer models fine-tuned on resume data 
- **API Integration**: Ready-to-use FastAPI endpoints for easy integration
- **Batch Processing**: Process multiple resume points at once

## Installation

```bash
# From the resume_gpt directory
pip install -r requirements.txt
```

## Usage

### Using the Module Directly

```python
from resume_gpt import enhance_bullet, enhance_resume

# Enhance a single bullet point
enhanced = enhance_bullet(
    "Responsible for managing a team of developers"
)
print(enhanced)
# Output: "Led and mentored a team of developers, resulting in 30% improved productivity"

# Enhance multiple bullet points
bullets = [
    "Worked on improving system performance",
    "Helped with customer support and troubleshooting"
]
enhanced_bullets = enhance_resume(bullets)
print(enhanced_bullets)
# Output: [
#   {
#     "original": "Worked on improving system performance",
#     "enhanced": "Improved system performance by 40% through database optimization and code refactoring"
#   },
#   {
#     "original": "Helped with customer support and troubleshooting",
#     "enhanced": "Resolved complex customer issues with 98% satisfaction rate, reducing escalations by 25%"
#   }
# ]
```

### Running the API

```bash
# From the resume_gpt directory
python -m uvicorn api:app --host 0.0.0.0 --port 8001
```

The API will be available at http://localhost:8001 with Swagger documentation at http://localhost:8001/docs.

## Fine-tuning Your Own Model

To fine-tune the model on your own data:

1. Prepare a CSV file with columns `original` and `enhanced` containing original bullet points and their improved versions.

2. Run the training script:

```bash
python train.py --train_data your_training_data.csv --val_data your_validation_data.csv
```

By default, the model will be saved to the `model` directory.

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /enhance`: Enhance multiple bullet points
- `POST /enhance/bullet`: Enhance a single bullet point

## Testing

Run unit tests with:

```bash
python -m unittest discover
```

## Requirements

- Python 3.7+
- PyTorch 1.9+
- Transformers 4.15+
- FastAPI 0.68+

## License

MIT 