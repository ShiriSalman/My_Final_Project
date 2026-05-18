class Company:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        

class Analyzer:

    def __init__(self, company_list):
        self.company_list = company_list

    def analyze_company(self, company):

        print()
        print("=" * 30)
        print(company.name)
        print("=" * 30)
        print()

        esg_scores_list = []     

        for entry in company.data:

            env, soc, gov, esg_score = Analyzer.calculate_esg_score(entry)
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

            print("Year", entry["year"])
            print(f"Environmental score: {env}")
            print(f"Social score: {soc}")
            print(f"Governance score: {gov}")

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
    @staticmethod
    def calculate_esg_score(entry):

        environmental_values = entry["environmental"].values()
        social_values = entry["social"].values() 
        governance_values = entry["governance"].values()

        environmental_score = sum(environmental_values) / len(environmental_values) 
        social_score = sum(social_values) / len(social_values)
        governance_score = sum(governance_values) / len(governance_values)

        esg_score = (
            0.4 * environmental_score
            + 0.3 * social_score
            + 0.3 * governance_score
        )

        return environmental_score, social_score, governance_score, esg_score

# --------------------------------------------------------------------------------------------------
    def ranking(self):

        ranking_list = []
        output = ""
        for company in self.company_list:
            last_entry = company.data[-1]  # last year

            env, soc, gov, esg_score = Analyzer.calculate_esg_score(last_entry)

            ranking_list.append((company.name, esg_score))
            ranking_list.sort(key = lambda x: x[1], reverse = True)

        output += "\n=== Company Ranking ===\n"
        output += "\n"   
        for i, (name, score) in enumerate(ranking_list, start = 1):
            output += f"{i}. {name:<20} --> {score:.2f}\n"
        return output    
