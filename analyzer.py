class Company:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        

class Analyzer:

    def __init__(self, company_list):
        self.company_list = company_list

    @staticmethod
    def analyze_company(company):

        result = ""
        result += "\n"
        result += f"=" * 30 + "\n"
        result += f"{company.name}\n"
        result += f"=" * 30 + "\n"

        esg_scores_list = []

        for entry in company.data:

            env, soc, gov, esg_score = Analyzer.calculate_esg_score(entry)
            esg_scores_list.append(esg_score)

            rating = Analyzer.get_rating(esg_score)

            result += "\n"

            result += f"Year: {entry['year']}\n"
            result += f"=" * 30 + "\n"
            result += f"{'Environmental Score':<22}: {env:.2f}\n"
            result += f"{'Social Score':<22}: {soc:.2f}\n"
            result += f"{'Governance Score':<22}: {gov:.2f}\n"
            result += f"{'Overall ESG Score':<22}: {esg_score:.2f}\n"
            result += f"{'Rating':<22} {rating}\n"

        trend = ""
        if len(esg_scores_list) > 1:
            trend = Analyzer.get_trend(company.data)

        result += f"=" * 30 + "\n"
        result += f"Trend: {trend}\n"
        result += "\n"
        return result
            
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
# ----------------------------------------------
    @staticmethod
    def get_trend(company_data):
        first_entry = company_data[0]
        last_entry = company_data[-1]

        _, _, _, first_score = Analyzer.calculate_esg_score(first_entry)
        _, _, _, last_score = Analyzer.calculate_esg_score(last_entry)

        if last_score > first_score:
            return "Improving"
        elif last_score < first_score:
            return "Declining"
        else:
            return "Stable"
    
# --------------------------------------------------    
    @staticmethod
    def get_rating(esg_score):

        if esg_score >= 90:
            rating = "Excellent"
        elif esg_score >= 75:
            rating = "Good"
        elif esg_score >= 60:
            rating = "Average"
        else:
            rating = "Needs Improvement"
        return rating