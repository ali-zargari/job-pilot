"""
API endpoints for the resume optimizer module.
Provides access to the two-tier AI optimization system.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from . import optimizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Resume Optimizer API",
    description="Two-tier AI system for resume optimization",
    version="0.1.0"
)

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Models
class OptimizationRequest(BaseModel):
    """Model for resume optimization request"""
    resume_text: str = Field(..., description="Resume text to optimize")
    job_description: Optional[str] = Field(None, description="Target job description")
    reference_resumes: Optional[List[str]] = Field(None, description="List of reference resumes")
    
class Suggestion(BaseModel):
    """Model for resume improvement suggestion"""
    text: str = Field(..., description="Text that needs improvement")
    message: str = Field(..., description="Suggestion message")
    severity: str = Field(..., description="Issue severity")
    type: str = Field(..., description="Type of issue")
    alternatives: Optional[List[str]] = Field(None, description="Suggested alternatives")
    
class OptimizationResponse(BaseModel):
    """Model for optimization response"""
    original: str = Field(..., description="Original resume text")
    rule_based: str = Field(..., description="Initial rule-based draft")
    optimized: str = Field(..., description="Final optimized text")
    score: int = Field(..., description="Resume score")
    lint_results: Dict = Field(..., description="Detailed analysis results")
    suggestions: Optional[Dict] = Field(None, description="Rule-based suggestions for improvement")
    improvements: Optional[List[str]] = Field(None, description="AI-generated improvements")
    
class SuggestionRequest(BaseModel):
    """Model for getting improvement suggestions"""
    resume_text: str = Field(..., description="Resume text to analyze")
    job_description: Optional[str] = Field(None, description="Target job description")

# Dependencies
def get_optimizer_instance():
    """Get ResumeOptimizer instance"""
    return optimizer.get_optimizer()

# Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "resume-optimizer"}

@app.post("/optimize", response_model=OptimizationResponse)
async def optimize_resume(
    request: OptimizationRequest,
    resume_optimizer: optimizer.ResumeOptimizer = Depends(get_optimizer_instance)
):
    """
    Optimize a resume using the two-tier AI system.
    
    This endpoint:
    1. Uses GPT-4 for fast initial draft
    2. Applies precision optimization with fine-tuned models
    3. Returns both draft and final versions
    """
    try:
        if not request.resume_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume text cannot be empty"
            )
            
        result = resume_optimizer.optimize_resume(
            resume_text=request.resume_text,
            job_description=request.job_description,
            reference_resumes=request.reference_resumes,
            apply_ai_rewrite=True  # Always use AI rewrite
        )
        
        return OptimizationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error optimizing resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing resume: {str(e)}"
        )
        
@app.post("/suggestions", response_model=List[Suggestion])
async def get_suggestions(
    request: SuggestionRequest,
    resume_optimizer: optimizer.ResumeOptimizer = Depends(get_optimizer_instance)
):
    """
    Get inline suggestions for resume improvements.
    
    This endpoint:
    1. Analyzes the resume for issues
    2. Provides specific suggestions for each issue
    3. Includes AI-generated alternatives
    """
    try:
        if not request.resume_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume text cannot be empty"
            )
            
        suggestions = resume_optimizer.get_suggestions(
            resume_text=request.resume_text,
            job_description=request.job_description
        )
        
        return suggestions
        
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting suggestions: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 