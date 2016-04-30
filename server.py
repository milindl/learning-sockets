import socket,os
#Sage advice server

def start():
    host = "127.0.0.1"
    port = 7801

    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssock.bind((host,port))

    ssock.listen(1)


    while True:
        conn, addr = ssock.accept()
        advice =os.popen("fortune").read()
        conn.send(advice.encode())
        conn.close()
    ssock.close()
if __name__ == '__main__':
    start()
