import socket,time,threading,os
#Server, the receiver of messages

def logger(con_socket, con_socket_num):
    '''
        Logs messages by printing them
    '''
    while True:
        data = con_socket.recv(10).decode()
        if not data or data=='': break
        print(str(con_socket_num) + ":" + data)
    con_socket.close()

def start():
    host = "127.0.0.1"
    port = 7801

    current_con_sock_num = 0
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind((host,port))

    ssock.listen(3)


    while True:
        conn, addr = ssock.accept()
        current_con_sock_num+=1
        t = threading.Thread(target=logger, args=(conn,current_con_sock_num))
        t.start()
    ssock.close()
if __name__ == '__main__':
    start()
