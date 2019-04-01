import server_socket
import threading

class Microphone(object):

    def __init__(self, host, port, steer):
        
        self.steer = steer
        self.socket = server_socket.Server(host, port)
        self.client = self.socket.Get_Client()
    

    def Recv(self) :
        while True :

            # 스레드를 돌면서 steer 객체의 microphone 변수를 갱신함
            speech = self.client.recv(128).decode()
            print('speech', speech)
            self.steer.Set_Microphone(speech)
    
    def Run(self) :
        # 코드를 병렬로 실행하기 위해서 스레드를 선언
        # target으로 설정된 함수 스레드가 실행함
        # 스레드가 실행하는 함수가 입력 파라미터가 필요한 경우 args에 선언함
        mic_thread = threading.Thread(target=self.Recv, args=())
        mic_thread.start()

    
