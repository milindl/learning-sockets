import socket, threading,tkinter

sock=None
txt_area=None
#client, sender of messages
#input_and_print_lock  = threading.Lock()
gui_setup_lock = threading.Lock()
def send_mess(event):
    global sock
    message =  event.widget.get()
    sender(sock,message)
    event.widget.delete(0,tkinter.END)


def sender(sock,message=''):
    message = message + '\n'
    sock.send(message.encode())


def receiver(sock):
    global txt_area
    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
        #input_and_print_lock.acquire()

        print("Recvd message follows: " + data)
        if txt_area:
            print('yo ho ho and a bottle of rum')
            txt_area.insert(tkinter.END,data)

        #input_and_print_lock.release()

def setup_gui():
    global txt_area
    #gui_setup_lock.acquire()
    #Setup the largest level widgets first
    window = tkinter.Tk()
    window.title("Chat Interface")
    window.geometry('900x500')
    upper_frame =  tkinter.Frame()
    lower_frame = tkinter.Frame()
    scroller = tkinter.Scrollbar(upper_frame)
    main_txt = tkinter.Text(upper_frame, yscrollcommand=scroller.set, height=1000)
    #main_txt.config(state=tkinter.DISABLED)
    scroller.config(command=main_txt.yview)
    entry = tkinter.Entry(lower_frame)
    entry.bind('<Return>', send_mess)
    entry.focus()
    main_txt.pack(fill=tkinter.X, side=tkinter.TOP)
    scroller.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    entry.pack(fill = tkinter.BOTH)
    lower_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)
    upper_frame.pack(fill=tkinter.X, side=tkinter.TOP)
    txt_area=main_txt
    main_txt.insert(tkinter.END,"Yo ho ho and a bottle of rum")
    #gui_setup_lock.release()
    window.mainloop()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 7801

    sock = socket.socket()
    sock.connect((host,port))
    #t1 = threading.Thread(target = sender, args = (sock,))
    t2 = threading.Thread(target = receiver, args = (sock,))
    t2.start()
    setup_gui()

    while threading.active_count() > 1:
        pass
    sock.close()
