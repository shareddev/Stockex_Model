import pandas
import json
class Algorithm:
    def getEasySearch(self, budget):
        b = int(budget)
        return json.loads(pandas.DataFrame(index=['GOOGL', 'AAPL'], data={'Score': [57*b, 33]}).to_json())

    def getAdvSearch(self, budget, company_type, company_name):
        return json.loads(pandas.DataFrame(index=['GOOGL', 'AAPL'], data={'Score': [57*b, 33]}).to_json())

    def getRecommend(self):
        #TODO: check mongoDB for previous recommendations and return if they are recent
        companies = ['GOOGL', 'AAPL']
        data = {'Score': '[57, 33]'}
        return pandas.DataFrame(index=companies, data=data).to_json()
