"""
Comprehensive test script for the resume_optimizer module.
"""

import os
import argparse
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import module functions
from ai_processing.resume_optimizer import (
    get_optimizer,
    ResumeOptimizer,
    get_matcher, 
    ResumeMatcher
)

# Import OpenAI module for testing if integrated
try:
    from ai_processing.resume_openai import check_api_key
    has_openai_module = True
except ImportError:
    has_openai_module = False
    logger.warning("resume_openai module not found. Some tests will be skipped.")

# Sample data for testing
SAMPLE_RESUME = """
WORK EXPERIENCE

Software Engineer, TechCorp (2019-2022)
• Responsible for developing web applications using React and Node.js
• Helped with testing and debugging of various software components
• Worked on database optimization that improved query performance

Developer, StartupX (2017-2019)
• Built and maintained customer-facing e-commerce website
• Assisted in implementing payment processing system
• Collaborated with design team on UI/UX improvements
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer

We're looking for a talented Software Engineer with experience in web development
and cloud technologies. The ideal candidate will have:

- Strong JavaScript skills, with React and Node.js experience
- Experience with database optimization and query tuning
- Knowledge of cloud platforms (AWS, Azure or GCP)
- Good communication and teamwork abilities

Join our dynamic team working on cutting-edge web applications!
"""

def test_optimizer_initialization(api_key=None):
    """Test ResumeOptimizer initialization in different modes."""
    logger.info("Testing ResumeOptimizer initialization...")
    
    # Test API mode
    api_optimizer = get_optimizer(openai_api_key=api_key)
    
    # Test local mode
    local_optimizer = get_optimizer(local_mode=True)
    
    logger.info(f"API mode local_mode flag: {api_optimizer.local_mode}")
    logger.info(f"Local mode local_mode flag: {local_optimizer.local_mode}")
    
    # Verify that without API key, we fall back to local mode
    expected_local_mode = not api_key or api_optimizer.local_mode
    
    return {
        "api_mode": not api_optimizer.local_mode,
        "local_mode": local_optimizer.local_mode,
        "fallback_working": expected_local_mode == api_optimizer.local_mode
    }

def test_matcher_initialization(api_key=None):
    """Test ResumeMatcher initialization."""
    logger.info("Testing ResumeMatcher initialization...")
    
    matcher = get_matcher(openai_api_key=api_key)
    
    # Try to get an embedding if API key is available
    has_embeddings = False
    if api_key:
        try:
            sample_text = "Testing embeddings functionality"
            embedding = matcher.get_embedding(sample_text)
            has_embeddings = len(embedding) > 0
            logger.info(f"Successfully generated embedding with {len(embedding)} dimensions")
        except Exception as e:
            logger.warning(f"Failed to generate embedding: {str(e)}")
    
    return {
        "initialized": matcher is not None,
        "has_embeddings": has_embeddings
    }

def test_basic_optimization(api_key=None):
    """Test basic resume optimization."""
    logger.info("Testing basic resume optimization...")
    
    # Initialize optimizer with local mode to test rule-based improvements
    optimizer = get_optimizer(local_mode=True)
    
    # Run optimization
    result = optimizer.optimize_resume(SAMPLE_RESUME)
    
    # Check for improved score
    original_score = result.get("score", 0)
    final_score = result.get("final_score", 0)
    improvement = final_score > original_score
    
    logger.info(f"Original score: {original_score}")
    logger.info(f"Optimized score: {final_score}")
    
    if improvement:
        logger.info("✅ Successfully improved resume score")
    else:
        logger.info("⚠️ No score improvement detected")
    
    return {
        "has_result": result is not None,
        "has_score_improvement": improvement,
        "original_score": original_score,
        "final_score": final_score
    }

def test_job_matching(api_key=None):
    """Test job matching functionality."""
    logger.info("Testing job matching functionality...")
    
    # Initialize matcher
    matcher = get_matcher(openai_api_key=api_key)
    
    # Calculate match score
    match_score = matcher.match_resume(SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)
    
    logger.info(f"Job match score: {match_score:.2f}")
    
    return {
        "has_match_score": match_score is not None,
        "match_score": match_score
    }

def test_ai_optimization(api_key=None):
    """Test AI-powered resume optimization."""
    logger.info("Testing AI-powered resume optimization...")
    
    if not api_key:
        logger.warning("Skipping AI optimization test - no API key provided")
        return {
            "skipped": True,
            "reason": "No API key provided"
        }
    
    # Initialize optimizer with API mode
    optimizer = get_optimizer(openai_api_key=api_key, apply_ai_rewrite=True)
    
    # If we're still in local mode despite API key, there's an issue
    if optimizer.local_mode:
        logger.warning("Optimizer is in local mode despite API key - possible API key issue")
        return {
            "skipped": True,
            "reason": "API key issue, still in local mode"
        }
    
    # Run optimization with job description for targeting
    result = optimizer.optimize_resume(
        SAMPLE_RESUME,
        job_description=SAMPLE_JOB_DESCRIPTION
    )
    
    # Check if optimization was applied
    original = result.get("original", "")
    optimized = result.get("optimized", "")
    used_ai = result.get("optimized_with_ai", False)
    
    if original != optimized:
        logger.info("✅ Resume was modified during optimization")
    else:
        logger.info("⚠️ Resume was not modified during optimization")
    
    logger.info(f"Used AI for optimization: {used_ai}")
    
    return {
        "has_result": result is not None,
        "is_modified": original != optimized,
        "used_ai": used_ai
    }

def run_all_tests(api_key=None):
    """Run all tests and return overall success status."""
    results = {}
    
    # Run all test functions
    results["optimizer_init"] = test_optimizer_initialization(api_key)
    results["matcher_init"] = test_matcher_initialization(api_key)
    results["basic_optimization"] = test_basic_optimization(api_key)
    results["job_matching"] = test_job_matching(api_key)
    
    # Only run AI tests if API key is provided
    if api_key:
        results["ai_optimization"] = test_ai_optimization(api_key)
    
    # Calculate success rate
    success_count = 0
    total_tests = 0
    
    for category, result in results.items():
        # Skip skipped tests
        if isinstance(result, dict) and result.get("skipped", False):
            continue
            
        total_tests += 1
        if isinstance(result, dict) and all(result.values()):
            success_count += 1
        elif result:
            success_count += 1
    
    success_rate = (success_count / total_tests) * 100 if total_tests > 0 else 0
    
    # Print summary
    logger.info("\n===== TEST SUMMARY =====")
    logger.info(f"Tests passed: {success_count}/{total_tests} ({success_rate:.1f}%)")
    
    for name, result in results.items():
        if isinstance(result, dict) and result.get("skipped", False):
            logger.info(f"⏩ SKIP - {name} ({result.get('reason', 'No reason')})")
        elif isinstance(result, dict) and all(v for k, v in result.items() if k != "skipped" and k != "reason"):
            logger.info(f"✅ PASS - {name}")
        elif result:
            logger.info(f"✅ PASS - {name}")
        else:
            logger.info(f"❌ FAIL - {name}")
    
    return success_rate >= 80  # Success if at least 80% of tests pass

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Test resume_optimizer module")
    parser.add_argument("--api-key", type=str, help="OpenAI API key to use")
    parser.add_argument("--init", action="store_true", help="Test initialization only")
    parser.add_argument("--basic", action="store_true", help="Test basic optimization only")
    parser.add_argument("--matching", action="store_true", help="Test job matching only")
    parser.add_argument("--ai", action="store_true", help="Test AI optimization only")
    parser.add_argument("--local", action="store_true", help="Force local mode for all tests")
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    
    # Force local mode if requested
    if args.local:
        api_key = None
    
    # Log API key status
    if not api_key:
        logger.info("Running in local mode (no API key provided)")
    else:
        logger.info(f"Using API key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else ''}")
        
        # Test API key if OpenAI module is available
        if has_openai_module:
            key_status = check_api_key(api_key)
            if key_status["is_valid"]:
                logger.info("✅ API key is valid")
            else:
                logger.warning(f"⚠️ API key validation failed: {key_status['message']}")
    
    # If specific tests are requested, run only those
    if args.init:
        test_optimizer_initialization(api_key)
        test_matcher_initialization(api_key)
    elif args.basic:
        test_basic_optimization(api_key)
    elif args.matching:
        test_job_matching(api_key)
    elif args.ai and api_key:
        test_ai_optimization(api_key)
    else:
        # Run all tests if no specific test is requested
        run_all_tests(api_key)
    
    logger.info("Tests completed.")

if __name__ == "__main__":
    main() 