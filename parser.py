import nltk
import re
import sys

NONTERMINALS = """
S -> VP NP 
NP -> ColList | ColList P Table | AllStatement
VP -> V |  V Det
ColList -> Col | Col Conj ColList

AllStatement -> All | All P Det Table | All P Table | Det All Table | VP All
"""

TERMINALS = """
Conj -> "and" | "until"
Det -> "a" | "an" | "me" | "my" | "the"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "from"
V -> "show" | "list" | "give" | "what" | "let" | "see"

Col -> "name" | "year" | "genre" | "director"
Table -> "movies" | "table" | "data"

All -> "everything" | "all" | "entire"
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def process(sentence, table):
    # Convert input into list of words
    s = preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return ""
    if not trees:
        print("Could not parse sentence.")
        return ""

    return translate_to_sql(table, trees)



def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.

    Arguments:
        sentence (string): A sentence written in natural language

    Returns:
        list: List of words in preprocessed sentence
    """
    sent_parsing = sentence.lower()
    tokens = nltk.word_tokenize(sent_parsing)

    return tokens

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

def translate_to_sql(table, trees):
    """
    Translates a natural language sentence into an SQL query for a table

    Arguments:
        table (string): Name of the table being queried
        trees (list): List of parse trees which represents a sentence in a 
                      tree of grammar nodes

    Return:
        string: The resulting SQL statement if able to translate the sentence
                Else, a blank string
    """
    first_tree = trees[0]

    # Starting with identifying SELECT *
    if find_subtree(first_tree, "AllStatement"):
        return f"SELECT * FROM {table}"
    
    return ""