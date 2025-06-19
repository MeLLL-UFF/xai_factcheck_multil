from langdetect import detect
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
CACHE_DIR = "./hf_cache" 

def ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def _load_tokenizer_and_model():
    ensure_cache_dir()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME, cache_dir=CACHE_DIR)
    return tokenizer, model


_tokenizer, _model = _load_tokenizer_and_model()

_lang_map = {
    'pt': 'pt_XX',
    'en': 'en_XX',
}


def _get_mbart_lang_code(lang_code):
    return _lang_map.get(lang_code[:2], 'en_XX')


def _translate_mbart(text, src_lang_code, tgt_lang_code):
    _tokenizer.src_lang = src_lang_code
    encoded = _tokenizer(text, return_tensors="pt",
                         max_length=1024, truncation=True)
    generated_tokens = _model.generate(
        **encoded,
        forced_bos_token_id=_tokenizer.lang_code_to_id[tgt_lang_code],
        max_length=1024,
        num_beams=5,
        early_stopping=True
    )
    return _tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]


def translate_claim(text, dest_lang):
    src_lang = detect_language(text)
    dest_lang = dest_lang or 'pt'
    src_code = _get_mbart_lang_code(src_lang)
    tgt_code = _get_mbart_lang_code(dest_lang)
    if src_code == tgt_code:
        return text
    return _translate_mbart(text, src_code, tgt_code)


def translate_back_to_original(text, original_lang):
    src_code = _get_mbart_lang_code('en')
    tgt_code = _get_mbart_lang_code(original_lang)
    if src_code == tgt_code:
        return text
    return _translate_mbart(text, src_code, tgt_code)


def detect_language(text):
    try:
        lang = detect(text)
        return lang
    except:
        return 'pt'
