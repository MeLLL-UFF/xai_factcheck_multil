

from googletrans import Translator

translator = Translator()

def translate_claim(claim, dest_lang='pt'):
    return translator.translate(claim, dest=dest_lang).text

def translate_back_to_original(claim, original_lang):
    return translator.translate(claim, dest=original_lang).text