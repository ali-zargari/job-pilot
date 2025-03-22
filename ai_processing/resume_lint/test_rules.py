import pytest
from . import rules

def test_check_passive_voice():
    # Test active voice sentences
    assert not rules.check_passive_voice("I managed a team of five developers.")
    assert not rules.check_passive_voice("She implemented a new CRM system.")
    
    # Test passive voice sentences
    assert rules.check_passive_voice("The team was managed by me.")
    assert rules.check_passive_voice("The CRM system was implemented by her.")
    
def test_check_weak_phrases():
    # Test sentences with weak phrases
    assert rules.check_weak_phrases("I was responsible for managing the project") == "responsible for"
    assert rules.check_weak_phrases("Worked on developing the application") == "worked on"
    
    # Test sentences without weak phrases
    assert rules.check_weak_phrases("I led the project team") is None
    assert rules.check_weak_phrases("Developed the application") is None
    
def test_check_missing_numbers():
    # Test sentences without numbers
    assert rules.check_missing_numbers("Improved customer satisfaction.")
    assert rules.check_missing_numbers("Managed a team of developers.")
    
    # Test sentences with numbers
    assert not rules.check_missing_numbers("Improved customer satisfaction by 25%.")
    assert not rules.check_missing_numbers("Managed a team of 5 developers.")
    
def test_check_sentence_length():
    # Test sentences that are too short
    assert not rules.check_sentence_length("Short sentence.")
    
    # Test sentences that are exactly at the limit
    twenty_words = "This is a sentence that has exactly twenty words which means it is right at the limit."
    assert not rules.check_sentence_length(twenty_words)
    
    # Test sentences that are too long
    long_sentence = "This is a very long sentence that definitely has more than twenty words and therefore should be flagged as too long because it's hard to read lengthy sentences in a resume context."
    assert rules.check_sentence_length(long_sentence)
    
def test_check_ats_friendly():
    # Test ATS-friendly text
    clean_text = "This is a clean resume with normal text."
    assert not rules.check_ats_friendly(clean_text)
    
    # Test text with images
    image_text = "This resume has an image: <img src='image.jpg'>"
    assert rules.check_ats_friendly(image_text)
    
    # Test text with tables
    table_text = "This resume has a table: <table><tr><td>Data</td></tr></table>"
    assert rules.check_ats_friendly(table_text)
    
    # Test text with emojis
    emoji_text = "This resume has emojis: 📊 📈"
    assert rules.check_ats_friendly(emoji_text)
    
def test_suggest_alternatives():
    # Test suggestions for existing phrases
    assert "managed" in rules.suggest_alternatives("responsible for")
    assert "developed" in rules.suggest_alternatives("worked on")
    
    # Test suggestions for non-existent phrases
    assert rules.suggest_alternatives("some random phrase") == []
    
if __name__ == "__main__":
    # Run all tests
    pytest.main(["-xvs", __file__])
