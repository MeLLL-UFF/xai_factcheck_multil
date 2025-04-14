from googletrans import Translator
from langdetect import detect

translator = Translator()

def translate_claim(claim, dest_lang='pt'):
    return translator.translate(claim, dest=dest_lang).text

def translate_back_to_original(claim, original_lang):
    return translator.translate(claim, dest=original_lang).text

def detect_language(text):
    try:
        return detect(text)
    except:
        return 'pt'
