class Company:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        

class Analyzer:

    def __init__(self, company_list):
        self.company_list = company_list

    def analyze_company(self):
        pass

    def calculate_esg_score(self):
        pass

    def ranking(self):
        ranking_list = []

        for company in self.company_list:
            last_entry = company["data"][-1]  # last year

            env, soc, gov, esg_score = self.calculate_esg_score(last_entry)

            ranking_list.append((company.name, esg_score))
            ranking_list.sort(key = lambda x: x[1], reverse = True)

            print("\n== Company Ranking ===")   
            for i, (name, score) in enumerate(ranking_list, start = 1):
             print(f"{i}. {name:} --> {score:}")
