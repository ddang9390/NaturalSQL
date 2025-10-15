import nltk
from utils import *

NONTERMINALS = """
S -> VP NP | VP NP FilterClause | FilterClause
NP -> ColList | ColList P Table | AllStatement
VP -> V |  V Det | V Det V


ColList ->  MainCol | MainCol Conj DetCol

# Single columns or columns separated with commas
MainCol -> DetCol | DetCol Punc MainCol | Conj DetCol

# Column with words like 'the' in front of it
DetCol -> Col | Det Col

AllStatement -> All | All P Det Table | All P Table | Det All Table | VP All

FilterClause -> Filter | Filter NP | Filter DetCol IsVal
IsVal -> V ValPlaceholder
"""

TERMINALS = """
Conj -> "and" | "until"
Punc -> ","
Det -> "a" | "an" | "me" | "my" | "the" | "are" 
P -> "at" | "before" | "in" | "of" | "on" | "to" | "from"
V -> "show" | "list" | "give" | "what" | "let" | "see" | "who" | "is"

Col -> "name" | "year" | "genre" | "director"
Table -> "movie" | "table" | "data"

All -> "everything" | "all" | "entire"
Filter -> "where" | "with" | "for"

ValPlaceholder -> "__value__"
"""

# For lemmatization purposes
VALID_VOCABULARY = {
        'V': ["show", "list", "give", "what", "let", "see", "who", "is"],
        'Det': ["a", "an", "me", "my", "the", "are"],
        'P': ["at", "before", "in", "of", "on", "to", "from"],
        'Conj': ["and", "until"],
        'Punc': [","],
        'Col': ["name", "year", "genre", "director"],
        'Table': ["movie", "table", "data"],
        'All': ["everything", "all", "entire"],
        'Filter' : ["where", "with", "for"],
        'ValPlaceholder' : ["__value__"],
}


grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def process(sentence, table):
    """
    Take a sentence and processes it to be able to be
    translated into an SQL query

    Arguments:
        sentence (string): Natural language sentence from user
        table (string): Name of the table being queried

    Returns:
        string: Either a valid SQL query
                or an empty string if the sentence could not be 
                parsed or translated properly
    """
    # Convert input into list of words
    s, unknown_words = preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))

    except ValueError as e:
        print(e)
        return ""
    if not trees:
        print("Could not parse sentence.")
        return ""

    return translate_to_sql(table, trees, unknown_words)



def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.

    Arguments:
        sentence (string): A sentence written in natural language

    Returns:
        processed_tokens (list): List of words in preprocessed sentence
        unknown_words (list): List of unknown words
    """
    sent_parsing = sentence.lower()
    tokens = nltk.word_tokenize(sent_parsing)

    # Converting unknown words
    known_words = set()
    for valid in VALID_VOCABULARY.values():
        known_words.update(valid)

    

    lemmatized_tokens = [lemmatize_word(token) for token in tokens]
    resolved_tokens = resolve_tokens(lemmatized_tokens, VALID_VOCABULARY)

    
    processed_tokens = []
    unknown_words = []
    for token in resolved_tokens:
        if token in known_words:
            processed_tokens.append(token)
        else:
            processed_tokens.append("__value__")
            unknown_words.append(token)

    return processed_tokens, unknown_words

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

def extract_cols_from_sentence(tree):
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
            best_match = find_best_match(word, VALID_VOCABULARY["Col"])
            if best_match:
                cols.append(best_match)

    return cols


def translate_to_sql(table, trees, unknown_words):
    """
    Translates a natural language sentence into an SQL query for a table

    Arguments:
        table (string): Name of the table being queried
        trees (list): List of parse trees which represents a sentence in a 
                      tree of grammar nodes
        unknown_words (list): List of words that may be names of values for
                              WHERE clause

    Return:
        string: The resulting SQL statement if able to translate the sentence
                Else, a blank string
    """
    first_tree = trees[0]
    
    # Starting with identifying SELECT *
    if find_subtree(first_tree, "AllStatement"):
        return f"SELECT * FROM {table};"
    
    elif find_subtree(first_tree, "ColList"):
        cols = []
        existing = set()
        for col in extract_cols_from_sentence(first_tree):
            if col not in existing:
                existing.add(col)
                cols.append(col)
 
        if len(cols) == 0:
            return ""
        
        # Identifies WHERE clause
        filter_node = find_subtree(first_tree, "FilterClause")
        where = ""
        if filter_node:
            where = build_filter_clause(filter_node, unknown_words)

        cols_str = ", ".join(cols)
        return f"SELECT {cols_str} FROM {table}{where};"
    
    return ""

def build_filter_clause(tree, unknown_words):
    """
    Builds the WHERE and FOR clauses for the translated
    SQL query

    Argument:
        tree: Parse tree that reporesentsa sentence in a tree of grammar nodes
        unknown_wards (list): List of unknown words

    Returns:
        where_clause (string): WHERE clause for the SQL query
    """
    where_clause = ""
    if find_subtree(tree, "Filter"):
        det_col_tree = find_subtree(tree, "DetCol")
        col = find_subtree(det_col_tree, "Col")
        where_clause = " WHERE LOWER(" + col.leaves()[0] + ") = '" + unknown_words[0] + "'"
            

    return where_clause