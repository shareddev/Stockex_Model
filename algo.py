import pandas
import json
class Algorithm:
    def getRecommend(self):
        #TODO: check mongoDB for previous recommendations and return if they are recent
        return json.loads(pandas.DataFrame(index=['GOOGL', 'AAPL'],data={'Score': [57, 33]}).to_json())