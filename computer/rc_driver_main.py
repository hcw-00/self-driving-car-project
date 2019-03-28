import server_video
#import server_ultra
#import server_microphone
import server_steer
import server_socket

import threading

if __name__ == '__main__':
    # host, port
    host, port = "141.223.140.53", 8000
    print("1")
    client = server_socket.Server(host, port)
    print("2")
    # 주행 로직을 가진 객체 선언
    steer = server_steer.Steer(client.Get_Client())
    
#-----------------------------------------------------------------------------------
    print("3")
    # 초음파 스레드를 실행시켜 초음파 데이터를 받아옴
#    ultrasonic_object = server_ultra.UltraSonic(host, port+1, steer)
#    ultrasonic_object.Run()

    # 마이크 스레드를 실행시켜 음성 데이터를 받아옴
#    microphone_object = server_microphone.Microphone(host, port+2, steer)
#    microphone_object.Run()

    # loop
    # 이미지 데이터를 받아 주행모델, YOLO, 정지선 검출을 실행함
    video_object = server_video.CollectTrainingData(client.Get_Client(), steer)
    video_object.collect()



#rc_driver_main -> server_socket -> steer_server -> server_video (while loop)
#rc_driver_main -> server_socket -> steer_server -> server_microphone (while loop)
#rc_driver_main -> server_socket -> steer_server -> server_ultra (while loop)
