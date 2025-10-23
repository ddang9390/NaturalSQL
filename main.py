from data.db_utils import *
from NLP.parser import *
from GUI.main_ui import *

def taking_question():
    """
    Taking input from user to translate it to SQL
    """
    while True:
        question = input("Please ask your question or type 'quit' to exit: ")
        if question.lower() == 'quit' or question.lower() == 'q':
            break

        query = process(question)
        if query:
            execute_query(query)
        else:
            print("Invalid input")



def main():
    schema = get_schema_info()
    print("List of tables")
    print("---------------")
    print("--".join(key for key in schema.keys()))

    #taking_question()
    main_ui = MainGUI(parser= init_parser())
    main_ui.run_ui()
    print("Ending program")


if __name__ == "__main__":
    main()