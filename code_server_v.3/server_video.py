import numpy as np
import cv2
import argparse


import threading

import Object
import Detection_modified
#import StopLine

from model import NeuralNetwork

class CollectTrainingData(object):

    def __init__(self, client, steer):        
        import argparse

        self.client = client        
        self.steer = steer

        #self.args = Namespace(classes='yolov3.txt', config='yolov2-tiny.cfg', image='dog.jpg', weights='yolov2-tiny.weights')
        #self.stopline = StopLine.Stop()


        #self.dect = Detection_modified.Object_Detection() # hcw
        self.dect = Object.Object_Detection(self.steer)

        # model create

        #self.model = NeuralNetwork()
        #self.model.load_model(path = 'model_data/video_model_1.h5')





    def collect(self):


        #################### detection code inserted ################################################
 ###############################################################################################

        print("Start video stream")        

        stream_bytes = b' '  
        test = 0
        cnt = 0
        while True :
	        #print("WHY")
            stream_bytes += self.client.recv(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')



            if first != -1 and last != -1:
                test = test+1
                print("IN TRY", test)
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    
                print(image)
                print('type : ',type(image))
                print('shape : ', image.shape)

################# detection code inserted ##################

############################################################




                cv2.imshow('image',image)




                #print("RGB: ",rgb)

                #cv2.imshow('Origin', rgb)
                #cv2.waitKey(1)
                #cv2.imshow('GRAY', image)
                #cv2.imshow('roi', roi)
                #print("hihi3")
                # reshape the roi image into a vector
               #image_array = np.reshape(roi, (-1, 120, 320, 1))
                #print("hihi2")


                # neural network makes prediction
                #self.steer.Set_Line(self.model.predict(image_array))
                #self.steer.Set_Stopline(self.stopline.GetStopLine(roi2))
                #print(self.dect.Detection(rgb))
                #print("hihi")
                cnt = 0
                self.dect.Detection(image)
                #print("hi")

                #self.steer.Control()
                #cv2.imshow('rgb',rgb)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()	 # inserted (by hcw)


