from googletrans import Translator

def validate_translation(data, question, answer, context, language='pt'):
    """
    Validate translation between Portuguese and English to verify if the results remain consistent.

    Parameters:
        - data (DataFrame): Dataframe.
        - question (str): Provided question.
        - answer (str): Provided answer.
        - context (str): Provided context.
        - language (str): Initial language of the text ('pt' for Portuguese or 'en' for English).

    Returns:
        - True if the translation maintains the same result, False otherwise.
    """
    translator = Translator()
    src_lang, dest_lang = ('pt', 'en') if language == 'pt' else ('en', 'pt')

    translated_question = translator.translate(
        question, src=src_lang, dest=dest_lang).text
    translated_answer = translator.translate(
        answer, src=src_lang, dest=dest_lang).text
    translated_context = translator.translate(
        context, src=src_lang, dest=dest_lang).text

    translated_present = data[
        (data['question'].str.lower() == translated_question.lower()) &
        (data['answer'].str.lower() == translated_answer.lower()) &
        (data['context'].str.contains(translated_context))
    ]

    if not translated_present.empty:
        retrieved_answer = translated_present['answer'].iloc[0]
        if retrieved_answer.lower() != translated_answer.lower():
            print(
                f"The translation found a similar entry in {dest_lang} with a different result.")
            return False

        print(
            f"The translation found a similar entry in {dest_lang} with the same result.")
    return True
