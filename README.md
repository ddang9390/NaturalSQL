# NaturalSQL
This project translates a natural language statement inputted by the user into an SQL query through Natural Language Processing



<details>
    <summary>Table of Contents</summary>
    <ol>
            <li><a href="#getting-started">Getting Started</a></li>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
            </ul>
            <li><a href="#how-it-works">How it Works</a></li>
            <li><a href="#contact">Contact</a></li>
    </ol>
</details>


## Getting Started
### Prerequisites
Python 3.7+

### Installation
1. Download the code or clone the repository  
git clone https://github.com/ddang9390/NaturalSQL.git
2. Navigate to the project directory  
cd NaturalSQL
3. Run the main file  
python3 main.py

## How it Works
### Preprocessing the Statement
Before the user's statement could be translated to SQL, it has to be cleaned and standardized for processing. First, phrases that would be involved in search statements like the names of movies would be replaced with generic placeholders with the original values being saved for later.

The remaining words are then lemmatized. This process involves reducing words to their root form, like making a plural word like 'movies' into a singular word like 'movie.'

After that, a fuzzy matching algorithm known as Levenshtein distance is used. This algorithm is used to compare unknown words against known vocabulary. If a match is found with a high confidence score, the unknown word is replaced with the known word. This is done as a way of handling mispellings or the user's way of shortening known words.


### Parsing with Context Free Grammar (CFG)
Once the sentence has been preprocessed, it is ready to be parsed using Context-Free Grammar (CFG). CFG is a set of formal rules that define the structure of a sentence. Through this CFG, the parser breaks the sentence apart into a syntax tree.

This syntax tree would identify which parts of the sentence are related to SELECT clauses, WHERE clauses, ORDER By clauses, or are just common noun or verb phrases. The translator would go through this tree and build the SQL query piece by piece.


## Contact
Daniel Dang - https://www.linkedin.com/in/daniel-dang-704791a6/

https://github.com/ddang9390/NaturalSQL