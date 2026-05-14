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

# ------------------------------------------------------------------------------------------------

def analyze_company(company):
    print()
    print("=" * 30)
    print(company["company"])
    print("=" * 30)
    print()

    esg_scores_list = []     

    for entry in company["data"]:

        env, soc, gov, esg_score = calculate_esg_score(entry)
        esg_scores_list.append(esg_score)
        print("Overall ESG Score: ", round(esg_score, 2))

        if esg_score >= 90:
            rating = "Excellent"
            print(f"Rating: {rating}")
        elif esg_score >= 75:
            rating = "Good"
            print(f"Rating: {rating}")
        elif esg_score >= 60:
            rating = "Average"
            print(f"Rating: {rating}")
        else:
            rating = "Needs Improvement"
            print(f"Rating: {rating}")
        print()
        print("-" * 30)
        print()

    if len(esg_scores_list) > 1:
        if esg_scores_list[-1] > esg_scores_list[0]:
            trend = "Improving"
            print(f"Trend: {trend}")
        elif esg_scores_list[-1] < esg_scores_list[0]:
            trend = "Declining"
            print(f"Trend: {trend}")
        else:
            trend = "Stable"
            print(f"Trend: {trend}")
    print()

def calculate_esg_score(entry):
        
        environmental_values = entry["environmental"].values()
        social_values = entry["social"].values() 
        governance_values = entry["governance"].values()

        environmental_score = sum(environmental_values) / len(environmental_values) 
        social_score = sum(social_values) / len(social_values)
        governance_score = sum(governance_values) / len(governance_values)

        print("Year", entry["year"])
        print(f"Environmental score: {environmental_score}")
        print(f"Social score: {social_score}")
        print(f"Governance score: {governance_score}")

        esg_score = (
            0.4 * environmental_score
            + 0.3 * social_score
            + 0.3 * governance_score
        )  
        return environmental_score, social_score, governance_score, esg_score

""" def ranking():
    ranking_list = []
    for company in data:
        last_entry = company["data"][-1]  # last year

        env, soc, gov, esg_score = calculate_esg_score(last_entry)
        ranking_list.append((company["company"], esg_score))
    ranking_list.sort(key = lambda x: x[1], reverse = True)
    print("\n== Company Ranking ===")   
    for i, (name, score) in enumerate(ranking_list, start = 1):
     print(f"{i}. {name:} --> {score:}") """
     
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
            for item in data:
                analyze_company(item) 

        elif choice == 2:
            for i, item in enumerate(data, start = 1):
                print(i, item["company"])         # show a list of available companies to choos from!
                
            company_number = int(input("\nPlease choose a company number to analyze: "))
            if 1 <= company_number <= len(data):
                index = company_number - 1
                selected_company = data[index]
                analyze_company(selected_company)
            else:
                print("Invalid number, please try again!")   

        elif choice == 3:
           analyzer.ranking()   
        
        elif choice == 4:
            break
        else:
            print("Invalid input, please try again")   
menu()