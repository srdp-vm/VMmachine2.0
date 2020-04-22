import json
import threading
from message.Instruction import Instruction


class Mediator:
    _instance_lock = threading.Lock()
    serial : object
    detector : object
    wsClient : object
    window : object

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Mediator, "_instance"):
            with Mediator._instance_lock:
                if not hasattr(Mediator, "_instance"):
                    Mediator._instance = object.__new__(cls)
        return Mediator._instance

    def setSerial(self, serial):
        self.serial = serial

    def setDetector(self, detector):
        self.detector = detector

    def setWSClient(self, wsClient):
        self.wsClient = wsClient

    def setWindow(self, window):
        self.window = window

    def startDetect(self):
        self.detector.detect()

    def stopDetect(self):
        self.detector.stop()

    def openTheDoor(self):
        self.serial.send("O")
        self.detector.detect()

    def closeTheDoor(self):
        self.serial.send("C")
        self.detector.stop()
        self.settleUp()

    def form_ShowImage(self, mat):
        self.window.showImage(mat)

    def form_ShowResult(self, msg : str):
        self.window.showDetectResult(msg)

    def form_SetDoorStatus(self, status):
        self.window.setDoorStatus(status)

    def form_UpdateLeftStatus(self, instruction : Instruction):
        self.window.updateLeftStatus(instruction)

    def wsSend(self, msg : str):
        self.wsClient.send(msg)

    def settleUp(self):
        instruction = Instruction()
        instruction.operation = "settleup"
        self.wsClient.send(json.dumps(instruction, default=lambda o: o.__dict__))

    def closeAll(self):
        self.serial.close()
        self.detector.stop()
        self.wsClient.close()