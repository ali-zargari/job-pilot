import spacy
from . import rules

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

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
        doc = self.nlp(resume_text)
        issues = []
        score = 100  # Start with a perfect score
        
        # Step 1: Check ATS-friendliness (high priority)
        if rules.check_ats_friendly(resume_text):
            issues.append({
                "severity": "high",
                "type": "format",
                "message": "❌ Avoid using images, tables, or special characters (ATS may reject them)."
            })
            score -= 10
        
        # Step 2: Analyze each sentence in the resume
        for sentence in doc.sents:
            sentence_text = sentence.text.strip()
            
            # Skip empty sentences
            if not sentence_text:
                continue
                
            # Check for passive voice
            if rules.check_passive_voice(sentence_text):
                issues.append({
                    "severity": "medium",
                    "type": "passive_voice",
                    "message": f"⚠️ Consider rewriting: '{sentence_text}' (Passive voice detected)",
                    "text": sentence_text
                })
                score -= 5
            
            # Check for weak phrases
            weak_phrase = rules.check_weak_phrases(sentence_text)
            if weak_phrase:
                alternatives = rules.suggest_alternatives(weak_phrase)
                alt_text = ", ".join(alternatives[:3]) if alternatives else "stronger action verbs"
                
                issues.append({
                    "severity": "medium",
                    "type": "weak_phrase",
                    "message": f"⚠️ Replace '{weak_phrase}' in: '{sentence_text}' (Try using {alt_text})",
                    "text": sentence_text,
                    "alternatives": alternatives
                })
                score -= 5
            
            # Check for missing numbers
            if rules.check_missing_numbers(sentence_text):
                # Only flag bullet points or sentences that look like achievements
                if sentence_text.startswith("•") or any(verb in sentence_text.lower() for verb in ["developed", "created", "managed", "led", "implemented", "improved"]):
                    issues.append({
                        "severity": "medium",
                        "type": "missing_numbers",
                        "message": f"⚠️ Consider adding quantifiable achievements in: '{sentence_text}' (Use numbers)",
                        "text": sentence_text
                    })
                    score -= 3
            
            # Check for overly long sentences
            if rules.check_sentence_length(sentence_text):
                issues.append({
                    "severity": "low",
                    "type": "long_sentence",
                    "message": f"⚠️ This sentence is too long: '{sentence_text}' (Consider making it more concise)",
                    "text": sentence_text
                })
                score -= 2
        
        # Final feedback based on score
        feedback = ""
        if score >= 90:
            feedback = "✅ Your resume is well-structured with minimal issues!"
        elif score >= 75:
            feedback = "⚠️ Your resume is decent but could use improvements in clarity and impact."
        else:
            feedback = "❌ Your resume has multiple weak points. Consider major improvements."
        
        return {
            "score": score,
            "issues": issues,
            "feedback": feedback,
            "improvement_count": {
                "high": len([i for i in issues if i["severity"] == "high"]),
                "medium": len([i for i in issues if i["severity"] == "medium"]),
                "low": len([i for i in issues if i["severity"] == "low"])
            }
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
