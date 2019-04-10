# import socket
#
# s = socket.socket()
#
# host, port = "141.223.140.53", 8000
# s.connect((host, port))
#
# print("connected server")
# message = s.recv(1024)
# message = message.decode()
# print("server message : ",message )
#
# while True:
#     message = s.recv(1024)
#     message = message.decode()
#     print("Server :", message)
#     message = s.recv(1024)
#     message = message.decode()
#     print("Server :", message)
#     new_m = input(str(">>"))
#     new_m = new_m.encode()
#     s.send(new_m)
#     print("message sent")
#-------------------------------------------------------------------------------
import socket
import time
import numpy as np
import cv2



def run():
    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    args = Namespace(classes='yolov3.txt', config='yolov2-tiny.cfg', image='dog.jpg', weights='yolov2-tiny.weights')

    # ## Output layer and bounding box

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

    COLORS = np.array([[51.02963421, 133.33210769, 243.21725606],
                       [175.84209847, 51.30845697, 179.11109931],
                       [87.71116865, 118.79286966, 142.3107074],
                       [221.93125845, 134.73951486, 225.50682739],
                       [160.66609826, 109.05245608, 220.71611797],
                       [172.14284708, 227.02767372, 207.31092287],
                       [100.88719946, 176.33757786, 243.21681371],
                       [118.33613722, 157.97737042, 22.30523238],
                       [7.87220512, 59.17413697, 82.42727971],
                       [23.30564032, 38.03866174, 64.94689196],
                       [250.68080983, 160.64525038, 23.70661121],
                       [157.42862051, 45.60183636, 73.04253765],
                       [204.88386115, 158.5590442, 7.49485822],
                       [153.30325975, 194.22211248, 43.94264195],
                       [24.443527, 207.02444389, 86.28925182],
                       [177.86281262, 229.54239429, 238.02859077],
                       [30.32750733, 151.19679753, 235.06746624],
                       [152.29394858, 229.32799913, 224.7800965],
                       [139.01875714, 60.95063585, 33.75412714],
                       [89.74315504, 4.41759779, 95.23490135],
                       [121.95867644, 46.54851352, 224.22321081],
                       [164.75719154, 158.13917179, 219.74994688],
                       [88.82702365, 240.3289352, 176.20571055],
                       [66.22210166, 150.1864507, 43.21442604],
                       [97.79730681, 24.88929604, 207.55778166],
                       [231.61059723, 116.65931972, 95.46733961],
                       [91.67466539, 191.46970861, 62.80395932],
                       [129.35355711, 20.21365956, 190.32735102],
                       [30.82154964, 109.85094534, 62.47208679],
                       [198.81292514, 216.08068124, 98.77855703],
                       [150.83082811, 67.05161652, 223.88001489],
                       [234.7435867, 144.21300329, 77.93886089],
                       [215.44070549, 221.64511692, 51.4713609],
                       [209.58806089, 123.04680908, 124.95469042],
                       [152.21394944, 154.25946246, 94.73176147],
                       [102.89119635, 237.51149322, 97.82939056],
                       [93.91863668, 238.37570604, 153.47355921],
                       [186.14102532, 171.76714368, 0.32759317],
                       [51.99894721, 236.52210418, 94.1417523],
                       [106.30317512, 133.43582586, 84.88353712],
                       [243.46836362, 248.92235796, 193.1624906],
                       [35.37771852, 118.73359489, 139.5912857],
                       [139.17865758, 61.46453425, 19.81208161],
                       [95.15919741, 201.77822839, 101.59358138],
                       [176.74893368, 128.44628764, 158.31560417],
                       [24.49229873, 136.07366223, 75.7670816],
                       [32.42622061, 84.37027205, 73.52030149],
                       [120.83085304, 221.968001, 129.51259917],
                       [21.0619381, 30.22523229, 188.7046096],
                       [235.80576349, 63.07255008, 204.11696318],
                       [94.45990808, 125.20569527, 56.53701353],
                       [21.98673454, 154.22010394, 32.11283833],
                       [125.46709309, 78.06489605, 47.2445875],
                       [144.78989702, 164.68085518, 117.1023838],
                       [127.98914986, 189.40912356, 16.13464285],
                       [28.8359526, 116.37278856, 22.47771492],
                       [44.709084, 30.88764636, 224.95454936],
                       [187.94195205, 153.29370466, 242.20007673],
                       [55.23731237, 85.08356815, 100.04202217],
                       [28.07421156, 31.06845771, 60.95414536],
                       [122.74073537, 119.9328851, 49.65496121],
                       [98.14766034, 250.0906442, 202.58889644],
                       [116.51905631, 180.19283702, 244.52558348],
                       [247.61303245, 34.47071024, 49.56560581],
                       [92.72228188, 243.68344993, 36.45336036],
                       [95.22048531, 24.62595964, 196.53770396],
                       [252.4398534, 102.37398534, 196.42856599],
                       [117.67142907, 78.51168055, 223.17357968],
                       [28.3782576, 84.66857791, 63.21539142],
                       [138.58506004, 61.8768467, 210.14026469],
                       [251.91349101, 40.72830569, 75.56356924],
                       [230.1432278, 24.36708643, 90.14528852],
                       [227.10925836, 185.84055672, 50.18383877],
                       [213.83055978, 95.72752231, 156.63936992],
                       [77.1578319, 32.64124449, 51.38303349],
                       [7.10189597, 65.39100545, 232.04095494],
                       [206.08135209, 32.85295503, 211.63033976],
                       [227.78339302, 245.72611299, 50.43441173],
                       [174.25525604, 168.65350269, 79.74627319],
                       [199.39959392, 15.27040506, 193.4996962]])

    cap = cv2.VideoCapture(0)
    cnt = 0



    HOST = "141.223.140.44"
    PORT = 8020

    s = socket.socket()
    # socket create for camera
    s.connect((HOST, PORT))
    time.sleep(1)
    print("connected server")


    while True:

        # Capture frame-by-frame
        ret, image = cap.read()
        cnt += 1
        # Our operations on the frame come here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        Width = image.shape[1]
        Height = image.shape[0]
        scale = 0.00392

        # read class names from text file
        classes = None

        with open(args.classes, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        # generate different colors for different classes
        # COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

        # read pre-trained model and config file
        net = cv2.dnn.readNet(args.weights, args.config)

        # create input blob
        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

        # set input blob for the network
        net.setInput(blob)

        if cnt % 1 == 0:

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
                draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

        # Display the resulting frame (note : if change position, it doesn't draw bounding box)
        #cv2.imshow('frame', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            # s.send(image.encode())

            #capture = cv2.VideoCapture(0)
            #ret, image =capture.read()
            #stringData = data.tostring()

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.jpg', image, encode_param)
            print("IMAGE: ",image)
            #data = np.array(imgencode)

            ## ME!!!!
            b = bytearray(imgencode)
            s.sendall(b)
            #s.sendall(data)

            ## ME !!!!!!!!!!!!!!!!!!!!!!1

            '''
            stringData = data.tostring()
            print("Client Data: ", data)
            # String 형태로 변환한 이미지를 socket을 통해서 전송
            s.send(str(len(stringData)).ljust(16))
            s.send(stringData)
            s.close()

            decimg = cv2.imdecode(data, 1)
            cv2.imshow('CLIENT', decimg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
        #s.sendall(image)
    # When everything done, release the capture
    #cap.release()
    #cv2.destroyAllWindows()



if __name__ == "__main__":
    run()

