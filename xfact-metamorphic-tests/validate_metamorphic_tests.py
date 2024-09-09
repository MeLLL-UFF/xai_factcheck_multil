from validate_authority_chage import validate_authority_change
from validate_parameter_change import validate_parameter_change
from validate_similar_word_change import validate_similar_word_change
from validate_translation import validate_translation


def validate_truthfulness(data, question, answer, context, alteration=None, language='pt', authority_change=None, similar_word=None):
    """
    Main function to validate the truthfulness of a text based on X-FACT.

    Parameters:
        - data (pd.DataFrame): X-FACT dataset containing questions, answers, and context.
        - question (str): Original question.
        - answer (str): Original answer.
        - context (str): Original context.
        - alteration (dict): Dictionary containing the alteration to be made (optional).
        - language (str): Desired language ('pt' for Portuguese or 'en' for English).
        - authority_change (dict): Dictionary containing the change of authority or entity (optional).
        - similar_word (dict): Dictionary containing settings for similar word alterations (optional).

    Returns:
        - True if all tests are successful, False otherwise.
    """
    if alteration and not validate_parameter_change(data, question, answer, context, alteration):
        return False

    if language == 'en' and not validate_translation(data, question, answer, context, language):
        return False
    elif language == 'pt' and not validate_translation(data, question, answer, context, language):
        return False

    if authority_change and not validate_authority_change(data, question, context, authority_change):
        return False

    if similar_word and not validate_similar_word_change(data, question, answer, context, similar_word):
        return False

    print("All the tests were sucessfull.")
    return True
