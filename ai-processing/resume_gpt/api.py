"""
FastAPI API wrapper for the resume_gpt module.
Provides endpoints to access the resume enhancement functionality.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from . import infer
import os
import re
import torch
import transformers
from transformers import T5ForConditionalGeneration, T5Tokenizer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Common programming languages, frameworks, and tools
COMMON_TECHNOLOGIES = {
    "languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Ruby", "PHP", 
        "Go", "Rust", "Swift", "Kotlin", "HTML", "CSS", "SQL", "R", "Scala", "Perl",
        "Shell", "Bash", "PowerShell", "MATLAB", "Julia", "Dart", "Assembly", "COBOL",
        "Fortran", "Haskell", "Lua", "Objective-C"
    ],
    "frameworks": [
        "React", "Angular", "Vue", "Django", "Flask", "FastAPI", "Spring", "Express", 
        "Rails", "Laravel", "ASP.NET", "Node.js", "Bootstrap", "Tailwind", "jQuery",
        "TensorFlow", "PyTorch", "Keras", "Pandas", "NumPy", "Scikit-learn", "Next.js",
        "Gatsby", "Redux", "GraphQL", "Apollo", "Ember", "Svelte", "Meteor", "Nest.js",
        "Xamarin", "Flutter", "Electron", "Symfony", "CodeIgniter", "Zend", "Slim"
    ],
    "tools": [
        "Git", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Heroku", "Jenkins", "CircleCI",
        "Travis CI", "GitHub Actions", "Ansible", "Terraform", "Puppet", "Chef", "Grafana",
        "Prometheus", "ELK Stack", "Jira", "Confluence", "Figma", "Sketch", "Adobe XD",
        "VS Code", "IntelliJ", "PyCharm", "Eclipse", "Xcode", "Android Studio", "Unity"
    ],
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server", "Redis", 
        "Cassandra", "DynamoDB", "Firebase", "Elasticsearch", "Neo4j", "Couchbase",
        "MariaDB", "InfluxDB", "H2", "Fauna", "CockroachDB", "Supabase"
    ],
    "cloud": [
        "AWS", "Azure", "GCP", "Heroku", "DigitalOcean", "Linode", "Cloudflare", "Netlify",
        "Vercel", "AWS Lambda", "S3", "EC2", "RDS", "DynamoDB", "SQS", "SNS", "API Gateway",
        "Azure Functions", "Azure Blob Storage", "Google Cloud Functions", "Firebase"
    ]
}

# Flatten the technology list for easy lookup
ALL_TECHNOLOGIES = []
for category, techs in COMMON_TECHNOLOGIES.items():
    ALL_TECHNOLOGIES.extend(techs)
ALL_TECHNOLOGIES = sorted(ALL_TECHNOLOGIES, key=len, reverse=True)  # Sort by length for better matching

def extract_tech_stack(text: str) -> List[str]:
    """
    Extract technology stack mentioned in the text.
    
    Args:
        text: The text to extract technology stack from
        
    Returns:
        List of technologies found
    """
    if not text:
        return []
        
    found_techs = set()
    
    # Normalize text
    text_lower = text.lower()
    
    # First check exact matches for all technologies
    for tech in ALL_TECHNOLOGIES:
        tech_pattern = r'\b' + re.escape(tech) + r'\b'
        if re.search(tech_pattern, text, re.IGNORECASE):
            found_techs.add(tech)
    
    # Special case for languages/frameworks with "+" like "C++"
    for special in ["C++", "C#"]:
        if special.lower() in text_lower:
            found_techs.add(special)
    
    # Additional checks for common abbreviations
    abbr_mapping = {
        "js": "JavaScript",
        "ts": "TypeScript",
        "py": "Python",
        "rb": "Ruby",
        "tf": "TensorFlow",
        "k8s": "Kubernetes"
    }
    
    for abbr, full in abbr_mapping.items():
        abbr_pattern = r'\b' + re.escape(abbr) + r'\b'
        if re.search(abbr_pattern, text, re.IGNORECASE):
            found_techs.add(full)
    
    return sorted(list(found_techs))

def enhance_resume(resume_texts: List[str]) -> List[str]:
    """
    Enhance multiple resume texts using the T5 model.
    
    Args:
        resume_texts: List of resume texts to enhance
        
    Returns:
        List of enhanced resume texts
    """
    # Check for model directory
    model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resume_gpt", "model")
    
    # Choose model path - use fine-tuned if available, else base model
    if os.path.exists(model_dir):
        model_path = model_dir
        logger.info(f"Using fine-tuned model from {model_path}")
    else:
        model_path = "t5-small"
        logger.info(f"Fine-tuned model not found at {model_dir}. Using base model {model_path} instead.")
    
    # Load model and tokenizer
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    
    enhanced_texts = []
    
    for text in resume_texts:
        # Prepare input
        input_text = f"enhance resume: {text}"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids
        
        # Generate enhanced text
        outputs = model.generate(
            input_ids, 
            max_length=512, 
            num_beams=4,
            early_stopping=True
        )
        enhanced = tokenizer.decode(outputs[0], skip_special_tokens=True)
        enhanced_texts.append(enhanced)
    
    return enhanced_texts

def enhance_bullet(bullet_text: str) -> str:
    """
    Enhance a single resume bullet point.
    
    Args:
        bullet_text: The bullet point text to enhance
        
    Returns:
        Enhanced bullet point text
    """
    return enhance_resume([bullet_text])[0]

# Create FastAPI app
app = FastAPI(
    title="ResumeGPT API",
    description="API for enhancing resume bullet points using a fine-tuned T5 model",
    version="0.1.0"
)

# Models
class BulletPoint(BaseModel):
    """Model for a single bullet point"""
    text: str = Field(..., description="Text of the bullet point")
    
class EnhancementRequest(BaseModel):
    """Model for enhancement request"""
    bullet_points: List[str] = Field(..., description="List of bullet points to enhance")
    
class EnhancedBullet(BaseModel):
    """Model for an enhanced bullet point"""
    original: str = Field(..., description="Original bullet point text")
    enhanced: str = Field(..., description="Enhanced bullet point text")
    
class EnhancementResponse(BaseModel):
    """Model for enhancement response"""
    enhanced_bullets: List[EnhancedBullet] = Field(..., description="List of enhanced bullet points")
    
class SingleBulletRequest(BaseModel):
    """Model for a single bullet point enhancement request"""
    text: str = Field(..., description="Text of the bullet point to enhance")
    
class SingleBulletResponse(BaseModel):
    """Model for a single bullet point enhancement response"""
    original: str = Field(..., description="Original bullet point text")
    enhanced: str = Field(..., description="Enhanced bullet point text")

# Dependencies
def get_enhancer():
    """Get a ResumeEnhancer instance"""
    return infer.get_enhancer()

# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model": "resume_gpt"}

@app.post("/enhance", response_model=EnhancementResponse)
async def enhance_resume(
    request: EnhancementRequest,
    enhancer: infer.ResumeEnhancer = Depends(get_enhancer)
):
    """
    Enhance multiple resume bullet points
    
    Args:
        request: Enhancement request with list of bullet points
        enhancer: ResumeEnhancer instance
        
    Returns:
        Enhanced bullet points
    """
    try:
        # Validate input
        if not request.bullet_points:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No bullet points provided"
            )
            
        # Process bullet points
        enhanced_data = enhancer.enhance_resume(request.bullet_points)
        
        # Convert to response model
        enhanced_bullets = [
            EnhancedBullet(original=item["original"], enhanced=item["enhanced"])
            for item in enhanced_data
        ]
        
        return EnhancementResponse(enhanced_bullets=enhanced_bullets)
        
    except Exception as e:
        logger.error(f"Error enhancing resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enhancing resume: {str(e)}"
        )
        
@app.post("/enhance/bullet", response_model=SingleBulletResponse)
async def enhance_bullet(
    request: SingleBulletRequest,
    enhancer: infer.ResumeEnhancer = Depends(get_enhancer)
):
    """
    Enhance a single resume bullet point
    
    Args:
        request: Enhancement request with bullet text
        enhancer: ResumeEnhancer instance
        
    Returns:
        Enhanced bullet point
    """
    try:
        # Validate input
        if not request.text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text provided"
            )
            
        # Process bullet point
        enhanced_text = enhancer.enhance_bullet(request.text)
        
        return SingleBulletResponse(
            original=request.text,
            enhanced=enhanced_text
        )
        
    except Exception as e:
        logger.error(f"Error enhancing bullet point: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enhancing bullet point: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 