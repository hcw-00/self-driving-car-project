import socket

s = socket.socket()

host, port = "141.223.140.44", 8000
s.connect((host, port))

print("connected server")
message = s.recv(1024)
message = message.decode()
print("server message : ",message )
  
while True:
    message = s.recv(1024)
    message = message.decode()
    print("Server :", message)
    message = s.recv(1024)
    message = message.decode()
    print("Server :", message)
    new_m = input(str(">>"))
    new_m = new_m.encode()
    s.send(new_m)
    print("message sent")

