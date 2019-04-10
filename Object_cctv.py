from pydarknet import Detector, Image
import cv2
import threading
import numpy as np

import server_steer

class Object_Detection():

    def __init__(self, steer):
        # 저장된 YOLO 모델을 호출함
        self.steer = steer
        '''
        self.net = Detector(bytes("YOLOv3/cfg/Noruway.cfg", encoding="utf-8"),
                   bytes("YOLOv3/cfg/Noruway_200.weights", encoding="utf-8"),
                   0, 
                   bytes("YOLOv3/cfg/Noruway.data", encoding="utf-8"))
        '''
        self.net = Detector(bytes("YOLOv3/cfg/yolov1.cfg", encoding="utf-8"),
                   bytes("YOLOv3/cfg/yolo.weights", encoding="utf-8"),
                   0,
                   bytes("YOLOv3/cfg/coco.data", encoding="utf-8"))
        print("ENTERED INIT")

    # 이미지를 입력받아 detection과 classification 결과를 리턴함
    def Detection(self, img):  
        print("test0")
        results = self.net.detect(Image(img))       
        print("RESULTS: ", results)

        detect_list = []
        print("list: ", detect_list)

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


########################################################################

def estimate_distance(x1, y1, x2, y2):
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    return distance



def Collision_Prediction(loc_x, loc_y):
    Dn = estimate_distance(init_x, init_y, loc_x, loc_y)
    Tn = int(time.time()) - T1
    Vn = Dn/Tn
    dn = estimate_distance(loc_x, loc_y, loc_x, emg_y) # Straight distance of object location and emergency line
    t_hat = dn/Vn

    return t_hat

########################################################################

import time
import socket
emg_y = 400 # user_choice emergency line
T1 = int(time.time())
init_x, init_y = (240, 320) # initial location


xn, yn = yolo() # current location return function
emg_t = Collision_Prediction(xn, yn)

if emg_t < 3:
    self.connection.send('s'.encode())
else:
    pass
