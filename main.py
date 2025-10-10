from database import *


def main():
    schema = get_schema_info()
    print("List of tables")
    print("---------------")
    print("--".join(key for key in schema.keys()))

    table = input("Please enter the name of the table you wish to query: ")
    print()
    if table in schema.keys():
        print("Table found!")
        print("Here are the available columns:")
        print(schema[table])
    else:
        print("Error: table not found")

if __name__ == "__main__":
    main()