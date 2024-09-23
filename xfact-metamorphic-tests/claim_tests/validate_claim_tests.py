import random
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('punkt')
from utils import translate_back_to_original, translate_claim

def synonym_replacement(claim):
    translated_claim = translate_claim(claim)
    words = nltk.word_tokenize(translated_claim)
    new_claim = []
    for word in words:
        synsets = wordnet.synsets(word, lang='por')
        if synsets:
            synonyms = synsets[0].lemmas()
            new_word = random.choice(synonyms).name() if synonyms else word
            new_claim.append(new_word)
        else:
            new_claim.append(word)
    return translate_back_to_original(' '.join(new_claim), 'auto')

def negate_claim(claim):
    translated_claim = translate_claim(claim)
    words = nltk.word_tokenize(translated_claim)
    negated_claim = []
    for word in words:
        if word.lower() in ["é", "são", "foi", "foram"]:
            negated_claim.append("não " + word)
        else:
            negated_claim.append(word)
    return translate_back_to_original(' '.join(negated_claim), 'auto')

def remove_non_critical_words(claim):
    translated_claim = translate_claim(claim)
    words = nltk.word_tokenize(translated_claim)
    non_critical = ["do", "de", "a", "e"]
    new_claim = [word for word in words if word.lower() not in non_critical]
    return translate_back_to_original(' '.join(new_claim), 'auto')

def change_to_question(claim):
    return translate_back_to_original(translate_claim(claim) + " é verdade?", 'auto')

def validate_claim_tests(original_claim, expected_outcome):
    tests = {
        "Original Claim": expected_outcome,
        "Synonym Replacement": synonym_replacement(original_claim) == expected_outcome,
        "Negated Claim": negate_claim(original_claim) == (not expected_outcome),
        "Removed Non-Critical Words": remove_non_critical_words(original_claim) == expected_outcome,
        "Changed to Question": change_to_question(original_claim) == expected_outcome,
    }

    return tests
