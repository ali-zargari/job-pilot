import spacy
import re

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# List of weak phrases that should be replaced with stronger action verbs
WEAK_PHRASES = [
    "responsible for", "worked on", "in charge of", "duties included", "helped with", "assisted in"
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

# List of common ATS-unfriendly elements
BAD_FORMATTING_PATTERNS = [
    r"<img .*?>",  # Detects images
    r"<table.*?>.*?</table>",  # Detects tables
    r"[^\w\s,.!?:;'-]"  # Detects special characters (e.g., emojis, non-standard symbols)
]

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
def check_sentence_length(sentence, max_words=20):
    """
    Checks if a sentence is too long and hard to read.
    
    Args:
        sentence (str): The sentence to analyze
        max_words (int): Maximum allowed words in a sentence
        
    Returns:
        bool: True if sentence is too long, False otherwise
    """
    words = sentence.split()
    return len(words) > max_words

# Checks for ATS-unfriendly elements (images, tables, special characters)
def check_ats_friendly(resume_text):
    """
    Checks if the resume text contains ATS-unfriendly elements.
    
    Args:
        resume_text (str): The full resume text
        
    Returns:
        bool: True if ATS-unfriendly elements are found, False otherwise
    """
    for pattern in BAD_FORMATTING_PATTERNS:
        if re.search(pattern, resume_text, re.DOTALL):
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
