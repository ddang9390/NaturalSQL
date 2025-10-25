from NLP.utils import *
from data.db_utils import *

def translate_to_sql(trees, unknown_words, true_vocab, numbers, table=""):
    """
    Translates a natural language sentence into an SQL query for a table

    Arguments:
        trees (list): List of parse trees which represents a sentence in a 
                      tree of grammar nodes
        unknown_words (list): List of words that may be names of values for
                              WHERE clause
        true_vocab (dict): Dictionary containing the vocab from the grammar file
                           that was then extended using the names of the table
                           and columns
        numbers (list): List of numbers that were extracted from the sentence
        table (string): Name of the table

    Return:
        string: The resulting SQL statement if able to translate the sentence
                Else, a blank string
    """
    first_tree = trees[0]

    where_nums, lim_nums = split_numbers_by_context(first_tree, numbers)

    if table == "":
        table = extract_table_from_sentence(first_tree)

    where = build_filter_clause(first_tree, unknown_words, where_nums, table)
    order = build_order_by_clause(first_tree)
    limit = build_limit_clause(first_tree, lim_nums)

    # Starting with identifying SELECT *
    if find_subtree(first_tree, "AllStatement"):
        return f"SELECT * FROM {table}{where}{order}{limit};"
    
    elif find_subtree(first_tree, "ColList"):
        cols = []
        existing = set()
        for col in extract_cols_from_sentence(find_subtree(first_tree, "ColList"), true_vocab):
            if col not in existing:
                existing.add(col)
                cols.append(col)
 
        if len(cols) == 0:
            return ""
        
        cols_str = ", ".join(cols)
        return f"SELECT {cols_str} FROM {table}{where}{order}{limit};"
    elif find_subtree(first_tree, "LimitClause"):
        return f"SELECT * FROM {table}{where}{order}{limit};"
    
    return ""

def build_filter_clause(tree, unknown_words, where_nums, table):
    """
    Builds the WHERE and FOR clauses for the translated
    SQL query

    Argument:
        tree: Parse tree that reporesents a sentence in a tree of grammar nodes
        unknown_words (list): List of unknown words
        where_nums (list): List of numbers that were used in WHERE clauses
        table (string): Name of the table

    Returns:
        where (string): WHERE clause for the SQL query
    """
    filter_node = find_subtree(tree, "FilterStatement")
    where = ""
    if filter_node:
        where = " WHERE "
        word_idx = 0
        num_idx = 0
        for node in filter_node:
            if find_subtree(node, "DetCol"):
                det_col_tree = find_subtree(node, "DetCol")
                col = find_subtree(det_col_tree, "Col")

                if find_subtree(node, "IsVal"):
                    where += "LOWER(" + col.leaves()[0] + ") = '" + (unknown_words[word_idx]) + "'"
                    word_idx+=1
                    
                if find_subtree(node, "IsNum"):
                     where += col.leaves()[0] + " = " + where_nums[num_idx]

            elif find_subtree(node, "Conj"):
                where += " " + node[0].upper() + " "
        if where == " WHERE ":
            where = ""

    return where

def build_order_by_clause(tree):
    """
    Builds the ORDER BY clause for the translated
    SQL query

    Argument:
        tree: Parse tree that reporesents a sentence in a tree of grammar nodes

    Returns:
        order (string): ORDER BY clause for the SQL query
    """
    filter_node = find_subtree(tree, "OrderClause")

    order = ""
    if filter_node:
        order = " ORDER BY "

        if find_subtree(filter_node, "DetCol"):
            det_col_tree = find_subtree(filter_node, "DetCol")
            col = find_subtree(det_col_tree, "Col")

            order += col.leaves()[0]

            dir_node = find_subtree(filter_node, "OrderDir")
            if dir_node:
                dir = dir_node.leaves()[0]
                if dir == "ascending" or dir == "asc":
                    order += " ASC"
                else:
                    order += " DESC"

        else:
            order = ""

    return order

def build_limit_clause(tree, lim_nums):
    """
    Builds the LIMIT clause for the translated
    SQL query

    Argument:
        tree: Parse tree that reporesents a sentence in a tree of grammar nodes
        lim_nums (list): List of numbers that were used in LIMIT clauses

    Returns:
        limit (string): LIMIT clause for the SQL query
    """
    filter_node = find_subtree(tree, "LimitClause")

    limit = ""
    if filter_node:
        num = find_subtree(tree, "NumPlaceholder")
        if num:
            limit = " LIMIT " + (lim_nums[0])
        else:
            limit = " LIMIT 1"


    return limit