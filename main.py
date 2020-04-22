import sys
import threading
from MainWindow import MainWindow
from PyQt5 import QtWidgets
from pattern.Mediator import Mediator
from ArduinoSerial import ArduinoSerial
from WSClient import WSClient
from Detector import Detector


if __name__ == '__main__':
    mediator = Mediator()
    serial = ArduinoSerial()
    wsClient = WSClient()
    wsThread = threading.Thread(target=wsClient.run)
    wsThread.start()
    detector = Detector()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #设置中介者托管类对象
    mediator.setSerial(serial)
    mediator.setWSClient(wsClient)
    mediator.setWindow(window)
    mediator.setDetector(detector)
    sys.exit(app.exec_())
