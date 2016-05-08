import threading, socket
import tkinter as tk

class AcceptClient:
    def __init__(self):
        self.window = tk.Tk()
        self.message_q = []
        self.main_txt = None
        self.entry_bar = None
        self.host = '127.0.0.1'
        self.port=7801
        self.message_q_lock = threading.Lock()
        self.sock = socket.socket()


    def close_gracefully(self):
        self.sock.close()
        self.window.destroy()


    def send(self,event):
        message = self.entry_bar.get()
        self.entry_bar.delete(0,tk.END)
        message+='\n'
        message = message.encode()
        self.sock.send(message)

    def receive(self):
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            with self.message_q_lock:
                self.message_q.append(data)

    def receiveq(self):
        self.message_q_lock.acquire()
        while len(self.message_q) != 0:
            mes = self.message_q.pop(0)
            self.main_txt.insert(tk.END, mes)
        self.message_q_lock.release()
        self.window.after(100, self.receiveq)

    def setup_gui(self):
        self.window.title("Chat Interface")
        self.window.geometry('900x500')
        upper_frame =  tk.Frame()
        lower_frame = tk.Frame()
        scroller = tk.Scrollbar(upper_frame)
        self.main_txt = tk.Text(upper_frame, yscrollcommand=scroller.set, height=1000)
        scroller.config(command=self.main_txt.yview)
        self.entry_bar = tk.Entry(lower_frame)
        self.entry_bar.bind('<Return>', self.send)
        self.entry_bar.focus()
        self.main_txt.pack(fill=tk.X, side=tk.TOP)
        scroller.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_bar.pack(fill = tk.BOTH)
        lower_frame.pack(fill=tk.X, side=tk.BOTTOM)
        upper_frame.pack(fill=tk.X, side=tk.TOP)
        self.window.protocol("WM_DELETE_WINDOW", self.close_gracefully)
        #gui_setup_lock.release()

    def start(self):
        self.sock.connect((self.host,self.port))
        threading.Thread(target=self.receive, daemon=True).start()
        self.window.after(100, self.receiveq)
        self.window.mainloop()


c = AcceptClient()
c.setup_gui()
c.start()
