import socket
import cv2
import numpy as np
from PIL import Image
import io

s = socket.socket()

host, port = "141.223.140.44", 8020
s.bind((host, port))
s.listen(1)
print("waiting for connections..")
conn, addr = s.accept()
print("client 1 has connected..")

#socket 수신 버퍼를 읽어서 반환하는 함수
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

while True:
    #while True:
    # stream_bytes = b' '
    # test = 0
    #
    # stream_bytes += conn.recv(1024)
    # first = stream_bytes.find(b'\xff\xd8')
    # last = stream_bytes.find(b'\xff\xd9')
    # if first != -1 and last != -1:
    #     try:
    #         test = test + 1
    #         print("IN TRY", test)
    #         jpg = stream_bytes[first:last + 2]
    #         stream_bytes = stream_bytes[last + 2:]
    #
    #         rgb = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
    #
    #         cv2.imshow('Origin', rgb)
    #         cv2.waitKey(1)
    #     except:
    #         continue


    # String형의 이미지를 수신받아서 이미지로 변환 하고 화면에 출력
    #length = recvall(conn, 16)  # 길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
    #stringData = recvall(conn, int(length))
    #data = np.fromstring(stringData, dtype='uint8')
    # s.close()
    #decimg = cv2.imdecode(data, 1)
    init = True
    ## ME!!!!
    while True:
        byte_image = conn.recv(65536)
        image = Image.open(io.BytesIO(byte_image))
        #image_total += image
        image.show()


    '''
    length = recvall(conn, 16)  # 길이 16의 데이터를 먼저 수신하는 것은 여기에 이미지의 길이를 먼저 받아서 이미지를 받을 때 편리하려고 하는 것이다.
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')
    print("DATA: ",data)
    s.close()
    decimg = cv2.imdecode(data, 1)
    cv2.imshow('SERVER', decimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    #cv2.imshow('SERVER', image)
    ## ME !!!!!!!!!!!!!!!!!!!!!!1

    #cv2.imshow('SERVER', decimg)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break