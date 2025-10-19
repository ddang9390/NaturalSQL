import re
from NLP.lemmatizer import find_best_match

def extract_search_value(sentence):
    """
    Extract search value from user input which should
    be in quotation marks

    Argument:
        sentence (string): A sentence written in natural language

    Returns:
        processed_sentence (string): Sentence with search value replaced with placeholder
        unknown_words (list): List of unknown words
    """
    unknown_words = re.findall(r'"(.+?)"', sentence)
    pattern = r'["\']([^"\']+)["\']'
    processed_sentence = re.sub(pattern, "__value__", sentence)

    
    return processed_sentence, unknown_words


def find_subtree(tree, label):
    """
    Helper function for finding subtrees with given label
    This would help identify what SQL statement the sentence is looking for

    Arguments:
        tree: The tree being searched through
        label: The label we are looking for

    Returns:
        subtree: The subtree that contains the label
        None: If no suitable subtree was found
    """
    for subtree in tree.subtrees():
        if subtree.label() == label:
            return subtree
        
    return None

def extract_cols_from_sentence(tree, true_vocab):
    """"
    Helper function for finding columns from a sentence

    Argument:
        tree: Parse tree that reporesentsa sentence in a tree of grammar nodes

    Returns:
        list: List of columns found
    """
    cols = []
    for subtree in tree.subtrees():
        if subtree.label() == 'Col':
            word = subtree.leaves()[0]
            best_match = find_best_match(word, true_vocab["Col"])
            if best_match:
                cols.append(best_match)

    return cols

def extract_table_from_sentence(tree):
    """
    Helper function for finding the table from a sentence

    Argument:
        tree: Parse tree that reporesentsa sentence in a tree of grammar nodes

    Returns:
        table: Name of the table
    """
    table = find_subtree(tree, "Table").leaves()[0]
    return table