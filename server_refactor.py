import threading, socket

class CastServer:
    '''
    This server accepts requests from multiple clients and broadcasts whatever one client sends to the server.
    Need to add : a pipe to process the incoming message to do MAFIA
    '''
    def __init__(self, host='127.0.0.1', port=7801):
        '''
        Initialize CastServer attributes
        __init__(host, port) : Returns None
        '''
        self.speaking_lock = threading.Lock()
        self.send_q_event = threading.Event()
        self.send_q_event_lock = threading.Lock()
        self.sock_list = []
        self.current_speaker = -1
        self.send_q = []
        self.host = host
        self.port = port
        self.ssock = None

    def listen(self,sock):
        '''
        Listens from specific client socket and decodes the message. Appends message to send_q.
        listen(socket):None
        '''
        while True:
            data = sock.recv(1024).decode()
            if not data:
                self.sock_list.remove(sock)
                sock.close()
                break
            print(data)
            self.send_q.append(data)
            with self.send_q_event_lock:
                if not self.send_q_event.is_set():
                    self.send_q_event.set()

    def sender(self):
        '''
        Sends to all connected client sockets - messages from the send_q
        Keeps sending - it's a thread!
        sender():None
        '''
        while True:
            self.send_q_event.wait()
            data = self.send_q.pop(0)
            with self.speaking_lock:
                for socket in self.sock_list:
                    socket.sendall(data.encode())
            self.send_q_event.clear()

    def start(self):
        '''
        Workhorse method of the class. Sets up the server socket, starts the sender thread to listen to the send_q
        Listens on ssock for new client sockets.
        start():None
        '''
        self.ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ssock.bind((self.host,self.port))
        self.ssock.listen(1)
        threading.Thread(target=self.sender).start()
        while True:
            conn, add = self.ssock.accept()
            self.sock_list.append(conn)
            threading.Thread(target=self.listen, args=(conn,)).start()
        self.ssock.close()

if __name__=='__main__':
    CastServer().start()
