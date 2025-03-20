# Resume Optimizer

A two-tier AI system for optimizing resumes, combining fast GPT-4 drafting with precision fine-tuning and embedding-based matching.

## Features

- **Two-Tier AI Processing**:
  - Fast initial drafts using GPT-4
  - Precision optimization with fine-tuned models
  - ATS compliance checking
  - Human-like quality improvements

- **Resume Matching**:
  - Embedding-based comparison with job descriptions
  - Matching against successful reference resumes
  - Keyword analysis and suggestions
  - Smart job targeting

- **Interactive Suggestions**:
  - Inline improvement suggestions
  - Accept/reject/modify options
  - Explanation for each suggestion
  - Alternative phrasings

## Installation

```bash
# From the resume_optimizer directory
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

## Configuration

Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Using the Module Directly

```python
from resume_optimizer import get_optimizer

# Initialize optimizer
optimizer = get_optimizer(openai_api_key="your_api_key")

# Optimize a resume
result = optimizer.optimize_resume(
    resume_text="Your resume text here",
    job_description="Target job description",
    reference_resumes=["Example successful resume 1", "Example 2"]
)

print(f"Resume Score: {result['score']}")
print(f"Optimized Text: {result['optimized']}")

# Get inline suggestions
suggestions = optimizer.get_suggestions(
    resume_text="Your resume text here",
    job_description="Target job description"
)

for suggestion in suggestions:
    print(f"Issue: {suggestion['message']}")
    print(f"Alternatives: {suggestion['alternatives']}")
```

### Running the API

```bash
# From the resume_optimizer directory
python -m uvicorn api:app --host 0.0.0.0 --port 8002
```

The API will be available at http://localhost:8002 with Swagger documentation at http://localhost:8002/docs.

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /optimize`: Full resume optimization
- `POST /suggestions`: Get improvement suggestions

## Architecture

### Two-Tier Processing

1. **Fast Draft (Tier 1)**:
   - Uses GPT-4 or T5-small for quick initial improvements
   - Focuses on speed (< 30 seconds)
   - Handles basic optimization

2. **Precision Optimization (Tier 2)**:
   - Fine-tuned models for specific improvements
   - ATS compliance checking
   - Keyword optimization
   - Final quality refinements

### Resume Matching

- Uses OpenAI embeddings for semantic comparison
- Matches against job descriptions and reference resumes
- Identifies missing keywords and skills
- Suggests targeted improvements

## Integration

The module integrates with:
- `resume_gpt`: For T5-based enhancements
- `resume_lint`: For ATS compliance checking
- OpenAI API: For GPT-4 and embeddings

## Testing

Run unit tests with:

```bash
python -m unittest discover
```

## Requirements

- Python 3.7+
- OpenAI API key
- Dependencies listed in requirements.txt

## License

MIT 