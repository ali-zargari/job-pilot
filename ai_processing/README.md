# AI Processing - Resume Optimizer

An AI-powered resume optimization tool that enhances your resume for job applications.

## Features

- **Rule-based Optimization**: Apply grammar fixes, proper capitalization, and strong action verbs
- **AI-powered Optimization**: Enhance your resume with professional wording and structure
- **Job-tailored Optimization**: Customize your resume to match specific job descriptions
- **Side-by-side Comparison**: View all optimization versions together

## Installation

### Option 1: Install from the current directory

```bash
# Navigate to the ai_processing directory
cd ai_processing

# Install in development mode
pip install -e .
```

### Option 2: Install as a Python package

```bash
pip install ai_processing
```

## Usage

### Command Line Interface

```bash
# Using installed command
optimize-resume --resume path/to/resume.txt --job path/to/job_description.txt --method all

# Using Python module (after installation)
python -m ai_processing.resume_optimizer --resume path/to/resume.txt --job path/to/job_description.txt --method all
```

### Available Methods

- `rule-based`: Apply basic grammar and phrasing improvements (offline)
- `ai`: Use AI to enhance and polish the resume (requires OpenAI API key)
- `job-tailored`: Customize resume for a specific job description (requires OpenAI API key)
- `all`: Apply all optimization methods sequentially

### Additional Options

- `--output`: Specify output directory (default: 'optimized_resumes')
- `--compare`: Show side-by-side comparison of all versions

## Requirements

- Python 3.8+
- OpenAI API key (for AI-powered optimizations)

## Environment Setup

Create a `.env` file in the working directory with:

```
OPENAI_API_KEY=your_api_key_here
GPT_MODEL=gpt-4  # Optional, defaults to gpt-3.5-turbo if not specified
```

## Example

```bash
# Optimize a resume using all methods
optimize-resume --resume examples/sample_resume.txt --job examples/sample_job.txt --method all --compare

# Use only rule-based optimization (no API key required)
optimize-resume --resume examples/sample_resume.txt --method rule-based
```

## Output

Results are saved to the specified output directory (default: 'optimized_resumes'):

- `rule_based_resume.txt`: Basic grammar and phrasing improvements
- `ai_optimized_resume.txt`: AI-enhanced version
- `job_tailored_resume.txt`: Version customized for the provided job description
- `comparison.txt`: Side-by-side comparison (if --compare is used)

## Important Notes

- The AI-powered methods require an OpenAI API key
- Always review AI-generated content before using it in job applications
- The optimizer preserves factual information and doesn't invent accomplishments

## License

MIT 