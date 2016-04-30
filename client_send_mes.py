import socket
#client, sender of messages
def start():
    host = '127.0.0.1'
    port = 7801

    sock = socket.socket()
    sock.connect((host,port))
    message = ''
    while message!='q':
        message = input('>>')
        sock.send(message.encode())

    sock.close()
    

if __name__ == '__main__':
    start()
