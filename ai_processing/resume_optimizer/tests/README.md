# Resume Optimizer Tests

This directory contains comprehensive test cases for the Resume Optimizer module, focusing on validating both basic functionality and edge cases.

## Test Organization

The test suite is organized into multiple test files:

1. **test_edge_cases.py**: Tests general edge cases such as empty resumes, extremely long resumes, and special characters.
2. **test_ai_rewrite.py**: Specifically tests the AI rewrite functionality to ensure it behaves as expected.
3. **test_drastic_changes.py**: Tests focused on detecting and preventing excessive changes to resumes.

## Running Tests

To run all tests, use the provided `run_tests.py` script:

```bash
python run_tests.py
```

Or run individual test files:

```bash
python -m unittest ai_processing.resume_optimizer.tests.test_edge_cases
python -m unittest ai_processing.resume_optimizer.tests.test_ai_rewrite
python -m unittest ai_processing.resume_optimizer.tests.test_drastic_changes
```

## Key Edge Cases Tested

The test suite covers the following edge cases:

1. **Empty or minimal resume input**
2. **Extremely long resumes**
3. **Special characters and unusual formatting**
4. **Resumes with no metrics**
5. **Resumes with many existing metrics**
6. **API failure fallback behavior**
7. **Various job description inputs**
8. **Resume formatting preservation**
9. **API call caching behavior**
10. **Local mode operation**

## AI Rewrite Tests

The AI rewrite tests specifically focus on ensuring that:

1. **Metrics are preserved** in the rewritten resume
2. **Fallback occurs when metrics are lost**
3. **Changes are minimal** as instructed in the prompt
4. **Job description alignment** happens without inventing experiences
5. **Correct extraction from code blocks** in AI responses
6. **Error handling works properly**

## Drastic Changes Detection

The drastic changes tests verify that the optimizer can detect and prevent:

1. **Content invention** (adding achievements or experiences that weren't in the original)
2. **Skill invention** (adding skills not mentioned in the original resume)
3. **Excessive wording changes** that alter the resume too dramatically
4. **Excessive job description tailoring** that invents qualifications to match a job

## Adding New Tests

When adding new tests:

1. Create a test method that starts with `test_` in one of the existing test classes
2. Or create a new test file with classes that inherit from `unittest.TestCase`
3. Update `run_tests.py` if needed to include new test files 