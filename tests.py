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
    "show show show"
    "me show movies"
]

class Tests(unittest.TestCase):
    def test_preprocess_success(self):
        """
        Test to make sure that the preprocess function can work
        with simple sentences
        """
        total = 0
        for sentence in GOOD_SENTENCES:
            total += len(preprocess(sentence))

        self.assertIsNot(total, 0)

    def test_preprocess_failure(self):
        """
        Test to make sure that the preprocess function does not work
        for sentences that should fail to process
        """
        total = 0
        for sentence in BAD_SENTENCES:
            total += len(preprocess(sentence))
            print(preprocess(sentence))

        self.assertEqual(total, 0)
    
    def test_process_SELECT(self):
        """
        Test to make sure that a SQL SELECT statement could be made 
        """
        pass

if __name__ == "__main__":
    unittest.main()