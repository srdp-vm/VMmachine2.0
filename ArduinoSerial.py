import serial
from pattern.Mediator import Mediator
from threading import Thread


class ArduinoSerial:

    def __init__(self, port_name = "COM3"):
        super().__init__()
        self.stop = False
        try:
            bps = 9600     #波特率
            # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
            timex = None
            self.ser = serial.Serial(port_name, bps, timeout=timex) #创建对象同时已经打开串口
            print("Serial:Serial {} opened".format(self.ser.name))

            def readSerial():
                while not self.stop:
                    if self.ser.inWaiting():  # Return the number of bytes in the receive buffer.
                        # Read size bytes from the serial port. If a timeout is set it
                        # may return less characters as requested. With no timeout it
                        # will block until the requested number of bytes is read.
                        data = self.ser.read(self.ser.inWaiting())
                        print("Serial: <<", data)
                        state = int.from_bytes(data, byteorder='big')
                        if state == 0:  #arduino发送来0，表示传感器检测到磁铁进入
                            print("Serial:Sensor detected Megnet in")
                            self.onMegnetIn()
                        elif state == 1: #arduino发送来1，表示传感器检测到磁铁远离
                            print("Serial:Sensor detected Megnet out")
                            self.onMegnetOut()

            self.ser_thread = Thread(target=readSerial)  #线程轮训访问串口
            self.ser_thread.start()
        except Exception as e:
            print("Serial:Exception ", e)
            #exit(0)


    def send(self, data):
        try:
            self.ser.write(data.encode('utf-8'))
            print("Serial: >> ", data)
        except Exception as e:
            print("Serial:Exception", e)

    def onMegnetIn(self):
        Mediator().settleUp()
        Mediator().form_SetDoorStatus("关")

    def onMegnetOut(self):
        Mediator().form_SetDoorStatus("开")

    def close(self):
        self.stop = True
        try:
            self.send('C')
            print("Serial:Lock close")
            self.ser_thread.join()
            self.ser.close()
        except Exception as e:
            print("Serial:Exception", e)