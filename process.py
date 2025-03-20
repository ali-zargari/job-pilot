import spacy
import re

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# List of weak phrases that should be replaced with stronger action verbs
WEAK_PHRASES = [
    "responsible for", "worked on", "in charge of", "duties included", "helped with", "assisted in"
]

# List of common ATS-unfriendly elements
BAD_FORMATTING_PATTERNS = [
    r"<img .*?>",  # Detects images
    r"<table.*?>.*?</table>",  # Detects tables
    r"[^\w\s,.!?:;'-]"  # Detects special characters (e.g., emojis, non-standard symbols)
]

# Detects passive voice using auxiliary passive verbs
def check_passive_voice(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == "auxpass":  # Passive voice detected
            return True
    return False

# Detects weak phrases that reduce impact
def check_weak_phrases(sentence):
    for phrase in WEAK_PHRASES:
        if phrase in sentence.lower():
            return phrase
    return None

# Detects missing quantifiable achievements (flags bullet points without numbers)
def check_missing_numbers(sentence):
    if not re.search(r'\d+', sentence):  # No numbers detected
        return True
    return False

# Checks if a sentence is too long (hard to read)
def check_sentence_length(sentence, max_words=20):
    words = sentence.split()
    return len(words) > max_words

# Checks for ATS-unfriendly elements (images, tables, special characters)
def check_ats_friendly(resume_text):
    for pattern in BAD_FORMATTING_PATTERNS:
        if re.search(pattern, resume_text, re.DOTALL):
            return True
    return False

# Main resume analysis function
def analyze_resume(resume_text):
    doc = nlp(resume_text)
    issues = []
    score = 100  # Start with a perfect score

    # Check ATS-unfriendliness
    if check_ats_friendly(resume_text):
        issues.append("❌ Avoid using images, tables, or special characters (ATS may reject them).")
        score -= 10

    # Analyze each sentence in the resume
    for sentence in doc.sents:
        sentence_text = sentence.text.strip()

        # Check for passive voice
        if check_passive_voice(sentence_text):
            issues.append(f"⚠️ Consider rewriting: '{sentence_text}' (Passive voice detected)")
            score -= 5

        # Check for weak phrases
        weak_phrase = check_weak_phrases(sentence_text)
        if weak_phrase:
            issues.append(f"⚠️ Replace '{weak_phrase}' in: '{sentence_text}' (Use action verbs)")
            score -= 5

        # Check for missing numbers
        if check_missing_numbers(sentence_text):
            issues.append(f"⚠️ Consider adding quantifiable achievements in: '{sentence_text}' (Use numbers)")
            score -= 3

        # Check for overly long sentences
        if check_sentence_length(sentence_text):
            issues.append(f"⚠️ This sentence is too long: '{sentence_text}' (Consider making it more concise)")
            score -= 2

    # Final feedback based on score
    if score >= 90:
        issues.append("✅ Your resume is well-structured with minimal issues!")
    elif score >= 75:
        issues.append("⚠️ Your resume is decent but could use improvements in clarity and impact.")
    else:
        issues.append("❌ Your resume has multiple weak points. Consider major improvements.")

    return {"score": score, "issues": issues}

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
for issue in result["issues"]:
    print(issue)
