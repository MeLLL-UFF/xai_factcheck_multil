import nlpaug.augmenter.word as naw
import nlpaug.augmenter.sentence as nas
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from ..utils import translate_claim, translate_back_to_original, detect_language


synonym_aug_en = naw.SynonymAug(aug_src='wordnet', lang='eng')
synonym_aug_pt = naw.SynonymAug(aug_src='wordnet', lang='por')
contextual_aug = naw.ContextualWordEmbsAug(
    model_path='bert-base-multilingual-cased', action='substitute')


def back_translate(text, src_lang=None):
    from langdetect import detect
    if not src_lang:
        src_lang = detect(text)
    pivot_lang = 'en' if src_lang == 'pt' else 'pt'
    translated = translate_claim(text, dest=pivot_lang).text
    back_translated = translate_back_to_original(
        translated, dest=src_lang).text
    return back_translated


def synonym_replacement(data):
    modified_data = data.copy()
    text = modified_data["claim"]
    lang = detect_language(text)

    if lang == 'pt':
        aug = synonym_aug_pt
        augmented = aug.augment(text)
    elif lang == 'en':
        aug = synonym_aug_en
        augmented = aug.augment(text)
    else:
        text_en = translate_claim(text, dest_lang='en')
        augmented_en = synonym_aug_en.augment(text_en)
        if isinstance(augmented_en, list):
            augmented_en = augmented_en[0]
        augmented = translate_back_to_original(augmented_en, lang)

    modified_data["claim"] = augmented
    return modified_data


def remove_non_critical_words(data):
    modified_data = data.copy()
    text = modified_data["claim"]
    lang = detect_language(text)

    try:
        stopwords_list = stopwords.words(lang)
    except:
        stopwords_list = stopwords.words('portuguese')

    words = word_tokenize(text)
    filtered = [w for w in words if w.lower() not in stopwords_list]
    modified_data["claim"] = " ".join(filtered)
    return modified_data


def negate_claim(data):
    modified_data = data.copy()
    text = modified_data["claim"]
    lang = detect_language(text)

    if lang != 'en':
        text_en = translate_claim(text, dest_lang='en')
    else:
        text_en = text

    augmented_en = contextual_aug.augment(f'not {text_en}')
    if isinstance(augmented_en, list):
        augmented_en = augmented_en[0]
    augmented = translate_back_to_original(
        augmented_en, lang) if lang != 'en' else augmented_en

    modified_data["claim"] = augmented
    return modified_data


def change_to_question(data):
    modified_data = data.copy()
    text = modified_data["claim"]
    question = f"{text.strip().rstrip('.')}" + "?"
    modified_data["claim"] = question
    return modified_data


def sentiment_shift(data):
    modified_data = data.copy()
    text = modified_data["claim"]
    lang = detect_language(text)

    if lang != 'en':
        text_en = translate_claim(text, dest_lang='en')
    else:
        text_en = text

    augmented_en = contextual_aug.augment(text_en)
    if isinstance(augmented_en, list):
        augmented_en = augmented_en[0]
    augmented = translate_back_to_original(
        augmented_en, lang) if lang != 'en' else augmented_en

    modified_data["claim"] = augmented
    return modified_data
