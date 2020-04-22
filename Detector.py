import cv2
import random
import json
from pattern.Mediator import Mediator
from message.Instruction import Instruction
from message.Item import Item

class Detector:
    def __init__(self):
        super().__init__()
        self.quit = False

    def detect(self):
        print("Detector: Start to detect.")
        self.quit = False
        i = 0
        cap = cv2.VideoCapture(0)
        while not self.quit:
            ret, frame = cap.read()
            if not ret:
                print("Read Complete")
                break
            # cv2.imshow("Camera", frame)
            Mediator().form_ShowImage(frame)
            cv2.waitKey(1)
            i %= 60
            if i == 0:
                item = Item()
                item.id = random.randint(1, 6)
                item.num = 1
                instruction = Instruction()
                instruction.operation = "add"# if random.randint(0, 1) == 0 else "del"
                instruction.item = item
                Mediator().wsSend(json.dumps(instruction, default=lambda o: o.__dict__))
                Mediator().form_ShowResult(json.dumps(instruction, default=lambda o: o.__dict__))
                Mediator().form_UpdateLeftStatus(instruction)
            i += 1
        cap.release()
        cv2.destroyAllWindows()


    def stop(self):
        self.quit = True