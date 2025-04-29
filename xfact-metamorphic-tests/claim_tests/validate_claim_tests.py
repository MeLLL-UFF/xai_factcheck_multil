import random
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from keybert import KeyBERT
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

from utils import translate_claim, translate_back_to_original, detect_language

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

tokenizer = AutoTokenizer.from_pretrained(
    "unicamp-dl/ptt5-base-portuguese-vocab")
model = AutoModelForSeq2SeqLM.from_pretrained(
    "unicamp-dl/ptt5-base-portuguese-vocab")
question_generator = pipeline(
    "text2text-generation", model="lmsys/fastchat-t5-3b-v1.0", device=0)
negation_generator = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0
)
sentiment_generator = pipeline(
    "text2text-generation", model="declare-lab/flan-alpaca-base", device=0)

LANG = 'portuguese'
STOPWORDS = stopwords.words(LANG)


def synonym_replacement(data):
    kw_model = KeyBERT()
    modified_data = data.copy()
    original_text = modified_data["question"]
    keywords = kw_model.extract_keywords(
        original_text, keyphrase_ngram_range=(1, 1), stop_words=LANG, top_n=3)
    keyword_list = [kw[0].lower() for kw in keywords]
    words = word_tokenize(original_text)

    new_claim = []
    for word in words:
        if word.lower() in keyword_list:
            synsets = wordnet.synsets(word)
            if synsets:
                synonyms = synsets[0].lemmas()
                new_word = random.choice(synonyms).name() if synonyms else word
                new_claim.append(new_word)
            else:
                new_claim.append(word)
        else:
            new_claim.append(word)

    modified_data["question"] = " ".join(new_claim)
    return modified_data


def remove_non_critical_words(data):
    modified_data = data.copy()
    original_text = modified_data["question"]

    words = word_tokenize(original_text)
    filtered = [w for w in words if w.lower() not in STOPWORDS]
    modified_data["question"] = " ".join(filtered)
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
        prompt = f"Negue a seguinte frase: {translated}"
        result = negation_generator(prompt, max_length=64, do_sample=False)[
            0]['generated_text']
        modified_data["question"] = translate_back_to_original(result, lang)

    except Exception as e:
        print(f"[Fallback] negate_claim(): {e}")
        result = fallback_negate(original_text)
        modified_data["question"] = result
    return modified_data


def fallback_question(text):
    return f"{text} ?"


def change_to_question(data):
    modified_data = data.copy()
    original_text = modified_data["question"]
    try:
        prompt = f"Transforme o texto em pergunta: {original_text}"
        result = question_generator(prompt, max_length=64, do_sample=False)[
            0]['generated_text']
        modified_data["question"] = result

    except Exception as e:
        print(f"[Fallback] change_to_question(): {e}")
        result = fallback_question(original_text)
        modified_data["question"] = result
    return modified_data


def fallback_sentiment(text):
    negative_words = ["não", "nunca", "jamais",
                      "ruim", "péssimo", "horrível", "mal", "triste"]
    positive_words = ["bom", "ótimo", "excelente",
                      "feliz", "alegre", "maravilhoso", "bem"]

    words = text.lower().split()

    neg_count = sum(1 for word in words if word in negative_words)
    pos_count = sum(1 for word in words if word in positive_words)

    if pos_count > neg_count:
        return "Infelizmente, " + text
    else:
        return "Felizmente, " + text


def sentiment_shift(data):
    modified_data = data.copy()
    original_text = modified_data["question"]

    try:
        prompt = f"Reescreva a frase com um tom emocional oposto: {original_text}"
        result = sentiment_generator(
            prompt, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']

    except Exception as e:
        print(f"[Fallback] sentiment_shift(): {e}")
        result = fallback_sentiment(original_text)

    modified_data["question"] = result
    return modified_data
