import sqlite3

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