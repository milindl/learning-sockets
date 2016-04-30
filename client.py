import socket


host = '127.0.0.1'
port = 7800

sock = socket.socket()
sock.connect((host,port))

message = input("->")

sock.send(message.encode())
sock.close()
