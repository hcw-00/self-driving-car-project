import socket
import sys
from typing import List

import cv2
import pickle
import numpy as np
import struct ## new
import zlib

HOST = "141.223.140.44"
PORT = 8088
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')

s.listen(10)
conn = s.accept()[0]
print('Socket now listening')

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)

    print(data)
    x = data[-3:]
    data = data[:-3]

    #print(data)
    print("X =", x.decode())
    print(x.decode(encoding='utf-8'))

    print("Type of Data:", type(data))
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    #frame = cv2.imdecode(frame, cv2.IMREAD_GRAYSCALE)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    # if the object in the range,
    #if x == '90':
    #    pass
    #else:
    cv2.imshow('Image in Server', frame)
    cv2.waitKey(1)