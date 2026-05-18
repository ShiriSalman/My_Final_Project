# import libraries

from pathlib import Path
import json

from analyzer import Company
from analyzer import Analyzer

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

print()

# create a list of company objects:

company_list = []
for item in data:
    new_company = Company(item["company"], item["data"])
    company_list.append(new_company)   

analyzer = Analyzer(company_list)                       
   
# ------------------------------------------------------------------------------------
                                       # main menu:
# ------------------------------------------------------------------------------------

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
            print("Invalid input, please enter a number")    
            continue

        if choice == 1:
            print("+++ Analyse all Companies +++")
            for company in company_list:
                analyzer.analyze_company(company) 

        elif choice == 2:
            for i, company in enumerate(company_list, start = 1):
                print(i, company.name)         # show a list of available companies to choos from!
                
            try:
                company_number = int(input("\nPlease choose a company number to analyze: "))
            except ValueError:
                print("Invalid input, please enter a number!")
                continue
            
            if 1 <= company_number <= len(data):
                index = company_number - 1
                selected_company = company_list[index]
                analyzer.analyze_company(selected_company)
            else:
                print("Invalid number, please try again!")   

        elif choice == 3:
           analyzer.ranking()   
        
        elif choice == 4:
            break
        else:
            print("Invalid input, please try again")   
            
menu()