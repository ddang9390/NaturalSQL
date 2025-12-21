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
    pattern = r'["\']([^"\']+)["\']'
    unknown_words = re.findall(pattern, sentence)
    processed_sentence = re.sub(pattern, "__value__", sentence)
    
    return processed_sentence, unknown_words


def find_subtree(tree, label):
    """
    Helper function for finding subtrees with given label
    This would help identify what SQL statement the sentence is looking for

    Arguments:
        tree: tree: Parse tree that reporesents a sentence in a tree of grammar nodes
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
        tree: Parse tree that reporesents a sentence in a tree of grammar nodes
        true_vocab (dict): Dictionary containing the vocab from the grammar file
                           that was then extended using the names of the table
                           and columns

    Returns:
        cols (list): List of columns found
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
        tree: Parse tree that reporesents a sentence in a tree of grammar nodes

    Returns:
        table: Name of the table
    """
    table_tree = find_subtree(tree, "Table")
    table = ""
    
    if table_tree:
        table = table_tree.leaves()[0]

    return table


def split_numbers_by_context(tree, numbers):
    """
    Split numbers into WHERE clause numbers and LIMIT clause numbers
    based on their position in the parse tree
    
    Arguments:
        tree: Parse tree that reporesents a sentence in a tree of grammar nodes
        numbers (list): All numbers extracted from query
    
    Returns:
        where_numbers (list): Numbers that were in WHERE clauses
        lim_numbers (list): Number that was in the LIMIT clause
    """
    where_numbers = []
    lim_numbers = []

    if not numbers:
        return where_numbers, lim_numbers

    idx = 0

    for subtree in tree.subtrees():
        if subtree.label() == 'FilterClause':
            for sub in subtree.subtrees():
                if sub.label() == 'IsNum':
                    where_numbers.append(numbers[idx])
                    idx += 1
        if subtree.label() == 'LimitClause':
            lim_numbers.append(numbers[idx])
            idx += 1

    return where_numbers, lim_numbers