import numpy as np
import cv2
#import serial
import pygame
from pygame.locals import *
import socket
import time
import os


class CollectTrainingData(object):
    
    def __init__(self, host, port, input_size):



        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket.bind((host, port))

        self.server_socket.listen(1)

        # accept a single connection
        #self.connection = self.server_socket.accept()[0].makefile('rb')


        self.connection = self.server_socket.accept()[0]
        self.send_inst = True

        self.input_size = input_size

        # create labels
        self.k = np.zeros((7, 7), 'float')
        for i in range(7):
            self.k[i, i] = 1

        pygame.init()
        pygame.display.set_mode((250, 250))
        pygame.key.set_repeat(True)

    def collect(self):

        saved_frame = 0
        total_frame = 0

        # collect images for training
        print("Start collecting images...")
        print("Press 'q' or 'x' to finish...")
        start = cv2.getTickCount()

        X = np.empty((0, self.input_size))
        y = np.empty((0, 7))
        
        direction = 17
        # stream video frames one by one
        try:
            print("2")
            stream_bytes = b' '
            frame = 1
            cnt = 0
            while self.send_inst:
                #stream_bytes += self.connection.read(1024)
                print("3")
                stream_bytes += self.connection.recv(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]

                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.COLOR_BGR2HSV)


                    # select lower half of the image
                    height, width, rgb = image.shape
                    #roi = image[int(height/2):height, :]
                    roi = image[120:240, :]

                    cv2.imshow('roi', roi)
                    cv2.imshow('origin', image)

                    # reshape the roi image into a vector
                    temp_array = roi.reshape(1, int(height/2) * width * rgb).astype(np.float32)


                    frame += 1
                    total_frame += 1

                    # get input from human driver
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            key_input = pygame.key.get_pressed()

                            #complex orders
                            #if key_input[pygame.K_UP] and key_input[pygame.K_LEFT] and direction == 14:
                            if key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
                                print("Forward Left")

                                if direction -1 >= 14:
                                    direction -=1

                                #X = np.vstack((X, temp_array))
                                #y = np.vstack((y, self.k[direction-14]))
                                saved_frame += 1
                                self.connection.send(str(direction).encode())


                            #elif key_input[pygame.K_UP] and key_input[pygame.K_RIGHT] and direction == 18:
                            elif key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
                                print("Forward Right")

                                if direction + 1 <= 20:
                                    direction +=1

                                #X = np.vstack((X, temp_array))
                                #y = np.vstack((y, self.k[direction-14]))
                                saved_frame += 1
                                self.connection.send(str(direction).encode())

                            # simple orders
                            if key_input[pygame.K_UP] and (not key_input[pygame.K_LEFT]) and (not key_input[pygame.K_RIGHT]):
                                print("Forward")
                                saved_frame += 1
                                #X = np.vstack((X, temp_array))
				                #X = np.concatenate(
                                #y = np.vstack((y, self.k[direction-14]))
                                self.connection.send(str(direction).encode())

                            elif key_input[pygame.K_q]:
                                print("exit")
                                self.send_inst = False
                                self.connection.send('q'.encode())
                                self.connection.close()
                                break

                            elif key_input[pygame.K_s]:
                                print("stop")
                                self.connection.send('s'.encode())

                            elif key_input[pygame.K_f]:
                                print("reset")
                                #X = np.empty((0, self.input_size))
                                #y = np.empty((0, 7))

                        else : # key up
                            pass
                            #self.connection.send('s'.encode())

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            # save data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=X, train_labels=y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            # calculate streaming duration
            print("Streaming duration: , %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(X.shape)
            print(y.shape)
            print("Total frame: ", total_frame)
            print("Saved frame: ", saved_frame)
            print("Dropped frame: ", total_frame - saved_frame)

        finally:
            self.connection.close()
            self.server_socket.close()


if __name__ == '__main__':
    # host, port
    h, p = "141.223.140.53", 8000

    # serial port
    #sp = "/dev/tty.usbmodem1421"

    # vector size, half of the image
    s = 120 * 320
    print("1")
    ctd = CollectTrainingData(h, p, s)
    ctd.collect()
