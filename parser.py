import nltk
import re
import sys

NONTERMINALS = """
S -> VP NP
NP -> ColList | ColList P Table
VP -> V |  V Det
ColList -> Col | Col Conj ColList
"""

TERMINALS = """
Conj -> "and" | "until"
Det -> "a" | "an" | "me" | "my" | "the"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "from"
V -> "show" | "list" | "give" | "what"

Col -> "name" | "year" | "genre" | "director"
Table -> "test_movies"
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def process(sentence):
    # Convert input into list of words
    s = preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()



def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    regex = re.compile('[a-z]')
    sent_parsing = sentence.lower()
    tokens = nltk.word_tokenize(sent_parsing)

    words = []
    for i in range(len(tokens)):
        if regex.match(tokens[i]):
            words.append(tokens[i])

    return words