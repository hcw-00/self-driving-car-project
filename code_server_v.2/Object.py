from pydarknet import Detector, Image
import cv2
import threading
import numpy as np

import server_steer

class Object_Detection():

    def __init__(self, steer):

        self.steer = steer
        '''
        self.net = Detector(bytes("YOLOv3/cfg/Noruway.cfg", encoding="utf-8"),
                   bytes("YOLOv3/cfg/Noruway_200.weights", encoding="utf-8"),
                   0, 
                   bytes("YOLOv3/cfg/Noruway.data", encoding="utf-8"))
        '''
        print("ENTERED INIT")
        self.net = Detector(bytes("YOLOv3/cfg/yolov1.cfg", encoding="utf-8"),
                   bytes("YOLOv3/cfg/yolo.weights", encoding="utf-8"),
                   0,
                   bytes("YOLOv3/cfg/coco.data", encoding="utf-8"))
        print("Exiting INIT")


    def Detection(self, img):  
        #print("test0")
        param = Image(img)
        #print(param)
        #print("test1")
        results = self.net.detect(param)       
        #print("RESULTS: ", results)

        detect_list = []
        #print("list: ", detect_list) # by hcw

        for cat, score, bounds in results:
            x, y, w, h = bounds
            cv2.rectangle(img, 
                          (int(x - w / 2), int(y - h / 2)), 
                          (int(x + w / 2), int(y + h / 2)), 
                          (255, 0, 0), 
                          thickness=2)
            cv2.putText(img, 
                        str(cat.decode("utf-8")), 
                        (int(x - w / 2), int(y + h / 4)), 
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255))
            detect_list.append(cat.decode())
        print("test")
        cv2.imshow('dect', img)
        print("test2")
        cv2.waitKey(1) # hcw

        self.steer.Set_ObjectDetection(detect_list)
