import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_Form import Ui_Form
from pattern.Mediator import Mediator
from message.Instruction import Instruction

def cvMat2QImage(mat):
    mat_rgb = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
    image = QtGui.QImage(mat_rgb.data, mat_rgb.shape[1], mat_rgb.shape[0], QtGui.QImage.Format_RGB888)
    return image

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btnOpen.clicked.connect(self.btnOpen_on_clicked)
        self.ui.btnClose.clicked.connect(self.btnClose_on_clicked)
        self.initTable()

    def closeEvent(self, event):
        Mediator().closeAll()

    def btnOpen_on_clicked(self):
        Mediator().openTheDoor()

    def btnClose_on_clicked(self):
        Mediator().closeTheDoor()

    def initTable(self):
        items = ["农夫山泉", "可口可乐", "美年达", "康师傅", "芬达", "蛇草水"]
        i = 0
        for item in items:
            self.ui.tableLeft.insertRow(i)
            self.ui.tableLeft.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i+1)))
            self.ui.tableLeft.setItem(i, 1, QtWidgets.QTableWidgetItem(item))
            self.ui.tableLeft.setItem(i, 2, QtWidgets.QTableWidgetItem(str(20)))
            i += 1


    def showImage(self, mat):
        qImage = cvMat2QImage(mat)
        self.ui.lblImg.setPixmap(QtGui.QPixmap.fromImage(qImage))

    def showDetectResult(self, msg):
        self.ui.listResult.addItem(QtWidgets.QListWidgetItem(msg))

    def setDoorStatus(self, status : str):
        self.ui.lblStatus.setText(status)

    def updateLeftStatus(self, instruction : Instruction):
        classid = instruction.item.id
        num = instruction.item.num
        operation = instruction.operation
        items = self.ui.tableLeft.findItems(str(classid), QtCore.Qt.MatchExactly)
        if len(items) != 0:
            row = items[0].row()
            originNum = eval(self.ui.tableLeft.item(row, 2).text())
            if operation == "add":
                num = originNum - num
            elif operation == "del":
                num = originNum + num
            self.ui.tableLeft.setItem(row, 2, QtWidgets.QTableWidgetItem(str(num)))
            self.ui.tableLeft.viewport().update()
