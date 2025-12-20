import csv
import sqlite3
import pandas as pd

# TODO - remove db_name, make it more dynamic
DB_DIR = "data"
DB_NAME = "test_movies.db"
DB_PATH = DB_DIR + "/" + DB_NAME

INPUT = "data/input/movies.csv"

def set_up_table():
    """
    Create a table and populate it with data
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    table_name = "movies"
    sql = f"DROP TABLE IF EXISTS {table_name}"

    # Execute the SQL query
    cur.execute(sql)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS movies(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    director TEXT,
                    rating FLOAT,
                    runtime FLOAT
                )
                """)

    contents = csv.reader(open(INPUT))
    
    cur.executemany("INSERT INTO movies (name, year, genre, director, rating, runtime) VALUES(?, ?, ?, ?, ?, ?)", contents)

    select_all = "SELECT * FROM movies"
    rows = cur.execute(select_all).fetchall()

    # Output to the console screen
    for r in rows:
        print(r)

    con.commit()
    con.close()
    print("Database", DB_NAME, " has been created and populated")


def execute_query(query, db_path=DB_PATH):
    """
    Connects to database and executes the query generated from
    translating the user's sentence. Displays the results of the
    query and the generated query

    Argument:
        query (string): The generated query
        db_path (string): Path to the database file
    """
    con = sqlite3.connect(db_path)

    results = pd.read_sql_query(query, con)
    con.close()

    print("\n----Query Results----")
    if results.empty:
        print("The query produced no results")
    else:
        print(results.to_string(index=False))

    print("\nResulting Query: ", query, "\n")

    return query, results.to_html()

