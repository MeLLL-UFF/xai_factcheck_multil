import random
import re

def alter_text(text, old_word, new_word, alteration_choice='all', num_words=1):
    """
    Alters specific words in a text based on the user's choice.
    Parameters:
        - text (str): The original text.
        - old_word (str): The word to be replaced.
        - new_word (str): The new word.
        - alteration_choice (str): Choice to determine how the alteration should be performed.
            - 'all': Alters all occurrences of the word.
            - 'random': Alters a random occurrence of the word.
            - 'set': Alters a specific set of words.
        - num_words (int): The number of words to be altered when 'alteration_choice' is 'set'.

    Returns:
        - The altered text.
    """
    words_to_alter = re.finditer(r'\b' + re.escape(old_word) + r'\b', text)
    words_positions = [match.start() for match in words_to_alter]
    
    if not words_positions:
        print(" No occurrences of the word were found")
        return text
    if alteration_choice == 'all':
        for pos in reversed(words_positions):
            text = text[:pos] + new_word + text[pos + len(old_word):]
    
    elif alteration_choice == 'random':
        pos = random.choice(words_positions)
        text = text[:pos] + new_word + text[pos + len(old_word):]
    
    elif alteration_choice == 'set':
        num_words = min(num_words, len(words_positions))
        positions_to_alter = random.sample(words_positions, num_words)
        for pos in sorted(positions_to_alter, reverse=True):
            text = text[:pos] + new_word + text[pos + len(old_word):]
    
    return text

def validate_similar_word_change(data, question, answer, context, similar_word):
    """
    Validates the change of similar words in text.

    Parameters:
        - data (DataFrame): Dataframe.
        - question (str): Provided question.
        - answer (str): Provided answer.
        - context (str): Provided context.
        - similar_word (dict): Dictionary containing the configuration for changing the words.

    Returns:
        - True if the change of similar words does not result in a change in the outcomes; False otherwise.
    """
    old_word = similar_word['old_word']
    new_word = similar_word['new_word']
    alteration_choice = similar_word['alteration_choice']
    num_words = similar_word.get('num_words', 1)
    
    altered_context = alter_text(context, old_word, new_word, alteration_choice, num_words)
    altered_question = question.replace(old_word, new_word)
    
    filtered_data = data[
        (data['question'] == altered_question) & (data['context'] == altered_context)
    ]
    
    if not filtered_data.empty:
        for _, row in filtered_data.iterrows():
            if row['answer'] != answer:
                print(f"Detected a change in similar words from '{old_word}' to '{new_word}'.")
                print(f"The model's outcome has changed from '{answer}' to '{row['answer']}'.")
                return False
        
    print("Validation of similar word changes was successful.")
    return True