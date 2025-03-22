# AI Processing Module Testing

This directory contains comprehensive tests for the ai_processing module, which implements resume optimization, linting, and matching functionality.

## Test Structure

The tests are organized by module:

- `test_ai_processing.py`: Integration tests that test the complete functionality across all submodules
- `test_resume_lint.py`: Tests for the resume linting functionality
- `test_resume_gpt.py`: Tests for the GPT-based text enhancement functionality
- `test_resume_matcher.py`: Tests for resume to job description matching functionality
- `test_resume_optimizer.py`: Tests for the main resume optimization functionality

## Running Tests

You can run the tests using the provided `run_tests.py` script in the root directory:

```bash
# Run all tests
python run_tests.py

# Run tests with verbose output
python run_tests.py -v

# Run tests with coverage report
python run_tests.py -c

# Identify redundant files without removing them
python run_tests.py --dry-run

# Clean up redundant files after running tests
python run_tests.py --clean
```

Alternatively, you can use pytest directly:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run a specific test file
pytest tests/test_resume_lint.py

# Run tests with coverage
pytest --cov=ai_processing
```

## Test Data

The tests use sample resume and job descriptions for testing. These samples are designed to exercise specific features of the resume processing module.

## API Key Required

Some tests require an OpenAI API key for testing AI enhancement functionality. These tests will be skipped if the API key is not available.

To provide an API key, create a `.env` file in the root directory with:

```
OPENAI_API_KEY=your_api_key_here
```

## Phase 1 vs Phase 2 Testing

The tests are organized to test both Phase 1 (rule-based) and Phase 2 (AI-enhanced) functionality:

- **Phase 1 Tests**: Test the rule-based resume optimization that works without API calls
- **Phase 2 Tests**: Test the AI-enhanced functionality that requires an OpenAI API key

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Place tests in the appropriate module-specific test file
2. Use descriptive test names that indicate what's being tested
3. Skip tests that require API keys when not available
4. Use the provided fixtures for common objects
5. Keep test data in the test files rather than external files 