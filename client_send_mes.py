import socket, threading
#client, sender of messages
#input_and_print_lock  = threading.Lock()
def sender(sock):

    message = ''
    while message!='q\n':

        #input_and_print_lock.acquire()
        message = input('>>')
        message = message + '\n'
        #input_and_print_lock.release()
        sock.send(message.encode())


def receiver(sock):
    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
        input_and_print_lock.acquire()
        print("Recvd message follows: " + data)
        input_and_print_lock.release()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 7801

    sock = socket.socket()
    sock.connect((host,port))
    t1 = threading.Thread(target = sender, args = (sock,))
    t2 = threading.Thread(target = receiver, args = (sock,))
    t1.start()
    t2.start()
    while threading.active_count() > 1:
        pass
    sock.close()
