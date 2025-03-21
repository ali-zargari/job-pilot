import spacy
from . import rules

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Preprocess the resume text to clean it up and prepare for analysis.
    
    Args:
        text (str): The raw resume text
        
    Returns:
        str: Cleaned and normalized text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Basic text normalization
    text = text.replace('\t', ' ')
    
    return text

def extract_bullet_points(text):
    """
    Extract bullet points from resume text.
    
    Args:
        text (str): The resume text
        
    Returns:
        list: List of bullet point strings
    """
    lines = text.split('\n')
    bullets = []
    
    for line in lines:
        line = line.strip()
        # Check for common bullet characters
        if any(line.startswith(bullet) for bullet in rules.VALID_BULLET_CHARS):
            bullets.append(line)
        # Check for numbered bullets
        elif len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')']:
            bullets.append(line)
            
    return bullets

class ResumeAnalyzer:
    """
    A class to analyze resumes and provide feedback on improvements.
    """
    
    def __init__(self):
        """
        Initialize the ResumeAnalyzer.
        """
        self.nlp = nlp
    
    def analyze_resume(self, resume_text):
        """
        Analyzes a resume text and returns a dict with score and issues found.
        
        Args:
            resume_text (str): The full resume text
            
        Returns:
            dict: A dictionary containing score and list of issues
        """
        # First preprocess the text
        cleaned_text = preprocess_text(resume_text)
        
        # Check if the resume is already optimized
        is_optimized, optimization_evidence = rules.is_already_optimized(resume_text)
        
        issues = []
        score = 100  # Start with a perfect score
        
        # If resume is already optimized, provide positive feedback and return early
        if is_optimized:
            return {
                "score": 95,  # High but not perfect score
                "issues": [],  # No issues to report
                "feedback": "✅ Your resume is already well-optimized! It has strong action verbs, quantifiable achievements, and proper formatting.",
                "improvement_count": {
                    "high": 0,
                    "medium": 0,
                    "low": 0
                },
                "is_already_optimized": True,
                "optimization_evidence": optimization_evidence
            }
        
        # Step 1: Check ATS-friendliness (high priority) using original text to preserve formatting
        if rules.check_ats_friendly(resume_text):
            issues.append({
                "severity": "high",
                "type": "format",
                "message": "❌ Avoid using images, tables, or special characters (ATS may reject them)."
            })
            score -= 10
        
        # Step 2: Process each bullet point or paragraph as a unit
        # This prevents treating multi-line bullets as separate items
        bullet_points = []
        current_bullet = ""
        
        # Parse the text into logical bullet points and paragraphs
        lines = resume_text.split('\n')
        in_bullet = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                if in_bullet and current_bullet:
                    bullet_points.append(current_bullet)
                    current_bullet = ""
                    in_bullet = False
                continue
                
            # Check if this is a section header (likely all caps with few words)
            is_header = line.isupper() and len(line.split()) <= 4
            if is_header:
                if in_bullet and current_bullet:
                    bullet_points.append(current_bullet)
                    current_bullet = ""
                    in_bullet = False
                continue
            
            # Check if this line starts a new bullet point
            starts_with_bullet = line.startswith(tuple(rules.VALID_BULLET_CHARS)) or (len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')'])
            
            if starts_with_bullet:
                # If we were in a bullet, save the previous one
                if in_bullet and current_bullet:
                    bullet_points.append(current_bullet)
                    current_bullet = ""
                
                # Start a new bullet
                current_bullet = line
                in_bullet = True
            elif in_bullet:
                # Continue the current bullet (this is a multi-line bullet)
                current_bullet += " " + line
            else:
                # Regular paragraph, treat as its own item
                bullet_points.append(line)
        
        # Add the last bullet if we have one
        if current_bullet:
            bullet_points.append(current_bullet)
        
        # Process each logical bullet point or paragraph
        for bullet in bullet_points:
            # Skip if it's just a bullet character
            if bullet in rules.VALID_BULLET_CHARS:
                continue
                
            # Skip if it's just a number with punctuation (like "1.")
            if len(bullet) <= 2 and bullet[0].isdigit():
                continue
                
            # Parse with spaCy for passive voice detection
            bullet_doc = self.nlp(bullet)
            
            # Check for passive voice
            if rules.check_passive_voice(bullet):
                issues.append({
                    "severity": "medium",
                    "type": "passive_voice",
                    "message": f"⚠️ Consider rewriting: '{bullet}' (Passive voice detected)",
                    "text": bullet
                })
                score -= 5
            
            # Check for weak phrases
            weak_phrase = rules.check_weak_phrases(bullet)
            if weak_phrase:
                alternatives = rules.suggest_alternatives(weak_phrase)
                alt_text = ", ".join(alternatives[:3]) if alternatives else "stronger action verbs"
                
                issues.append({
                    "severity": "medium",
                    "type": "weak_phrase",
                    "message": f"⚠️ Replace '{weak_phrase}' in: '{bullet}' (Try using {alt_text})",
                    "text": bullet,
                    "alternatives": alternatives
                })
                score -= 5
            
            # Check for missing numbers in bullet points
            if bullet.startswith(tuple(rules.VALID_BULLET_CHARS)) and rules.check_missing_numbers(bullet):
                # Only flag bullet points or sentences that look like achievements
                if any(verb in bullet.lower() for verb in ["developed", "created", "managed", "led", "implemented", "improved"]):
                    issues.append({
                        "severity": "medium",
                        "type": "missing_numbers",
                        "message": f"⚠️ Consider adding quantifiable achievements in: '{bullet}' (Use numbers)",
                        "text": bullet
                    })
                    score -= 3
            
            # Check for overly long sentences - but only for actual complete thoughts, not headings
            if len(bullet.split()) > 5 and rules.check_sentence_length(bullet):
                issues.append({
                    "severity": "low",
                    "type": "long_sentence",
                    "message": f"⚠️ This bullet is too long: '{bullet}' (Consider making it more concise)",
                    "text": bullet
                })
                score -= 2
        
        # Check for bullet points in the original text
        if not rules.has_bullet_points(resume_text):
            issues.append({
                "severity": "high",
                "type": "format",
                "message": "❌ Your resume doesn't have bullet points. Add bullet points for better readability.",
                "text": resume_text[:100] + "..."
            })
            score -= 10
        
        # Add insights about positive aspects if there are few issues
        if len(issues) <= 2:
            # Provide positive reinforcement for what's already good
            strong_verbs = optimization_evidence['strong_verbs']
            if strong_verbs:
                # Pick up to 3 strong verbs to highlight
                highlighted_verbs = strong_verbs[:3]
                verb_text = ", ".join(highlighted_verbs)
                issues.append({
                    "severity": "positive",
                    "type": "strong_verbs",
                    "message": f"✅ Good use of strong action verbs like '{verb_text}'. Continue using impactful language."
                })
            
            if optimization_evidence['quantifiable_achievements']:
                issues.append({
                    "severity": "positive",
                    "type": "achievements",
                    "message": "✅ Excellent use of quantifiable achievements. This helps demonstrate your impact."
                })
        
        # Final feedback based on score
        feedback = ""
        if score >= 90:
            feedback = "✅ Your resume is well-structured with minimal issues. Keep up the good work!"
        elif score >= 75:
            feedback = "⚠️ Your resume is decent but could use some targeted improvements in clarity and impact."
        else:
            feedback = "❌ Your resume has several areas for improvement. Follow the suggestions to enhance its effectiveness."
        
        return {
            "score": score,
            "issues": issues,
            "feedback": feedback,
            "improvement_count": {
                "high": len([i for i in issues if i["severity"] == "high"]),
                "medium": len([i for i in issues if i["severity"] == "medium"]),
                "low": len([i for i in issues if i["severity"] == "low"]),
                "positive": len([i for i in issues if i["severity"] == "positive"])
            },
            "is_already_optimized": False,
            "optimization_evidence": optimization_evidence
        }

# Create a singleton instance
analyzer = ResumeAnalyzer()

def analyze_resume(resume_text):
    """
    Convenience function to analyze a resume without creating an instance.
    
    Args:
        resume_text (str): The full resume text
        
    Returns:
        dict: A dictionary containing score and list of issues
    """
    return analyzer.analyze_resume(resume_text)

if __name__ == "__main__":
    # Example resume text
    resume_text = """
    Responsible for managing projects and ensuring deadlines were met.
    Worked on various client accounts to improve engagement.
    Assisted in scheduling and administrative tasks for the team.
    Developed a social media strategy but no quantifiable results.
    """
    
    # Run the resume analysis
    result = analyze_resume(resume_text)
    
    # Display results
    print(f"Resume Score: {result['score']}/100")
    print(f"Feedback: {result['feedback']}")
    print("\nIssues:")
    for issue in result["issues"]:
        print(f"[{issue['severity'].upper()}] {issue['message']}")
