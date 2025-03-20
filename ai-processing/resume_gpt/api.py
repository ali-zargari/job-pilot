"""
FastAPI API wrapper for the resume_gpt module.
Provides endpoints to access the resume enhancement functionality.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
from . import infer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

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