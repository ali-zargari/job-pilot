import spacy
import re

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# List of weak phrases that should be replaced with stronger action verbs
WEAK_PHRASES = [
    "responsible for", "worked on", "in charge of", "duties included", "helped with", "assisted in"
]

# Strong action verbs that indicate an already-optimized resume
STRONG_ACTION_VERBS = [
    "achieved", "accelerated", "accomplished", "acquired", "adapted", "addressed", "advanced", "advised",
    "allocated", "analyzed", "applied", "appointed", "appraised", "approved", "architected", "arranged",
    "assembled", "assessed", "assigned", "attained", "authored", "automated", "balanced", "boosted",
    "built", "calculated", "captured", "catalyzed", "centralized", "championed", "clarified", "coached",
    "collaborated", "communicated", "compiled", "completed", "conceptualized", "conducted", "consolidated",
    "constructed", "consulted", "controlled", "converted", "coordinated", "created", "cultivated", "customized",
    "decreased", "defined", "delegated", "delivered", "demonstrated", "designed", "determined", "developed",
    "devised", "diagnosed", "directed", "discovered", "doubled", "drove", "earned", "edited", "educated",
    "eliminated", "enabled", "encouraged", "engineered", "enhanced", "established", "evaluated", "exceeded",
    "executed", "expanded", "expedited", "engineered", "facilitated", "finalized", "fixed", "forecasted",
    "formulated", "founded", "generated", "grew", "guided", "headed", "hired", "identified", "implemented",
    "improved", "increased", "influenced", "initiated", "innovated", "installed", "instituted", "instructed",
    "integrated", "introduced", "invented", "investigated", "launched", "led", "leveraged", "maintained",
    "managed", "marketed", "maximized", "measured", "mentored", "merged", "minimized", "modernized", "monitored",
    "motivated", "navigated", "negotiated", "operated", "optimized", "orchestrated", "organized", "outperformed",
    "overhauled", "oversaw", "pioneered", "planned", "presented", "prioritized", "processed", "produced",
    "programmed", "promoted", "proposed", "provided", "published", "purchased", "recommended", "redesigned",
    "reduced", "reengineered", "refined", "refocused", "regulated", "reorganized", "reported", "researched",
    "resolved", "restructured", "revamped", "reviewed", "revitalized", "saved", "scheduled", "secured",
    "selected", "served", "set", "shaped", "simplified", "sold", "solved", "specialized", "spearheaded",
    "standardized", "started", "streamlined", "strengthened", "structured", "succeeded", "supervised", 
    "supported", "surpassed", "surveyed", "sustained", "systematized", "targeted", "taught", "tested",
    "trained", "transformed", "translated", "upgraded", "utilized", "validated", "won", "wrote"
]

# Stronger alternatives for weak phrases
STRONG_ALTERNATIVES = {
    "responsible for": ["managed", "led", "orchestrated", "directed", "oversaw"],
    "worked on": ["developed", "implemented", "executed", "delivered", "created"],
    "in charge of": ["managed", "headed", "directed", "led", "supervised"],
    "duties included": ["achieved", "performed", "executed", "delivered", "completed"],
    "helped with": ["contributed to", "supported", "facilitated", "collaborated on", "enhanced"],
    "assisted in": ["supported", "contributed to", "facilitated", "collaborated on", "aided"]
}

# List of common ATS-unfriendly elements - more specific to avoid false positives
BAD_FORMATTING_PATTERNS = [
    r"<img.*?>",  # Detects HTML images
    r"<table.*?>.*?</table>",  # Detects HTML tables
    r"[^a-zA-Z0-9\s,.!?:;'\-•*#@%$()/\\\"]+",  # Detects truly problematic special characters (emojis, etc)
]

# Valid bullet point characters that should NOT trigger warnings
VALID_BULLET_CHARS = ['•', '-', '*', '→', '▪', '▸', '‣', '○', '·', '–', '—', '♦', '★', '»', '▶']

# Detects passive voice using auxiliary passive verbs
def check_passive_voice(sentence):
    """
    Detects if a sentence is written in passive voice.
    
    Args:
        sentence (str): The sentence to analyze
        
    Returns:
        bool: True if passive voice is detected, False otherwise
    """
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == "auxpass":  # Passive voice detected
            return True
    return False

# Detects weak phrases that reduce impact
def check_weak_phrases(sentence):
    """
    Detects weak phrases in a sentence that reduce impact.
    
    Args:
        sentence (str): The sentence to analyze
        
    Returns:
        str or None: The weak phrase if found, None otherwise
    """
    for phrase in WEAK_PHRASES:
        if phrase in sentence.lower():
            return phrase
    return None

# Detects missing quantifiable achievements (flags bullet points without numbers)
def check_missing_numbers(sentence):
    """
    Detects missing quantifiable achievements.
    
    Args:
        sentence (str): The sentence to analyze
        
    Returns:
        bool: True if no numbers are detected, False otherwise
    """
    if not re.search(r'\d+', sentence):  # No numbers detected
        return True
    return False

# Checks if a sentence is too long (hard to read)
def check_sentence_length(text):
    """
    Check if a sentence is too long.
    
    Args:
        text (str): The sentence to check
        
    Returns:
        bool: True if the sentence is too long, False otherwise
    """
    # Don't treat bullet point lists as one sentence
    if text.startswith(tuple(VALID_BULLET_CHARS)):
        # For bullet points, shorter threshold
        return len(text.split()) > 25
    
    # For regular sentences
    return len(text.split()) > 20

# Checks for ATS-unfriendly elements (images, tables, problematic special characters)
def check_ats_friendly(resume_text):
    """
    Checks if the resume text contains ATS-unfriendly elements.
    
    Args:
        resume_text (str): The full resume text
        
    Returns:
        bool: True if ATS-unfriendly elements are found, False otherwise
    """
    # Only detect truly problematic elements, not standard bullet points or formatting
    for pattern in BAD_FORMATTING_PATTERNS:
        if re.search(pattern, resume_text, re.DOTALL):
            # Don't count matches that are just common bullet points or formatting
            matches = re.findall(pattern, resume_text, re.DOTALL)
            for match in matches:
                # Skip if it's a valid bullet character
                if match in VALID_BULLET_CHARS:
                    continue
                return True
    return False

# Suggest improvements for weak phrases
def suggest_alternatives(weak_phrase):
    """
    Suggests stronger alternatives for weak phrases.
    
    Args:
        weak_phrase (str): The weak phrase to find alternatives for
        
    Returns:
        list: A list of suggested alternative phrases
    """
    if weak_phrase in STRONG_ALTERNATIVES:
        return STRONG_ALTERNATIVES[weak_phrase]
    return []

# Check if the text contains bullet points
def has_bullet_points(text):
    """
    Checks if the text contains bullet points.
    
    Args:
        text (str): The text to check
        
    Returns:
        bool: True if bullet points are found, False otherwise
    """
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        # Check for common bullet characters
        for bullet in VALID_BULLET_CHARS:
            if line.startswith(bullet):
                return True
        # Check for numbered bullets
        if len(line) > 2 and line[0].isdigit() and line[1] in ['.', ')']:
            return True
    return False

# NEW: Check for strong action verbs in text
def check_strong_action_verbs(text):
    """
    Detects the presence of strong action verbs in text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        list: List of strong action verbs found
    """
    words = re.findall(r'\b\w+\b', text.lower())
    found_verbs = []
    
    for verb in STRONG_ACTION_VERBS:
        if verb.lower() in words:
            found_verbs.append(verb)
            
    return found_verbs

# NEW: Check for quantifiable achievements
def has_quantifiable_achievements(text):
    """
    Determines if the text contains quantifiable achievements.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        bool: True if quantifiable achievements are found
    """
    # Look for numbers followed by % or other indicators of metrics
    patterns = [
        r'\d+\s*%',  # Percentage (e.g., "increased revenue by 25%")
        r'\$\s*\d+',  # Dollar amounts (e.g., "$1.5 million in sales")
        r'\d+\s*x',  # Multiplier (e.g., "5x increase")
        r'by\s+\d+', # "by X" phrases (e.g., "improved by 30")
        r'increased\s+\w+\s+by\s+\d+', # "increased X by Y" pattern
        r'reduced\s+\w+\s+by\s+\d+', # "reduced X by Y" pattern
        r'generated\s+\w+\s+\d+', # "generated X Y" pattern
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
            
    return False

# NEW: Is resume already optimized (high quality)
def is_already_optimized(resume_text):
    """
    Evaluates if a resume is already well-optimized.
    
    Args:
        resume_text (str): The full resume text
        
    Returns:
        (bool, dict): Tuple with optimization status and supporting evidence
    """
    # Setup counters and evidence
    evidence = {
        'bullet_points': has_bullet_points(resume_text),
        'strong_verbs': [],
        'quantifiable_achievements': False,
        'passive_voice_count': 0,
        'weak_phrases_count': 0
    }
    
    # Check for strong action verbs
    evidence['strong_verbs'] = check_strong_action_verbs(resume_text)
    
    # Check for quantifiable achievements
    evidence['quantifiable_achievements'] = has_quantifiable_achievements(resume_text)
    
    # Process each bullet point for passive voice and weak phrases
    lines = resume_text.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            if check_passive_voice(line):
                evidence['passive_voice_count'] += 1
            
            if check_weak_phrases(line):
                evidence['weak_phrases_count'] += 1
    
    # Evaluate if resume is optimized based on evidence
    # A resume is considered optimized if:
    # 1. It has bullet points
    # 2. It uses at least 5 strong action verbs
    # 3. It has quantifiable achievements
    # 4. It has minimal passive voice and weak phrases
    is_optimized = (
        evidence['bullet_points'] and
        len(evidence['strong_verbs']) >= 5 and
        evidence['quantifiable_achievements'] and
        evidence['passive_voice_count'] <= 1 and  # Allow at most 1 instance
        evidence['weak_phrases_count'] <= 1       # Allow at most 1 instance
    )
    
    return is_optimized, evidence
