import threading, socket
import tkinter as tk

class AcceptClient:
    def __init__(self):
        self.window = tk.Tk()
        self.main_txt = None
        self.entry_bar = None
        self.host = '127.0.0.1'
        self.port=7801
        self.sock = socket.socket()

    def send(self,event):
        message = self.entry_bar.get()
        message+='\n'
        message = message.encode()


    def setup_gui(self):
        self.window.title("Chat Interface")
        self.window.geometry('900x500')
        upper_frame =  tk.Frame()
        lower_frame = tk.Frame()
        scroller = tk.Scrollbar(upper_frame)
        self.main_txt = tk.Text(upper_frame, yscrollcommand=scroller.set, height=1000)
        scroller.config(command=self.main_txt.yview)
        self.entry_bar = tk.Entry(lower_frame)
        #entry.bind('<Return>', send_mess)
        self.entry_bar.focus()
        self.main_txt.pack(fill=tk.X, side=tk.TOP)
        scroller.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_bar.pack(fill = tk.BOTH)
        lower_frame.pack(fill=tk.X, side=tk.BOTTOM)
        upper_frame.pack(fill=tk.X, side=tk.TOP)
        #window.protocol("WM_DELETE_WINDOW", close_gracefully)
        #gui_setup_lock.release()

    def start(self):
        self.sock.connect((self.host,self.port))
        self.window.mainloop()


if __name__=='__main__':
    c = AcceptClient()
    c.setup_gui()
    c.start()
