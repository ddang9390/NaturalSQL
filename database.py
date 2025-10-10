import sqlite3
import pandas as pd

DB_DIR = "data"
DB_NAME = "test_movies.db"
DB_PATH = DB_DIR + "/" + DB_NAME


def set_up_table():
    """
    Create a table and populate it with data
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS movies(
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    director TEXT 
                )
                """)

    sample_movies = [
        (1, "The Dark Knight", 2008, "Action", "Chirstopher Nolan"),
        (2, "The Dark Knight Rises", 2012, "Action", "Chirstopher Nolan"),
        (3, "Shrek", 2001, "Comedy", "Andrew Adamson")
    ]

    cur.executemany("INSERT INTO movies VALUES(?, ?, ?, ?, ?)", sample_movies)

    con.commit()
    con.close()
    print("Database", DB_NAME, " has been created and populated")

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

def execute_query(query):
    """
    Connects to database and executes the query generated from
    translating the user's sentence. Displays the results of the
    query and the generated query

    Argument:
        query (string): The generated query
    """
    con = sqlite3.connect(DB_PATH)

    results = pd.read_sql_query(query, con)
    con.close()

    print("\n----Query Results----")
    if results.empty:
        print("The query produced no results")
    else:
        print(results.to_string(index=False))

    print("\nResulting Query: ", query, "\n")
