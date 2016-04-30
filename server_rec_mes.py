import socket,time,threading,os
#Server, the receiver of messages
speaking_lk = threading.Lock()
currently_speaking=-1
def logger(con_socket, con_socket_num):
    global currently_speaking
    '''
        Logs messages by printing them
    '''
    while True:
        data = con_socket.recv(10).decode()
        speaking_lk.acquire()
        if not data or data=='':
            break


        if currently_speaking==con_socket_num:
            print('' +data, end='')

        if currently_speaking!=con_socket_num:
            print(''+str(con_socket_num) + ":" + data,end='')
            currently_speaking = con_socket_num
        #time.sleep(2)
        speaking_lk.release()
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
    currently_speaking = -1
    start()
