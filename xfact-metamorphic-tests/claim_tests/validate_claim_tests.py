import random
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from keybert import KeyBERT
from textblob import TextBlob
from transformers import pipeline

from utils import translate_claim, translate_back_to_original, detect_language

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


question_generator = pipeline(
    "text2text-generation", model="lmsys/fastchat-t5-3b-v1.0", device=0)
negation_generator = pipeline(
    "text2text-generation", model="google/flan-t5-large", device=0)
sentiment_generator = pipeline(
    "text2text-generation", model="declare-lab/flan-alpaca-base", device=0)

LANG = 'portuguese'
STOPWORDS = stopwords.words(LANG)


def synonym_replacement(data):
    kw_model = KeyBERT()
    modified_data = data.copy()
    original_text = modified_data["question"]
    source_lang = detect_language(original_text)
    translated = translate_claim(original_text)

    keywords = kw_model.extract_keywords(
        translated, keyphrase_ngram_range=(1, 1), stop_words=LANG, top_n=3)
    keyword_list = [kw[0].lower() for kw in keywords]
    words = word_tokenize(translated)

    new_claim = []
    for word in words:
        if word.lower() in keyword_list:
            synsets = wordnet.synsets(word, lang='eng')
            if synsets:
                synonyms = synsets[0].lemmas()
                new_word = random.choice(synonyms).name() if synonyms else word
                new_claim.append(new_word)
            else:
                new_claim.append(word)
        else:
            new_claim.append(word)

    modified_data["question"] = translate_back_to_original(
        " ".join(new_claim), source_lang)
    return modified_data


def remove_non_critical_words(data):
    modified_data = data.copy()
    original_text = modified_data["question"]
    lang = detect_language(original_text)
    translated = translate_claim(
        original_text) if lang != 'pt' else original_text

    words = word_tokenize(translated)
    filtered = [w for w in words if w.lower() not in STOPWORDS]
    modified_data["question"] = translate_back_to_original(
        " ".join(filtered), lang)
    return modified_data


def fallback_negate(text):
    words = word_tokenize(text)
    negated = []
    inserted = False
    for i, word in enumerate(words):
        if not inserted and word.lower() in ["é", "são", "foi", "foram", "está", "estavam"]:
            if i == 0 or words[i - 1].lower() != "não":
                negated.append("não")
                inserted = True
        negated.append(word)
    return " ".join(negated)


def negate_claim(data):
    modified_data = data.copy()
    original_text = modified_data["question"]
    lang = detect_language(original_text)
    translated = translate_claim(
        original_text) if lang != 'pt' else original_text

    try:
        prompt = f"Negate the sentence: {translated}"
        result = negation_generator(prompt, max_length=64, do_sample=False)[
            0]['generated_text']
        modified_data["question"] = translate_back_to_original(result, lang)

    except Exception as e:
        print(f"[Fallback] negate_claim(): {e}")
        result = fallback_negate(original_text)
        modified_data["question"] = result
    return modified_data


def fallback_question(text, lang):
    if lang == 'pt':
        return f"{text}?"
    elif lang == 'en':
        return f"{text}. Is that true?"
    else:
        return f"{text} ?"


def change_to_question(data):
    modified_data = data.copy()
    original_text = modified_data["question"]
    lang = detect_language(original_text)
    translated = translate_claim(
        original_text) if lang != 'pt' else original_text

    try:
        prompt = f"Turn the following statement into a yes/no question: {translated}"
        result = question_generator(prompt, max_length=64, do_sample=False)[
            0]['generated_text']
        modified_data["question"] = translate_back_to_original(result, lang)

    except Exception as e:
        print(f"[Fallback] change_to_question(): {e}")
        result = fallback_question(original_text, lang)
        modified_data["question"] = result
    return modified_data


def fallback_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    prefix = "Unfortunately, " if polarity >= 0 else "Fortunately, "
    return prefix + text


def sentiment_shift(data):
    modified_data = data.copy()
    original_text = modified_data["question"]
    lang = detect_language(original_text)
    translated = translate_claim(
        original_text) if lang != 'en' else original_text

    try:
        prompt = f"Rewrite the sentence with stronger emotional tone: {translated}"
        result = sentiment_generator(prompt, max_length=64, do_sample=False)[
            0]['generated_text']
    except Exception as e:
        print(f"[Fallback] sentiment_shift(): {e}")
        result = fallback_sentiment(translated)

    modified_data["question"] = translate_back_to_original(result, lang)
    return modified_data
