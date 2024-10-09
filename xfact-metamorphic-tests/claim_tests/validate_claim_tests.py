import random
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('punkt')
from utils import translate_back_to_original, translate_claim

def synonym_replacement(data):
    modified_data = data.copy()
    translated_claim = translate_claim(modified_data["question"])
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
    modified_data["question"] = translate_back_to_original(' '.join(new_claim), 'auto')

    return modified_data

def negate_claim(data):
    modified_data = data.copy()
    translated_claim = translate_claim(modified_data["question"])
    words = nltk.word_tokenize(translated_claim)
    negated_claim = []
    for word in words:
        if word.lower() in ["é", "são", "foi", "foram"]:
            negated_claim.append("não " + word)
        else:
            negated_claim.append(word)
    modified_data["question"] = translate_back_to_original(' '.join(negated_claim), 'auto')

    return modified_data


def remove_non_critical_words(data):
    modified_data = data.copy()
    translated_claim = translate_claim(modified_data["question"])
    words = nltk.word_tokenize(translated_claim)
    non_critical = ["do", "de", "a", "e"]
    new_claim = [word for word in words if word.lower() not in non_critical]
    modified_data["question"] = translate_back_to_original(' '.join(new_claim), 'auto')

    return modified_data

def change_to_question(data):
    modified_data = data.copy()
    modified_data["question"] = translate_back_to_original(translate_claim(modified_data["question"]) + " é verdade?", 'auto')
    
    return modified_data

def validate_claim_tests(data):
    prompt =f"""
        Synonym Replacement: {synonym_replacement(data)},
        Negated Claim: {negate_claim(data)},
        Removed Non-Critical Words": {remove_non_critical_words(data)},
        Changed to Question: {change_to_question(data)},
    """
    return prompt
