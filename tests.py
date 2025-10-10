import unittest
from parser import preprocess, process

# Sentences that should parse correctly
# TODO - sentences must include more specific names later on
GOOD_SENTENCES = [
    "show me the name of movies",
    "list the name and genre from movies",
    "give me the year, director, and genre in movies"
]

# Sentences that should fail to parse
BAD_SENTENCES = [
    "i eat",
    "show show show",
    "me show movies"
]

# Sentences for testing the SELECT * statement
SELECT_ALL_SENTENCES = [
    "give me everything in the table",
    "show me all of the movies",
    "show me the entire table",
    "let me see everything"
]

TEST_TABLE = "movies"

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

    def test_preprocess_failure(self):
        """
        Test to make sure that the preprocess function does not work
        for sentences that should fail to process
        """
        print()
        print("Testing preprocessing bad sentences")
        total = 0
        for sentence in BAD_SENTENCES:
            if len(preprocess(sentence)) == 0:
                total += 1
            else:
                print("PROBLEM SENTENCE: ", sentence)

        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(BAD_SENTENCES))
    
    def test_process_SELECT_All(self):
        """
        Test to make sure that a SQL SELECT statement could be made 
        """
        print()
        print("Testing translating sentences to SELECT * queries")
        total = 0
        for sentence in SELECT_ALL_SENTENCES:
            query = process(sentence, TEST_TABLE)
            if len(query) > 0:
                total += 1
                print("Translated Statement: ", query)
            else:
                print("PROBLEM SENTENCE: ", sentence)

        print("Test complete")
        print("--------------\n")
        self.assertEqual(total, len(SELECT_ALL_SENTENCES))

if __name__ == "__main__":
    unittest.main()