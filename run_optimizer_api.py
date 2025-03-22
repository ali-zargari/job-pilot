"""
Script to run the Resume Optimizer API with AI rewrite feature enabled.
"""
import os
import uvicorn
from dotenv import load_dotenv
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("resume-optimizer")

# Load environment variables from .env file
load_dotenv()

# Print current working directory and environment for debugging
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python version: {sys.version}")
logger.info(f"Environment variables loaded from: {os.path.abspath('.env') if os.path.exists('.env') else 'Not found'}")

# Check if OpenAI API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")
api_key_status = "Not set" if not openai_api_key else f"Set ({openai_api_key[:5]}...{openai_api_key[-5:] if len(openai_api_key) > 10 else ''})"
logger.info(f"OpenAI API key status: {api_key_status}")

if not openai_api_key or openai_api_key == "your_openai_api_key_here":
    logger.warning("⚠️  WARNING: OpenAI API key is not set or using the placeholder value!")
    logger.warning("Please set your OpenAI API key in the .env file to use the AI rewrite feature.")
    logger.warning("The optimizer will fallback to rule-based mode without a valid API key.\n")
    
    # Set local_mode to true in environment
    os.environ["LOCAL_MODE"] = "true"
else:
    logger.info("✅ OpenAI API key found. AI rewrite feature is ENABLED.\n")
    
    # Test OpenAI API
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        logger.info("Testing OpenAI API connection...")
        
        # Simple API test
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one word."}
            ],
            max_tokens=10
        )
        
        logger.info(f"✅ OpenAI API test successful! Response: {response.choices[0].message.content}")
        os.environ["LOCAL_MODE"] = "false"
    except Exception as e:
        logger.error(f"❌ OpenAI API test failed: {str(e)}")
        logger.warning("Falling back to rule-based mode without AI rewrite.")
        os.environ["LOCAL_MODE"] = "true"

# Run the API
logger.info("")
logger.info("=====================================")
logger.info("Starting Resume Optimizer API...")
logger.info(f"AI rewrite feature: {'ENABLED' if os.environ.get('LOCAL_MODE') != 'true' else 'DISABLED'}")
logger.info("API will be available at: http://localhost:8002")
logger.info("API documentation: http://localhost:8002/docs")
logger.info("=====================================")
logger.info("")

if __name__ == "__main__":
    try:
        # Start the server with reload enabled for development
        uvicorn.run(
            "ai_processing.resume_optimizer.api:app", 
            host="0.0.0.0", 
            port=8002,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        logger.error(f"Failed to start the API server: {str(e)}")
        sys.exit(1) 