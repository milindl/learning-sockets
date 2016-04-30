import socket

def start():
    host = '127.0.0.1'
    port = 7801

    sock = socket.socket()
    sock.connect((host,port))
    total_data = []
    while True:
        data = sock.recv(8)
        if data=='' or not data:
            break
        total_data.append(data.decode())
        print(data.decode())
    sock.close()
    print(''.join(total_data))


if __name__ == '__main__':
    start()
