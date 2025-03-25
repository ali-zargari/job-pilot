import spacy
from . import rules
import re

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
    
    # Improved bullet detection patterns
    bullet_patterns = [
        # Standard bullet characters
        r'^\s*[•\-\*\→\▪\▸\‣\○\·\–\—\♦\★\»\▶]\s+(.+)$',
        # Numbered bullets
        r'^\s*\d+[\.\)]\s+(.+)$',
        # Letter bullets
        r'^\s*[a-zA-Z][\.\)]\s+(.+)$',
        # Diamond bullets
        r'^\s*[\◆\◇\◊\♦]\s+(.+)$',
        # Lines with some indentation that appear after a bullet line
        r'^\s{2,}(.+)$'
    ]
    
    # Two-pass process: first detect bullet starters, then combine multi-line bullets
    bullet_start_indices = []
    potential_bullets = []
    
    # First pass: identify potential bullet starting lines
    for i, line in enumerate(lines):
        line = line.strip()
        is_bullet_start = False
        
        for pattern in bullet_patterns[:4]:  # Only check actual bullet starters, not continuation lines
            if re.match(pattern, line):
                is_bullet_start = True
                bullet_start_indices.append(i)
                potential_bullets.append(line)
                break
                
        if not is_bullet_start and i > 0:
            # Check for lines that are likely continuations of previous bullets
            # This handles PDF parsing that breaks lines in the middle of a bullet point
            prev_line = lines[i-1].strip()
            
            # If previous line ended without punctuation or is very short, this line may be a continuation
            if prev_line and (
                not prev_line[-1] in '.!?:;' or  # No ending punctuation
                len(prev_line) < 40 or           # Previous line is short (likely a broken line)
                not prev_line[0].isupper()       # Previous line doesn't start with a capital letter
            ):
                if i-1 in bullet_start_indices or (potential_bullets and len(potential_bullets) > 0):
                    # Add to the last bullet as a continuation
                    if potential_bullets:
                        potential_bullets[-1] += ' ' + line
    
    # Second pass: consolidate multi-line bullets
    current_bullet = ""
    in_bullet = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            if in_bullet and current_bullet:
                bullets.append(current_bullet)
                current_bullet = ""
                in_bullet = False
            continue
            
        is_bullet_start = i in bullet_start_indices
        
        if is_bullet_start:
            if in_bullet and current_bullet:
                bullets.append(current_bullet)
                current_bullet = ""
            
            current_bullet = line
            in_bullet = True
        elif in_bullet:
            # Check if this is likely a continuation of the current bullet
            if (
                re.match(bullet_patterns[4], ' ' + line) or  # Indented continuation
                not line[0].isupper() or                     # Doesn't start with uppercase (continuation)
                not any(line.startswith(b) for b in '•-*→▪▸‣○·–—♦★»▶') or  # Not a new bullet
                len(current_bullet) < 50                     # Current bullet is short (likely incomplete)
            ):
                current_bullet += ' ' + line
            else:
                # This looks like a new paragraph or section, not a bullet continuation
                bullets.append(current_bullet)
                current_bullet = line
                in_bullet = False
    
    # Add the last bullet if we have one
    if current_bullet:
        bullets.append(current_bullet)
            
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
        
        # Extract rule-based suggestions
        rule_based_suggestions = rules.get_rule_based_suggestions(resume_text)
        
        issues = []
        score = 100  # Start with a perfect score
        
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
                "message": "⚠️ Consider adding more bullet points to highlight your achievements and improve readability.",
                "text": resume_text[:100] + "..."
            })
            score -= 5
        
        # Add strengths based on evidence
        strengths = []
        
        # Add strong action verbs as a strength
        strong_verbs = optimization_evidence['strong_verbs']
        if strong_verbs:
            # Pick up to 3 strong verbs to highlight
            highlighted_verbs = strong_verbs[:3]
            strengths.append({
                "severity": "positive",
                "type": "strong_verbs",
                "message": f"✅ Good use of strong action verbs like '{', '.join(highlighted_verbs)}'. Continue using impactful language.",
                "text": resume_text[:100] + "..."
            })
            score += 5
        
        # Add quantifiable achievements as a strength
        if optimization_evidence.get('quantifiable_achievements'):
            # Extract examples of quantifiable achievements
            quantifiable_examples = []
            # Look for numbers followed by % or other indicators of metrics
            patterns = [
                r'\d+\s*%',                   # Percentage
                r'\$\s*\d+',                  # Dollar amounts
                r'\d+\s*x',                   # Multiplier
                r'by\s+\d+',                  # "by X" phrases
                r'improved\s+\w+\s+by\s+\d+', # "improved X by Y"
                r'increased\s+\w+\s+by\s+\d+', # "increased X by Y"
                r'reduced\s+\w+\s+by\s+\d+',  # "reduced X by Y"
                r'generated\s+\$?\d+',        # "generated $X"
                r'team\s+of\s+\d+',           # Team size
                r'\d+\s+hours',               # Time measurements
                r'\d+\s+members',             # Team members
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, resume_text, re.IGNORECASE)
                if matches:
                    for match in matches[:2]:  # Limit to first 2 examples
                        # Get some context around the match
                        match_index = resume_text.lower().find(match.lower())
                        if match_index >= 0:
                            # Get up to 20 chars before and after for context
                            start = max(0, match_index - 20)
                            end = min(len(resume_text), match_index + len(match) + 20)
                            context = resume_text[start:end].strip()
                            # Clean up the context
                            if start > 0:
                                context = "..." + context
                            if end < len(resume_text):
                                context = context + "..."
                            quantifiable_examples.append(context)
            
            # Create message with examples
            metric_message = "✅ Excellent use of quantifiable achievements."
            if quantifiable_examples:
                metric_message += " Examples: " + "; ".join(quantifiable_examples[:2])
            metric_message += " This helps demonstrate your impact."
            
            strengths.append({
                "severity": "positive",
                "type": "metrics",
                "message": metric_message,
                "text": resume_text[:100] + "..."
            })
            score += 5
        
        # If there are no detected strengths but the resume has content,
        # add a generic strength to encourage the user
        if not strengths and len(resume_text) > 500:
            strengths.append({
                "severity": "positive",
                "type": "structure",
                "message": "✅ Your resume has a clear structure that provides a good foundation to build upon.",
                "text": resume_text[:100] + "..."
            })
        
        # Combine strengths with issues
        all_issues = strengths + issues
        
        # If there are no issues but there are rule-based suggestions,
        # add a generic improvement area
        if not issues and (rule_based_suggestions['weak_verbs'] or rule_based_suggestions['content_improvements']):
            all_issues.append({
                "severity": "low",
                "type": "general",
                "message": "⚠️ Your resume is good, but could be strengthened with more impactful language.",
                "text": resume_text[:100] + "..."
            })
        
        # Generate feedback based on score
        feedback = ""
        if score >= 90:
            feedback = "✅ Your resume is well-structured with minimal issues. Check out the rule-based suggestions for further improvements!"
        elif score >= 75:
            feedback = "⚠️ Your resume is decent but could use some targeted improvements in clarity and impact."
        else:
            feedback = "❌ Your resume has several areas for improvement. Follow the suggestions to enhance its effectiveness."
        
        return {
            "score": score,
            "issues": all_issues,
            "feedback": feedback,
            "improvement_count": {
                "high": len([i for i in issues if i["severity"] == "high"]),
                "medium": len([i for i in issues if i["severity"] == "medium"]),
                "low": len([i for i in issues if i["severity"] == "low"]),
                "positive": len(strengths)
            },
            "is_already_optimized": is_optimized,
            "optimization_evidence": optimization_evidence,
            "suggestions": rule_based_suggestions
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
