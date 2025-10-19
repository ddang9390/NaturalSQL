from NLP.utils import *
from data.db_utils import *

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


    return where