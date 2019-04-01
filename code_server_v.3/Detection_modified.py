import numpy as np
import cv2
import argparse
import Namespace


#class Namespace:
#    def __init__(self, **kwargs):
#        self.__dict__.update(kwargs)
#

class Object_Detection(object):

    def __init__(self):
        
        self.cnt = 0
        self.classes = None
        self.COLORS = None        
        
        
    # function to get the output layer names
    # in the architecture
    def get_output_layers(self, net):
        
        layer_names = net.getLayerNames()
        
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        
        return output_layers


    # function to draw bounding box on the detected object with class name

    def draw_prediction(self, img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        
        label = str(self.classes[class_id])
        
        color = self.COLORS[class_id]
        
        cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
        
        cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


    # ## Webcam

    # # generate different colors for different classes
    # COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    def Detection(self, image):
        
        #args =    {'classes': 'yolov3.txt', 'config': 'yolov2-tiny.cfg', 'image': 'dog.jpg', 'weights'='yolov2-tiny.weights'}
        
        
        args = Namespace.Namespace(classes='yolov3.txt', config='yolov2-tiny.cfg', image='dog.jpg', weights='yolov2-tiny.weights')

        
        
#        cap = cv2.VideoCapture(0)
#        cnt = 0
#        while(True):
        # Capture frame-by-frame
#        ret, image = cap.read()
        self.cnt += 1
        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        self.image = image
        
        Width = self.image.shape[1]
        Height = self.image.shape[0]
        scale = 0.00392
        
        
        
        # read class names from text file
        #classes = None
        
        with open(args.classes, 'r') as f:
            self.classes = [line.strip() for line in f.readlines()]


        # generate different colors for different classes
        self.COLORS = np.random.uniform(0, 255, size=(len(self.classes), 3))
        # read pre-trained model and config file
        net = cv2.dnn.readNet(args.weights, args.config)
        #create input blob
        blob = cv2.dnn.blobFromImage(self.image, scale, (416,416), (0,0,0), True, crop=False)
        # set input blob for the network
        net.setInput(blob)
        if self.cnt%1 == 0:
            # run inference through the network
            # and gather predictions from output layers
            outs = net.forward(self.get_output_layers(net))
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
                self.draw_prediction(self.image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))


        # Display the resulting frame (note : if change position, it doesn't draw bounding box)
        cv2.imshow('frame',image)

#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#
#    # When everything done, release the capture
#    cap.release()
#    cv2.destroyAllWindows()

