NONTERMINALS = """
S -> VP NP | VP NP FilterStatement | FilterStatement | AllStatement 
S -> VP NP OrderClause | VP NP FilterStatement OrderClause | VP NP OrderClause LimitClause | VP NP FilterStatement OrderClause LimitClause  
S -> VP NP FilterStatement LimitClause | VP LimitClause | VP LimitClause OrderClause

NP -> ColList | ColList P TableRef | AllStatement | TableRef 
VP -> V |  V Det | V Det V | V Det Det | V VP

ColList ->  MainCol | MainCol Conj DetCol

# Single columns or columns separated with commas
MainCol -> DetCol | DetCol Punc MainCol | Conj DetCol

# Column with words like 'the' in front of it
DetCol -> Col | Det Col

# Table references
TableRef -> Table | Det Table

AllStatement -> All | All P Det TableRef | All P TableRef | Det All TableRef | VP All | V Det Table | VP All P Det Table | VP Det All Table | Det Table | All TableRef

FilterStatement -> FilterClause | FilterClause Conj FilterClause 
FilterClause -> Filter | Filter NP | Filter DetCol IsVal | DetCol IsVal | Filter DetCol IsNum | DetCol IsNum
IsVal -> V ValPlaceholder
IsNum -> V NumPlaceholder

OrderClause -> Order OrderP DetCol | Order OrderP DetCol OrderDir | Order OrderP DetCol OrderDir  
OrderClause -> Order OrderP DetCol OrderDir Order | Order OrderP DetCol OrderP OrderDir Order | OrderP DetCol

LimitClause -> Limit | Limit NumPlaceholder | Limit TableRef | NumPlaceholder TableRef | Limit NumPlaceholder TableRef
LimitClause -> Det Limit NumPlaceholder TableRef
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
NumPlaceholder -> "__num__"

Order -> "order" | "ordered" | "sort" | "sorted"
OrderDir -> "ascending" | "asc" | "descending" | "desc"
OrderP -> "by" | "from" | "in"

Limit -> "best" | "top" | "worst" | "bottom" | "limit" | "just"
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
        'NumPlaceholder' : ["__num__"],

        'Order': ["order" , "ordered" , "sort", "sorted"],
        'OrderDir' : ["ascending" , "asc" , "descending" , "desc"],
        'OrderP': ["by", "from", "in"],

        'Limit': ["best", "top", "worst", "bottom", "limit", "just"]
}