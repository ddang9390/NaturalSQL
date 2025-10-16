import nltk
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer

SIMILARITY_THRESHOLD = 80

def find_best_match(word, valid_words):
    """
    Find the best matching word through lemmatization and fuzzywuzzy.
    We attempt to see if a given word resembles one of the valid words
    by trying to handle misspellings.

    The fuzz ratio that would be used is a ratio that calculates the
    similarity between two inputs.

    Arguments:
        word (string): The word that we are looking the best matching word for
        valid_words (list): List of valid words

    Returns:
        string: The word that closely resembles the inputted word
    """
    best_match = None
    best_score = SIMILARITY_THRESHOLD
    
    for item in valid_words:
        original_score = fuzz.ratio(word.lower(), item.lower())
        if original_score > best_score:
            best_score = original_score
            best_match = item
    
    return best_match


def lemmatize_word(word):
    """
    Helper function for lemmatization allowing for usage
    outside of this file

    Argument:
        word (string): Word to lemmatize
    
    Returns:
        string: Word converted to singular form
    """
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize(word)

def resolve_tokens(tokens, valid_vocabulary):
    """
    Takes a list of user tokens and resolves them against a known vocabulary.

    Args:
        tokens (list): A list of words from the user.
        valid_vocabulary (dict): A dictionary categorizing known words.
    
    Returns:
        list: A new list of tokens where words have been corrected.
    """
    resolved_tokens = []

    # Convert valid vocabulary dictionary to single set for use in find_best_match function
    known_grammar_words = set(
        valid_vocabulary.get('V', []) + 
        valid_vocabulary.get('Det', []) + 
        valid_vocabulary.get('P', []) + 
        valid_vocabulary.get('Conj', []) +
        valid_vocabulary.get('Punc', []) +
        valid_vocabulary.get('Col', []) +
        valid_vocabulary.get('Table', []) +
        valid_vocabulary.get('All', []) +
        valid_vocabulary.get('Filter', []) +
        valid_vocabulary.get('ValPlaceholder', [])
    )

    for token in tokens:
        if token in known_grammar_words:
            resolved_tokens.append(token)

        else:
            best_match = find_best_match(token, known_grammar_words)
            if best_match:
                resolved_tokens.append(best_match)
            else:
                resolved_tokens.append(token)
    
    return resolved_tokens