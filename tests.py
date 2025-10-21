import unittest
from NLP.parser import preprocess, process, init_parser

TEST_TABLE = "movies"
parser = init_parser()

# Sentences that should parse correctly
GOOD_SENTENCES = [
    "show me the name of movies",
    "list the name and genre from movies",
    "give me the year, director, and genre in movies",
    "show me the movies"
]

# Sentences that should fail to parse
# TODO - make actual bad sentences
BAD_SENTENCES = [
    "i eat",
    "show show show",
    "me show movies"
]

# Sentences for testing the SELECT * statement
SELECT_ALL_SENTENCES = [
    "Show the movies",
    "give me everything in the table",
    "show me all of the movies",
    "show me the entire table",
    "let me see everything",
    "show me the movies"
]

SELECT_FROM_COLUMNS_SENTENCES = {
    "show me the name of movies": f"SELECT name FROM {TEST_TABLE};",
    "list the director and genre": f"SELECT director, genre FROM {TEST_TABLE};",
    "who are the director": f"SELECT director FROM {TEST_TABLE};",
    "show me the year": f"SELECT year FROM {TEST_TABLE};",
    "give me the name, director, and genre": f"SELECT name, director, genre FROM {TEST_TABLE};",
    "show me the names of movies": f"SELECT name FROM {TEST_TABLE};",
}

SIMILAR_SOUNDING_SENTENCES = {
    "shw me the nam of movies": f"SELECT name FROM {TEST_TABLE};",
    "lst the director and gere": f"SELECT director, genre FROM {TEST_TABLE};",
    "who are the directors": f"SELECT director FROM {TEST_TABLE};",
    "show me the years": f"SELECT year FROM {TEST_TABLE};",
    "give me the names, directors, and genres": f"SELECT name, director, genre FROM {TEST_TABLE};",
    "show me the names of movies": f"SELECT name FROM {TEST_TABLE};",
}
    
WHERE_SENTENCES = {
    "show me the name of movies where name is \"Shrek\"": f"SELECT name FROM {TEST_TABLE} WHERE LOWER(name) = 'shrek';",
    "show me the name of movies where name is \"The Dark Knight Rises\"": f"SELECT name FROM {TEST_TABLE} WHERE LOWER(name) = 'the dark knight rises';",
    "show me the name of movies where the name is \"shrek\"": f"SELECT name FROM {TEST_TABLE} WHERE LOWER(name) = 'shrek';",
    "show me all of movies where the name is \"shrek\"": f"SELECT * FROM {TEST_TABLE} WHERE LOWER(name) = 'shrek';",
    "show me all of movies where the year is 2008": f"SELECT * FROM {TEST_TABLE} WHERE year = 2008;",

    # Handling SELECT * with WHERE clause
    "show me the movies where the name is \"Shrek\"": f"SELECT * FROM {TEST_TABLE} WHERE LOWER(name) = 'shrek';",

    # Handling more complex clauses with AND/OR
    "show me movies where director is \"Christopher Nolan\" and year is 2010": f"SELECT * FROM {TEST_TABLE} WHERE LOWER(director) = 'christopher nolan' AND year = 2010;",
    "show me movies where director is \"Christopher Nolan\" or director is \"Steven Spielberg\"": f"SELECT * FROM {TEST_TABLE} WHERE LOWER(director) = 'christopher nolan' OR LOWER(director) = 'steven spielberg';",
    
    
}


ORDER_BY_SENTENCES = {
    "show me movies sorted by year": "SELECT * FROM movies ORDER BY year;",
    "list name and genre ordered by name desc": "SELECT name, genre FROM movies ORDER BY name DESC;",
    "list name and genre ordered by name in descending order": "SELECT name, genre FROM movies ORDER BY name DESC;",
    "show all movies where genre is \"Action\" order by year asc": "SELECT * FROM movies WHERE LOWER(genre) = 'action' ORDER BY year ASC;",
    "show all movies where genre is 'Action' order by the year in ascending order": "SELECT * FROM movies WHERE LOWER(genre) = 'action' ORDER BY year ASC;"
}

LIMIT_SENTENCES = {    
    "show me 15 movies": f"SELECT * FROM {TEST_TABLE} LIMIT 15;",
    "show me the name and year for 5 movies": f"SELECT name, year FROM {TEST_TABLE} LIMIT 5;",

    # Implied order by, column can't be determined
    "show me the top 5 movies": f"SELECT * FROM {TEST_TABLE} LIMIT 5;",
    "list the bottom 3 movies": f"SELECT * FROM {TEST_TABLE} LIMIT 3;",
    "what is the top movie": f"SELECT * FROM {TEST_TABLE} LIMIT 1;",
    "show me the worst movie": f"SELECT * FROM {TEST_TABLE} LIMIT 1;",


    # With explicit order by
    "list the top 5 movies by name": f"SELECT * FROM {TEST_TABLE} ORDER BY name ASC LIMIT 5;", 
    "show me the top 3 movies ordered by year descending": f"SELECT * FROM {TEST_TABLE} ORDER BY year DESC LIMIT 3;",
    "give me 5 movies sorted by genre": f"SELECT * FROM {TEST_TABLE} ORDER BY genre ASC LIMIT 5;",


    # Combining WHERE, ORDER BY, and LIMIT
    "show me the top 2 movies where genre is 'Action'": f"SELECT * FROM {TEST_TABLE} WHERE LOWER(genre) = 'action' ORDER BY year DESC LIMIT 2;",
    "list name and year from movies where director is 'Christopher Nolan' order by year desc limit 1": f"SELECT name, year FROM {TEST_TABLE} WHERE LOWER(director) = 'christopher nolan' ORDER BY year DESC LIMIT 1;",
    "show me the bottom 2 movies with genre 'Action'": f"SELECT * FROM {TEST_TABLE} WHERE LOWER(genre) = 'action' ORDER BY year ASC LIMIT 2;",
    "show me the top 2 movies where year is 2008": f"SELECT * FROM {TEST_TABLE} WHERE year = 2008 ORDER BY year DESC LIMIT 2;",
}

class Tests(unittest.TestCase):
    def test_preprocess_success(self):
        """
        Test to make sure that the preprocess function can work
        with simple sentences
        """
        print()
        print("Testing preprocessing good sentences")
        total = 0
        for sentence in GOOD_SENTENCES:
            if len(preprocess(sentence)) > 0:
                total += 1
            else:
                print("PROBLEM SENTENCE: ", sentence)

        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(GOOD_SENTENCES))

    # def test_preprocess_failure(self):
    #     """
    #     Test to make sure that the preprocess function does not work
    #     for sentences that should fail to process
    #     """
    #     print()
    #     print("Testing preprocessing bad sentences")
    #     total = 0
    #     for sentence in BAD_SENTENCES:
    #         if len(preprocess(sentence)) == 0:
    #             total += 1
    #         else:
    #             print("PROBLEM SENTENCE: ", sentence)

    #     print("Test complete")
    #     print("--------------\n")
    #     self.assertEqual(total, len(BAD_SENTENCES))
    
    def test_process_SELECT_All(self):
        """
        Test to make sure that a SQL SELECT statement could be made 
        """
        print()
        print("Testing translating sentences to SELECT * queries")
        total = 0
        expected_query = f"SELECT * FROM {TEST_TABLE};"
        for sentence in SELECT_ALL_SENTENCES:
            query = process(sentence, parser, TEST_TABLE)
            if query == expected_query:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("PROBLEM SENTENCE: ", sentence)

        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(SELECT_ALL_SENTENCES))

    def test_process_SELECT_COLS(self):
        """
        Test to make sure that a SQL SELECT statement could be made
        targetting specific columns
        """
        print()
        print("Testing translating sentences to SELECT queries with cols")
        total = 0

        for sentence in SELECT_FROM_COLUMNS_SENTENCES.keys():
            expected_query = SELECT_FROM_COLUMNS_SENTENCES[sentence]
            query = process(sentence, parser, TEST_TABLE)
            if query == expected_query:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("Expected:", expected_query)
                print("Actual:", query)
                print("PROBLEM SENTENCE: ", sentence)
                print()
                
        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(SELECT_FROM_COLUMNS_SENTENCES))

    def test_process_similar_sentences(self):
        """
        Test to make sure that sentences with similar words that are not the exact words
        could be processed and translated properly
        """
        print()
        print("Testing translating sentences with similar words")
        total = 0

        for sentence in SIMILAR_SOUNDING_SENTENCES.keys():
            expected_query = SIMILAR_SOUNDING_SENTENCES[sentence]
            query = process(sentence, parser, TEST_TABLE)
            if query == expected_query:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("Expected:", expected_query)
                print("Actual:", query)
                print("PROBLEM SENTENCE: ", sentence)
                print()
                
        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(SIMILAR_SOUNDING_SENTENCES))

    def test_process_WHERE_clause(self):
        """
        Test to make sure that a WHERE clause could be made
        """
        print()
        print("Testing generating queries with WHERE clause")
        total = 0

        for sentence in WHERE_SENTENCES.keys():
            expected_query = WHERE_SENTENCES[sentence]
            query = process(sentence, parser, TEST_TABLE)
            if query == expected_query:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("Expected:", expected_query)
                print("Actual:", query)
                print("PROBLEM SENTENCE: ", sentence)
                print()
                
        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(WHERE_SENTENCES))

    def test_process_ORDER_BY_clause(self):
        """
        Test to make sure that a ORDER BY clause could be made
        """
        print()
        print("Testing generating queries with ORDER BY clause")
        total = 0

        for sentence in ORDER_BY_SENTENCES.keys():
            expected_query = ORDER_BY_SENTENCES[sentence]
            query = process(sentence, parser, TEST_TABLE)
            if query == expected_query:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("Expected:", expected_query)
                print("Actual:", query)
                print("PROBLEM SENTENCE: ", sentence)
                print()
                
        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(ORDER_BY_SENTENCES))

    def test_process_LIMIT_clause(self):
        """
        Test to make sure that a LIMIT clause could be made
        """
        print()
        print("Testing generating queries with LIMIT clause")
        total = 0

        for sentence in LIMIT_SENTENCES.keys():
            expected_query = LIMIT_SENTENCES[sentence]
            query = process(sentence, parser, TEST_TABLE)
            if query == expected_query:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("Expected:", expected_query)
                print("Actual:", query)
                print("PROBLEM SENTENCE: ", sentence)
                print()
                
        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(LIMIT_SENTENCES))


if __name__ == "__main__":
    unittest.main()