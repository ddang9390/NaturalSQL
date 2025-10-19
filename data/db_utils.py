import sqlite3
from data.database import DB_PATH

def get_column_and_tablenames():
    """
    Retrieve the names of all tables and columns from the database

    Returns:
        column_names (list): List of all column names
        table_names (list): List of all table names
    """
    schema = get_schema_info()
    column_names = set()
    table_names = set(schema.keys())

    for table in schema.items():
        for col in table[1]:
            column_names.add(col)

    return list(column_names), list(table_names)


def get_column_types(table):
    """
    Retrieves the types of the columns in the table

    Argument:
        table (String): name of the table

    Returns:
        dict: Dictionary mapping column names to their types
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    column_types = {}

    cur.execute(f"PRAGMA table_info({table})")
    column_info = cur.fetchall()
    for col_info in column_info:
        column_types[col_info[1]] = col_info[2].upper()

    con.close()
    return column_types

def column_is_number(column_type):
    """
    Determines if the column is numeric or not

    Argument:
        column_type (String): Name of the column's type

    Returns:
        bool: True if numeric, False if not
    """
    numeric_types = ["INTEGER", "REAL", "NUMERIC", "FLOAT", "DOUBLE"]
    return column_type.upper() in numeric_types


def get_schema_info():
    """
    Connects to a database and returns its schema info

    Returns:
        dict: A dictionary where the keys are the table names and the
              values are the table's columns
    """
    schema = {}
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    query = "SELECT name FROM sqlite_master WHERE type='table';"
    cur.execute(query)

    tables = [row[0] for row in cur.fetchall()]

    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        column_names = [column[1] for column in cur.fetchall()]
        
        schema[table] = column_names

    con.close()
    return schema