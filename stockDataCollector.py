import bulbea as bb
from pprint import pprint as pp
import json
class StockHandler:
    def openStock(self, symbol, source = 'WIKI'):
        self.stock = bb.Share(source = 'WIKI', ticker = symbol)

    def getHistorical(self, start, end):
        data = self.stock.data
        data = data[(data.index <= end) & (data.index >= start)]
        jsonObj = json.loads(data.to_json(orient='index', date_format='iso'))
        self.__clean_timestamps(jsonObj)
        return jsonObj

    def __clean_timestamps(self, jsonObj):
        for datetime in list(jsonObj):
            jsonObj[datetime[:10]] = jsonObj.pop(datetime)

    def test(self):
        print("Testing the handler with Google's stock, 2017-01-01 through 2017-01-06...")
        self.openStock('GOOGL')
        z = self.getHistorical('2017-01-01', '2017-01-06')
        pp(z)

# s = StockHandler()
# s.test()