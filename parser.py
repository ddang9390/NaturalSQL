import nltk
import re
from utils import *
from database import *

NONTERMINALS = """
S -> VP NP | VP NP FilterStatement | FilterStatement | AllStatement
NP -> ColList | ColList P TableRef | AllStatement | TableRef 
VP -> V |  V Det | V Det V

ColList ->  MainCol | MainCol Conj DetCol

# Single columns or columns separated with commas
MainCol -> DetCol | DetCol Punc MainCol | Conj DetCol

# Column with words like 'the' in front of it
DetCol -> Col | Det Col

# Table references
TableRef -> Table | Det Table

AllStatement -> All | All P Det TableRef | All P TableRef | Det All TableRef | VP All | V Det Table | VP All P Det Table | VP Det All Table | Det Table

FilterStatement -> FilterClause | FilterClause Conj FilterClause 
FilterClause -> Filter | Filter NP | Filter DetCol IsVal | DetCol IsVal
IsVal -> V ValPlaceholder
"""

TERMINALS = """
Conj -> "and" | "until" | "or"
Punc -> ","
Det -> "a" | "an" | "me" | "my" | "the" | "are" 
P -> "at" | "before" | "in" | "of" | "on" | "to" | "from"
V -> "show" | "list" | "give" | "what" | "let" | "see" | "who" | "is"

All -> "everything" | "all" | "entire"
Filter -> "where" | "with" | "for"

ValPlaceholder -> "__value__"
"""

# For lemmatization purposes
VALID_VOCABULARY = {
        'V': ["show", "list", "give", "what", "let", "see", "who", "is"],
        'Det': ["a", "an", "me", "my", "the", "are"],
        'P': ["at", "before", "in", "of", "on", "to", "from"],
        'Conj': ["and", "until", "or"],
        'Punc': [","],

        'All': ["everything", "all", "entire"],
        'Filter' : ["where", "with", "for"],
        'ValPlaceholder' : ["__value__"],
}



def init_parser():
    """
    Initiates the parser so that it can handle our current static grammar
    along with dynamic table and column names

    Returns:
        grammar
        parser
    """
    column_names, table_names = get_column_and_tablenames()

    col_rules = "Col -> " + " | ".join(f'"{col}"' for col in column_names) + "\n"
    table_rules = "Table -> " + " | ".join(f'"{table}"' for table in table_names) + ' | "table" | "data"\n'

    true_terminals = TERMINALS + "\n" + col_rules + "\n" + table_rules

    grammar = nltk.CFG.fromstring(NONTERMINALS + true_terminals)
    parser = nltk.ChartParser(grammar)

    return parser

def process(sentence, table=""):
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
    parser = init_parser()

    # Convert input into list of words
    s, unknown_words, true_vocab = preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))

    except ValueError as e:
        print(e)
        return ""
    if not trees:
        print("Could not parse sentence.")
        return ""

    return translate_to_sql(trees, unknown_words, true_vocab, table)

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
    sent_parsing, unknown_words = extract_search_value(sentence.lower())
    # sent_parsing = sentence.lower()
    tokens = nltk.word_tokenize(sent_parsing)

    column_names, table_names = get_column_and_tablenames()
    true_vocab = VALID_VOCABULARY.copy()
    true_vocab["Table"] = table_names
    true_vocab["Col"] = column_names
    true_vocab["Table"].extend(["table", "data"])

    # Converting unknown words
    known_words = set()
    for valid in true_vocab.values():
        known_words.update(valid)

    lemmatized_tokens = [lemmatize_word(token) for token in tokens]
    resolved_tokens = resolve_tokens(lemmatized_tokens, true_vocab)
    
    processed_tokens = []

    for token in resolved_tokens:
        if token in known_words:
            processed_tokens.append(token)
        else:
            processed_tokens.append("__value__")
            unknown_words.append(token)

    return processed_tokens, unknown_words, true_vocab











#TODO - separate into separate translator file
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

def translate_to_sql(trees, unknown_words, true_vocab, table=""):
    """
    Translates a natural language sentence into an SQL query for a table

    Arguments:
        trees (list): List of parse trees which represents a sentence in a 
                      tree of grammar nodes
        unknown_words (list): List of words that may be names of values for
                              WHERE clause

    Return:
        string: The resulting SQL statement if able to translate the sentence
                Else, a blank string
    """
    first_tree = trees[0]

    if table == "":
        table = extract_table_from_sentence(first_tree)
    where = build_filter_clause(first_tree, unknown_words, table)
    # Starting with identifying SELECT *
    if find_subtree(first_tree, "AllStatement"):
        return f"SELECT * FROM {table}{where};"
    
    elif find_subtree(first_tree, "ColList"):
        cols = []
        existing = set()
        for col in extract_cols_from_sentence(first_tree, true_vocab):
            if col not in existing:
                existing.add(col)
                cols.append(col)
 
        if len(cols) == 0:
            return ""
        
        cols_str = ", ".join(cols)
        return f"SELECT {cols_str} FROM {table}{where};"
    
    return ""

def build_filter_clause(tree, unknown_words, table):
    """
    Builds the WHERE and FOR clauses for the translated
    SQL query

    tree: Parse tree that reporesents a sentence in a tree of grammar nodes
        unknown_words (list): List of unknown words

    Returns:
        where_clause (string): WHERE clause for the SQL query
    """
    filter_node = find_subtree(tree, "FilterStatement")

    where = ""
    if filter_node:
        where = " WHERE "
        idx = 0
        for node in filter_node:
            if find_subtree(node, "DetCol"):
                det_col_tree = find_subtree(node, "DetCol")
                col = find_subtree(det_col_tree, "Col")

                column_info = get_column_types(table)

                if column_is_number(column_info[col.leaves()[0]]):
                    where += col.leaves()[0] + " = " + unknown_words[idx]
                else:
                    where += "LOWER(" + col.leaves()[0] + ") = '" + (unknown_words[idx]) + "'"
                idx+=1

            elif find_subtree(node, "Conj"):
                where += " " + node[0].upper() + " "

        # if find_subtree(filter_node, "Filter"):
        #     det_col_tree = find_subtree(tree, "DetCol")
        #     col = find_subtree(det_col_tree, "Col")

        #     column_info = get_column_types(table)

        #     if column_is_number(column_info[col.leaves()[0]]):
        #         where = " WHERE " + col.leaves()[0] + " = " + unknown_words[0]
        #     else:
        #         where = " WHERE LOWER(" + col.leaves()[0] + ") = '" + " ".join(unknown_words) + "'"

    return where

