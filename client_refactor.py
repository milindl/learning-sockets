import threading, socket
import tkinter as tk

class AcceptClient:
    def __init__(self, host='127.0.0.1', port=7801):
        '''
        Constructor for the client
        __init__(host, port)
        '''
        self.window = tk.Tk()
        self.message_q = []
        self.main_txt = None
        self.entry_bar = None
        self.host = host
        self.port=port
        self.message_q_lock = threading.Lock()
        self.sock = socket.socket()


    def close_gracefully(self):
        '''
        Used to close the socket and destroy the window carefully.
        close_gracefully():None
        '''
        self.sock.close()
        self.window.destroy()


    def send(self,event):
        '''
        Used to send a message to the server.
        Clears the gui also.
        Is an event handler too, for the event "Return"
        send(self, event)
        send(event)
        send()
        :None
        '''
        message = self.entry_bar.get()
        self.entry_bar.delete(0,tk.END)
        message+='\n'
        message = message.encode()
        self.sock.send(message)

    def receive(self):
        '''
        The recieve thread. Listens at the host and port and then appends the message to the incoming message q.
        recieve():None
        '''
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            with self.message_q_lock:
                self.message_q.append(data)

    def receive_display(self):
        '''
        Takes messages from the message_q and appends it to the text area.
        Uses after-polling mechanism.
        Possible TODO: using threading with Tk..?
        receive_display():None
        '''
        self.message_q_lock.acquire()
        while len(self.message_q) != 0:
            mes = self.message_q.pop(0)
            self.main_txt.insert(tk.END, mes)
        self.message_q_lock.release()
        self.window.after(100, self.receive_display)

    def setup_gui(self):
        '''
        This sets up the gui.
        setup_gui():None
        '''
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
        '''
        Starts reciever thread and mainloop.
        start():None
        '''
        self.sock.connect((self.host,self.port))
        threading.Thread(target=self.receive, daemon=True).start()
        self.window.after(100, self.receive_display)
        self.window.mainloop()


c = AcceptClient()
c.setup_gui()
c.start()
