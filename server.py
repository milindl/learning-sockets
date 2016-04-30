import socket,time,threading,os
#Sage advice server

def magic_counter(con_socket):
    '''
        Sends 0 - 10 to socket and closes it. TODO: check if socket is unclosed initially
    '''
    for i in range(10):
        con_socket.send(str(i).encode())
        time.sleep(0.5)
    con_socket.close()

def magic_fortune(con_socket):
    '''
        Delivers fortune result to con_socket. TODO: check if socket is unclosed initially.
    '''
    advice = os.popen("fortune").read()
    con_socket.send(advice.encode())
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
        t = threading.Thread(target=magic_fortune, args=(conn,))
        t.start()
    ssock.close()
if __name__ == '__main__':
    start()
