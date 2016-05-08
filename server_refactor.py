import threading, socket

class CastServer:
    def __init__(self):
        self.speaking_lock = threading.Lock()
        self.sock_list = []
        self.current_speaker = -1
        self.send_q = []
        self.host = '127.0.0.1'
        self.port = 7801
        self.ssock = None

    def listen(self,sock):
        while True:
            data = sock.recv(1024).decode()
            if not data:
                self.sock_list.remove(sock)
                sock.close()
                break
            print(data)
            self.send_q.append(data)

    def sender(self):
        while True:
            if len(self.send_q) == 0:
                continue
            data = self.send_q.pop(0)
            with self.speaking_lock:
                for socket in self.sock_list:
                    socket.sendall(data.encode())

    def start(self):
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
