# import libraries

from pathlib import Path
import json

# --------------- read ESG data from esg_data.json --------------------

FILE_NAME = "esg_data.json"

path = Path.cwd() / FILE_NAME

try:
    with path.open(mode="r", ) as file:
        data = json.load(file)  # Convert JSON data to a Python object
        print("*** Data loaded successfully ***")
        print("Number of companies:", len(data))
except FileNotFoundError:
    print(f"{path} does not exist.")
except Exception as e:
    print(f"Unexpected error: {e}")

print(data)

# ------------------------------------------------------------------------------------------------

# main menu:
def menu(): 
    while True:
        print("=" * 25)
        print("ESG Data Analyzer")
        print("=" * 25)

        print()

        # menu options:
        print("1. Analyze all companies")
        print("2. Analyze one Company")
        print("3. Ranking")
        print("4. Exit")

        try:
            choice = int(input("\nPlease choose an option: "))
        except ValueError:
            print("Invalid input, please enter  number")    
            continue

        if choice == 1:
            print("+++ Analyse all Companies +++")
            ...
            # to be implemented

        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            break
        else:
            print("Invalid input, please try again")   
menu()