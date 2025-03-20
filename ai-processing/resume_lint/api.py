"""
API endpoints for resume linting functionality.
This module provides FastAPI endpoints that can be used to analyze resumes.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from .preprocess import analyze_resume

# Create FastAPI app
app = FastAPI(
    title="Resume Lint API",
    description="API for analyzing and improving resumes",
    version="1.0.0"
)

class ResumeRequest(BaseModel):
    """Input model for resume text analysis."""
    text: str = Field(..., description="The full text of the resume to analyze")
    
class Issue(BaseModel):
    """Model for resume issues."""
    severity: str = Field(..., description="Issue severity (high, medium, low)")
    type: str = Field(..., description="Type of issue")
    message: str = Field(..., description="Human-readable message describing the issue")
    text: Optional[str] = Field(None, description="The text that triggered the issue")
    alternatives: Optional[List[str]] = Field(None, description="Suggested alternatives, if applicable")

class ImprovementCount(BaseModel):
    """Model for counting improvements by severity."""
    high: int = Field(..., description="Number of high severity issues")
    medium: int = Field(..., description="Number of medium severity issues")
    low: int = Field(..., description="Number of low severity issues")
    
class ResumeAnalysisResponse(BaseModel):
    """Output model for resume analysis results."""
    score: int = Field(..., description="Resume score (0-100)")
    issues: List[Dict[str, Any]] = Field(..., description="List of issues found")
    feedback: str = Field(..., description="Overall feedback summary")
    improvement_count: ImprovementCount = Field(..., description="Count of improvements by severity")

@app.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze(request: ResumeRequest):
    """
    Analyze a resume text and provide feedback on improvements.
    
    This endpoint performs a comprehensive analysis of resume text, checking for:
    - Passive voice
    - Weak phrases
    - Missing quantifiable achievements
    - Overly long sentences
    - ATS-unfriendly elements
    
    Returns a score and detailed feedback to improve the resume.
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    
    try:
        analysis = analyze_resume(request.text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns a simple status message to indicate the service is running.
    """
    return {"status": "healthy", "service": "resume-lint"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 