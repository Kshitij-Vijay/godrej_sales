from spellchecker import SpellChecker

spell = SpellChecker()

def clean_text(raw_text: str) -> str:
    corrected_words = []
    for word in raw_text.split():
        # Correct the word if misspelled, else keep original
        corrected_word = spell.correction(word)
        corrected_words.append(corrected_word if corrected_word else word)
    corrected_text = " ".join(corrected_words)
    return corrected_text
