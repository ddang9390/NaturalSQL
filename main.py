from database import *
from parser import *

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

    # table = input("Please enter the name of the table you wish to query: ")
    # print()
    # if table in schema.keys():
    #     print("Table found!")
    #     print("Here are the available columns:")
    #     print(schema[table])
    #     print()
    #     taking_question(table)
    #     print("Ending program")
    taking_question()
    print("Ending program")
    

    # else:
    #     print("Error: table not found")

if __name__ == "__main__":
    main()