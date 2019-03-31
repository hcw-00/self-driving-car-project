import numpy as np
import cv2
import argparse


import threading

import Object
#import StopLine

from model import NeuralNetwork

class CollectTrainingData(object):

    def __init__(self, client, steer):        
        import argparse

        self.client = client        
        self.steer = steer

        #self.args = Namespace(classes='yolov3.txt', config='yolov2-tiny.cfg', image='dog.jpg', weights='yolov2-tiny.weights')
        #self.stopline = StopLine.Stop()


        #self.dect = Object.Object_Detection(self.steer) # hcw

        # model create

        #self.model = NeuralNetwork()
        #self.model.load_model(path = 'model_data/video_model_1.h5')





    def collect(self):


        #################### detection code inserted ################################################



        # function to get the output layer names
        # in the architecture
        def get_output_layers(net):

            layer_names = net.getLayerNames()

            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            return output_layers

        # function to draw bounding box on the detected object with class name

        def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

            label = str(classes[class_id])

            color = COLORS[class_id]

            cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

            cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

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

#########################################
                
##########################################






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

                Width = image.shape[1]
                Height = image.shape[0]
                scale = 0.00392

                # read class names from text file
                classes = None

                with open('yolov3.txt', 'r') as f:
                    classes = [line.strip() for line in f.readlines()]

                # generate different colors for different classes
                COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

                # read pre-trained model and config file
                net = cv2.dnn.readNet('yolov2-tiny.weights', 'yolov2-tiny.cfg')

                # create input blob
                blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

                # set input blob for the network
                net.setInput(blob)

                if cnt % 10 == 0:

                    # run inference through the network
                    # and gather predictions from output layers
                    outs = net.forward(get_output_layers(net))

                    # initialization
                    class_ids = []
                    confidences = []
                    boxes = []
                    conf_threshold = 0.5
                    nms_threshold = 0.4

                    # for each detetion from each output layer
                    # get the confidence, class id, bounding box params
                    # and ignore weak detections (confidence < 0.5)

                    for out in outs:
                        for detection in out:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]
                            if confidence > 0.5:
                                center_x = int(detection[0] * Width)
                                center_y = int(detection[1] * Height)
                                w = int(detection[2] * Width)
                                h = int(detection[3] * Height)
                                x = center_x - w / 2
                                y = center_y - h / 2
                                class_ids.append(class_id)
                                confidences.append(float(confidence))
                                boxes.append([x, y, w, h])

                    # apply non-max suppression

                    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

                    # go through the detections remaining
                    # after nms and draw boundng box

                    for i in indices:
                        i = i[0]
                        box = boxes[i]
                        x = box[0]
                        y = box[1]
                        w = box[2]
                        h = box[3]
                        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w),
                                        round(y + h))

                ############################################################




                cv2.imshow('image',image)










#################################
#		inserted code start (by hcw)
#################################


##################################
#		inserted code end
##################################


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

                    #self.dect.Detection(rgb)
                    #print("hi")

                    #self.steer.Control()
                #cv2.imshow('rgb',rgb)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cv2.destroyAllWindows()	 # inserted (by hcw)


























