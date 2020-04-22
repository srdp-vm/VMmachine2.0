import websocket
import json
from pattern.Mediator import Mediator

class WSClient:

    def __init__(self, url="ws://srdp-vm.cn/VMserver/websocket/machine"):
        super().__init__()
        self.ws = websocket.WebSocketApp(url=url,
                                         on_open=lambda w: self.on_open(w),
                                         on_message=lambda w, msg: self.on_message(w, msg),
                                         on_close=lambda w: self.on_close(w),
                                         on_error=lambda w, e: self.on_error(w, e))
        self.status = "Initailed"

    def on_open(self, ws):
        print("Websocket: Connection opened.")
        self.status = "Open"

    def on_close(self, ws):
        print("Websocket: Connection closed.")
        self.status = "Close"

    def on_error(self, ws, error):
        print("Websocket: Error!", error)
        self.status = "Error"

    def on_message(self, ws, message):
        print("Websocket: <<", message)
        instructon = json.loads(message)
        if instructon['operation'] == "open":
            Mediator().openTheDoor()
            Mediator().startDetect()
        elif instructon['operation'] == "close":
            Mediator().closeTheDoor()
            Mediator().stopDetect()

    def close(self):
        self.ws.close()

    def send(self, message):
        try:
            self.ws.send(message)
            print("Websocket: >>", message)
        except Exception as e:
            print("Websocket:Exception ", e)
            exit(0)

    def run(self):
        self.ws.run_forever(ping_interval=30)
