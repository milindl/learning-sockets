import socket

def start():
    host = "127.0.0.1"
    port = 7800

    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.bind((host,port))
    ssock.listen(1)
    conn, addr = ssock.accept()
    message = ''
    while True:
            data = conn.recv(1024).decode()
            if not data:
                    break
            message = message+data
    print(message)

    conn.close()

if __name__ == '__main__':
    start()
