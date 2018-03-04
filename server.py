import zmq
from stockDataCollector import StockHandler
import json
import ast

def parse_dict(param_str):
    return ast.literal_eval(param_str)

def parse_json(param_str):
    return json.loads(param_str)

class Server:

    # def signal_handler(self, signal, frame):
    #     sys.exit(0)
    #     signal.signal(signal.SIGINT, signal_handler)
    #     j = json.dumps({'hey' : 'ho!'})
    def __init__(self, port):
        self.socket = zmq.Context().socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:" + str(port))

    def __try_communication(self):
        self.socket.send_string('{ Communication test : successful }')

    def run(self):
        try:
            while True:
                #  Wait for next request from client
                print("waiting for client input...")
                message = self.socket.recv()
                print("Received request: %s" % message)

                #  Do some 'work'
                #time.sleep(1)

                #  Send reply back to client
                self.reply(message)
                if(self.should_shutdown):
                    raise ShutdownException("server shutdown due to controller command")
        except AttributeError:
            raise

    def reply(self, message):
        self.socket.send_json(self.handle(message))

    def handle(self, message):
        print("Got message: {}".format(message))
        # self.__try_communication() #placeholder
        replies = {}
        #handle each request and append the replies dictionary with a reply. Exit when receiving an entry with "exit" value.
        for entry in message:
            request = message[entry]
            if(request == "exit"):
                self.should_shutdown = True
            if(request["action"].lower() == "getHistorical".lower()):
                sh = StockHandler()
                sh.openStock(request["symbol"])
                replies[entry] = sh.getHistorical(request["start"], request["end"]) # add reply
        return replies

class ShutdownException(Exception): pass #define an exception for server shutdown

try:
    s = Server(5555)
    print("mockup reply (because we have no client to ask us for a reply): " + str(s.handle(json.loads('{"1":{"action":"getHistorical", "symbol":"GOOGL", "start":"2017-01-01", "end":"2017-01-06"}}'))))#, "2":"exit"
    s.run()

except Exception as e:
    if(type(e) == ShutdownException):
        print("******* Server shutting down due to controller command *******")
    else:
        print("CAUGHT AN EXCEPTION, SHUTTING DOWN...")
        s.socket.__exit__()
        raise
