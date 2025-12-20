import sqlite3
import os
from data.database import DB_PATH, DB_DIR

def get_column_and_tablenames(db_path=DB_PATH):
    """
    Retrieve the names of all tables and columns from the database

    Argument:
        db_path (string): Path to the database file

    Returns:
        column_names (list): List of all column names
        table_names (list): List of all table names
    """
    schema = get_schema_info(db_path)
    column_names = set()
    table_names = set(schema.keys())

    for table in schema.items():
        for col in table[1]:
            column_names.add(col)

    return list(column_names), list(table_names)


def get_column_types(table, db_path=DB_PATH):
    """
    Retrieves the types of the columns in the table

    Argument:
        table (String): name of the table
        db_path (string): Path to the database file

    Returns:
        dict: Dictionary mapping column names to their types
    """
    con = sqlite3.connect(db_path)
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


def get_schema_info(db_path=DB_PATH):
    """
    Connects to a database and returns its schema info

    Argument:
        db_path (string): Path to the database file

    Returns:
        dict: A dictionary where the keys are the table names and the
              values are the table's columns
    """
    schema = {}

    con = sqlite3.connect(db_path)
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

def get_available_dbs():
    """
    Get list of db files in data directory

    Returns:
        lst: List of db files
    """
    if not os.path.exists(DB_DIR):
        os.mkdir(DB_DIR)
        return []
    
    dbs = []
    for file in os.listdir(DB_DIR):
        if file.endswith('.db'):
            dbs.append(file)

    return dbs

def get_db_path(db):
    """
    Get full path to database file

    Argument:
        db (string): Name of the database file

    Returns:
        string: Path to database file
    """
    return os.path.join(DB_DIR, db)