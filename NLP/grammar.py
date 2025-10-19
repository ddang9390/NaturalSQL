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