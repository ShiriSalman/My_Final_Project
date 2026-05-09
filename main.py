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

def analyze_company(company):
    print()
    print("=" * 30)
    print(company["company"])
    print("=" * 30)
    print()

    esg_scores_list = []     

    for entry in company["data"]:
        
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

    esg_scores_list.append(esg_score)
    print("Overall ESG Score: ", round(esg_score, 2))

    rating = ""
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

    trend = ""
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
            print("Invalid input, please enter  number")    
            continue

        if choice == 1:
            print("+++ Analyse all Companies +++")
            for item in data:
                analyze_company(item)    # to be implemented

        elif choice == 2:
            ...
        elif choice == 3:
            pass
        elif choice == 4:
            break
        else:
            print("Invalid input, please try again")   
menu()