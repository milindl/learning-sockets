import socket,time,threading
#Sage advice server

def magic_counter(con_socket):
    for i in range(10):
        con_socket.send(str(i).encode())
        time.sleep(0.5)
    con_socket.close()

def start():
    host = "127.0.0.1"
    port = 7801

    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind((host,port))

    ssock.listen(3)


    while True:
        conn, addr = ssock.accept()
        t = threading.Thread(target=magic_counter, args=(conn,))
        t.start()
    ssock.close()
if __name__ == '__main__':
    start()
