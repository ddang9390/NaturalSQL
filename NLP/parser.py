import nltk
from NLP.lemmatizer import *
from NLP.grammar import *
from NLP.sql_translator import *

def init_parser():
    """
    Initiates the parser so that it can handle our current static grammar
    along with dynamic table and column names

    Returns:
        parser
    """
    column_names, table_names = get_column_and_tablenames()

    col_rules = "Col -> " + " | ".join(f'"{col}"' for col in column_names) + "\n"
    table_rules = "Table -> " + " | ".join(f'"{table}"' for table in table_names) + ' | "table" | "data"\n'

    true_terminals = TERMINALS + "\n" + col_rules + "\n" + table_rules

    grammar = nltk.CFG.fromstring(NONTERMINALS + true_terminals)
    parser = nltk.ChartParser(grammar)

    return parser

def process(sentence, parser, table=""):
    """
    Take a sentence and processes it to be able to be
    translated into an SQL query

    Arguments:
        sentence (string): Natural language sentence from user
        parser (ChartParser): Parser that will be parsing the sentence 
        table (string): Name of the table being queried

    Returns:
        string: Either a valid SQL query
                or an empty string if the sentence could not be 
                parsed or translated properly
    """
    # Convert input into list of words
    s, unknown_words, true_vocab, numbers = preprocess(sentence)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))

    except ValueError as e:
        print(e)
        return ""
    if not trees:
        print("Could not parse sentence.")
        return ""

    return translate_to_sql(trees, unknown_words, true_vocab, numbers, table)



def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and matching similar looking words to what is in our grammar.
    Unidentified words are replaced with placeholders
    
    Arguments:
        sentence (string): A sentence written in natural language

    Returns:
        processed_tokens (list): List of words in preprocessed sentence
        unknown_words (list): List of unknown words
        true_vocab (dict): Dictionary containing the vocab from the grammar file
                           that was then extended using the names of the table
                           and columns
        numbers (list): List of numbers that were extracted from the sentence
    """
    sent_parsing, unknown_words = extract_search_value(sentence.lower())
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

    numbers = []
    for token in resolved_tokens:
        if token in known_words:
            processed_tokens.append(token)
        elif token.isnumeric():
            numbers.append(token)
            processed_tokens.append("__num__")
        else:
            processed_tokens.append("__value__")
            unknown_words.append(token)

    return processed_tokens, unknown_words, true_vocab, numbers










