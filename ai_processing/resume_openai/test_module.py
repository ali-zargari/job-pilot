"""
Comprehensive test script for the resume_openai module.
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
from resume_openai import (
    get_openai_client,
    check_api_key,
    get_embedding,
    calculate_similarity,
    get_document_similarity,
    generate_text,
    enhance_text,
    rewrite_resume
)

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

def test_client_initialization(api_key=None):
    """Test the OpenAI client initialization."""
    logger.info("Testing OpenAI client initialization...")
    
    client = get_openai_client(api_key=api_key)
    status = "available" if client.is_available else "unavailable"
    
    logger.info(f"OpenAI client status: {status}")
    logger.info(f"Default model: {client.default_model}")
    logger.info(f"Embedding model: {client.embedding_model}")
    
    return client.is_available

def test_api_key(api_key=None):
    """Test API key validation."""
    logger.info("Testing API key validation...")
    
    result = check_api_key(api_key)
    
    if result["is_valid"]:
        logger.info("✅ API key is valid and working")
    else:
        logger.warning(f"❌ API key validation failed: {result['message']}")
    
    return result["is_valid"]

def test_embedding(api_key=None):
    """Test embedding generation."""
    logger.info("Testing embedding generation...")
    
    text = "Software engineer with experience in React and Node.js"
    embedding = get_embedding(text, api_key=api_key)
    
    if embedding:
        logger.info(f"✅ Generated embedding with {len(embedding)} dimensions")
    else:
        logger.warning("❌ Failed to generate embedding")
        
    return bool(embedding)

def test_similarity(api_key=None):
    """Test similarity calculation."""
    logger.info("Testing similarity calculation...")
    
    # Test document similarity
    result = get_document_similarity(
        SAMPLE_RESUME,
        SAMPLE_JOB_DESCRIPTION,
        api_key=api_key
    )
    
    if result["has_valid_embeddings"]:
        logger.info(f"✅ Resume-job similarity score: {result['similarity']:.4f}")
    else:
        logger.warning("❌ Failed to calculate document similarity")
    
    return result["has_valid_embeddings"]

def test_text_generation(api_key=None):
    """Test basic text generation."""
    logger.info("Testing text generation...")
    
    prompt = "Suggest three ways to improve a resume for a software engineer position."
    system = "You are a professional resume writer helping job seekers."
    
    generated = generate_text(
        prompt=prompt,
        system_prompt=system,
        max_tokens=150,
        api_key=api_key
    )
    
    if generated:
        logger.info(f"✅ Generated response: {generated[:100]}...")
    else:
        logger.warning("❌ Failed to generate text")
        
    return bool(generated)

def test_text_enhancement(api_key=None):
    """Test text enhancement."""
    logger.info("Testing bullet point enhancement...")
    
    bullet = "Helped develop web applications for multiple clients"
    
    enhanced = enhance_text(
        text=bullet,
        goal="improve with quantifiable achievements",
        api_key=api_key
    )
    
    if enhanced:
        logger.info(f"✅ Original: {bullet}")
        logger.info(f"✅ Enhanced: {enhanced}")
    else:
        logger.warning("❌ Failed to enhance text")
        
    return bullet != enhanced and bool(enhanced)

def test_resume_rewrite(api_key=None):
    """Test resume rewriting."""
    logger.info("Testing resume rewriting...")
    
    result = rewrite_resume(
        resume_text=SAMPLE_RESUME,
        job_description=SAMPLE_JOB_DESCRIPTION,
        skills=["React", "Node.js", "JavaScript", "SQL"],
        api_key=api_key
    )
    
    rewritten = result.get("rewritten_resume", "")
    improvements = result.get("improvements", [])
    
    if rewritten:
        logger.info(f"✅ Resume successfully rewritten")
        logger.info(f"Improvements made: {len(improvements)}")
        logger.info(f"First 100 characters: {rewritten[:100]}...")
    else:
        logger.warning("❌ Failed to rewrite resume")
        
    return bool(rewritten)

def run_all_tests(api_key=None):
    """Run all tests and return overall success status."""
    results = {}
    
    # Run all test functions
    results["client_init"] = test_client_initialization(api_key)
    results["api_key"] = test_api_key(api_key)
    results["embedding"] = test_embedding(api_key)
    results["similarity"] = test_similarity(api_key)
    results["generation"] = test_text_generation(api_key)
    results["enhancement"] = test_text_enhancement(api_key)
    results["rewrite"] = test_resume_rewrite(api_key)
    
    # Calculate overall success
    success_count = sum(1 for r in results.values() if r)
    total = len(results)
    success_rate = (success_count / total) * 100 if total > 0 else 0
    
    # Print summary
    logger.info("\n===== TEST SUMMARY =====")
    logger.info(f"Tests passed: {success_count}/{total} ({success_rate:.1f}%)")
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")
    
    return success_rate >= 80  # Success if at least 80% of tests pass

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description="Test resume_openai module")
    parser.add_argument("--api-key", type=str, help="OpenAI API key to use")
    parser.add_argument("--client", action="store_true", help="Test client initialization only")
    parser.add_argument("--embedding", action="store_true", help="Test embedding generation only")
    parser.add_argument("--similarity", action="store_true", help="Test similarity calculation only")
    parser.add_argument("--generation", action="store_true", help="Test text generation only")
    parser.add_argument("--enhancement", action="store_true", help="Test text enhancement only")
    parser.add_argument("--rewrite", action="store_true", help="Test resume rewriting only")
    
    args = parser.parse_args()
    
    # Get API key from args or environment
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        logger.warning("⚠️ No OpenAI API key provided. Tests will likely fail.")
        logger.warning("Set OPENAI_API_KEY in your .env file or pass with --api-key")
    else:
        logger.info(f"Using API key: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else ''}")
    
    # If specific tests are requested, run only those
    if args.client:
        test_client_initialization(api_key)
    elif args.embedding:
        test_embedding(api_key)
    elif args.similarity:
        test_similarity(api_key)
    elif args.generation:
        test_text_generation(api_key)
    elif args.enhancement:
        test_text_enhancement(api_key)
    elif args.rewrite:
        test_resume_rewrite(api_key)
    else:
        # Run all tests if no specific test is requested
        run_all_tests(api_key)
    
    logger.info("Tests completed.")

if __name__ == "__main__":
    main() 