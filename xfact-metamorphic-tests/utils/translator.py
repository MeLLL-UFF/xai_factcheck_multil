from deep_translator import GoogleTranslator
from langdetect import detect


def translate_claim(claim, dest_lang='pt'):
    return GoogleTranslator(source='auto', target=dest_lang).translate(claim)


def translate_back_to_original(claim, original_lang):
    return GoogleTranslator(source='auto', target=original_lang).translate(claim)

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'pt'
