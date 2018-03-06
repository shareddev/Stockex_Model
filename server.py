from pprint import pprint
import zmq
from stockDataCollector import StockHandler
import json
import ast
from algo import Algorithm as Algo
def parse_dict(param_str):
    return ast.literal_eval(param_str)

def parse_json(param_str):
    return json.loads(param_str)

def comp(str1, str2):
    return str1.lower() == str2.lower()

class Server:
    def __init__(self, port):
        self.socket = zmq.Context().socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:" + str(port))
        self.algo = Algo()
        self.stockHandler = StockHandler()

    def __try_communication(self):
        self.socket.send_string('{ Communication test : successful }')

    def run(self):
        try:
            while True:
                #  Wait for next request from client
                print("waiting for client input...")
                message = self.socket.recv()

                #  Do some 'work'
                #time.sleep(1)

                #  Send reply back to client
                self.reply(message)
                if(self.should_shutdown):
                    raise ShutdownException("server shutdown due to controller command")

        except Exception as e:
            if (type(e) == ShutdownException):
                print("******* Server shutting down due to controller command *******")
            else:
                print("CAUGHT AN EXCEPTION, SHUTTING DOWN...")
                s.socket.__exit__()
                raise

    def reply(self, message):
        self.socket.send_json(self.handle(message))
    def __shouldExit(self):
        self.should_shutdown = True

    def __getHistorical(self, request, entry):
        #TODO: sort requests by stock and handle requests to same stock together (not sure if faster)
        self.replies[entry] = self.stockHandler.getHistorical(request["symbol"], request["start"], request["end"])  # add reply

    def __getRecommend(self, request, entry):
        self.replies[entry] = self.algo.getRecommend()




    def handle(self, message):
        print("Got message: ")
        pprint(message)
        self.replies = {}
        #handle each request and append the replies dictionary with a reply. Exit when receiving an entry with "exit" value.
        for entry in message:
            request = message[entry]
            action = request["action"]
            if (action == "exit"):
                self.__shouldExit()
            elif(comp(action, "getRecommend")):
                self.__getRecommend(request, entry)
            elif(comp(action, "getHistorical")):
                self.__getHistorical(request, entry)
        return self.replies

class ShutdownException(Exception): pass #define an exception for server shutdown

##############  TESTS  ##############
def test_getHistorical():
    return {"action":"getHistorical", "symbol":"GOOGL", "start":"2017-01-06", "end":"2017-01-06"}
def test_getRecommend():
    return {"action":"getRecommend"}
def test_exit():
    return {"action":"exit"}
def test(requestList):
    i = 0
    jsonReq = {}
    for req in requestList:
        jsonReq[i] = req
        i+=1
     # , "2":"exit"
    reply = (s.handle(jsonReq))
    print("mockup reply: ")
    pprint(reply)
##############  /TESTS  ##############

s = Server(5555)
print("mockup request (because we have no client to ask us for a reply)...")
test([test_getHistorical(),test_getRecommend(),test_exit()])
s.run()




