import socket,time,threading,os
#Server, the receiver of messages
speaking_lk = threading.Lock()
currently_speaking=-1

def send_to_all(socket_list, mess):
    for sock in socket_list:
        sock.send(mess.encode())

def logger(con_socket, con_socket_num, socket_list):
    global currently_speaking
    '''
        Logs messages by printing them
    '''
    while True:
        data = con_socket.recv(1024).decode()
        speaking_lk.acquire()
        if not data or data=='':
            break

        string=''
        if currently_speaking==con_socket_num:
            string = '' +data

        if currently_speaking!=con_socket_num:
            string = ''+str(con_socket_num) + ":" + data
            currently_speaking = con_socket_num

        threading.Thread(target=send_to_all, args=(socket_list,string,)).start()
        #time.sleep(2)
        speaking_lk.release()
    con_socket.close()

def start():
    socket_list = []
    host = "127.0.0.1"
    port = 7801

    current_con_sock_num = 0
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind((host,port))

    ssock.listen(3)


    while True:
        conn, addr = ssock.accept()
        socket_list.append(conn)
        current_con_sock_num+=1
        t = threading.Thread(target=logger, args=(conn,current_con_sock_num, socket_list))
        t.start()
    ssock.close()


if __name__ == '__main__':
    currently_speaking = -1
    start()
