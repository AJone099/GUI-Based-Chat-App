from tkinter import *
from threading import Thread
import socket

class GUI:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 55555))
        
        self.Window = Tk()
        self.Window.withdraw()
        
        self.login = Toplevel()
        self.login.title("Login")
        self.login.geometry("400x300")
        self.login.configure(bg="lightgrey")
        
        self.login_label = Label(self.login, text="Please login to continue", font=("Helvetica", 14), bg="lightgrey")
        self.login_label.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        self.name_label = Label(self.login, text="Name:", font=("Helvetica", 12), bg="lightgrey")
        self.name_label.place(relx=0.3, rely=0.5, anchor=E)
        
        self.entryName = Entry(self.login, font=("Helvetica", 12))
        self.entryName.place(relx=0.5, rely=0.5, anchor=W)
        
        self.go = Button(self.login,
                         text="Continue",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.5, rely=0.7, anchor=CENTER)
        
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.name = name
        rcv = Thread(target=self.receive)
        rcv.start()
        self.layout(name)

    def layout(self, name):
        self.name = name
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#17202A")
        
        self.labelHead = Label(self.Window, bg="#17202A", fg="#EAECEE", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)
        
        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        
        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)
        
        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()
        
        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        
        self.textCons.config(cursor="arrow")
        
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = Thread(target=self.write)
        snd.start()

    def show_message(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message + "\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            try:
                message = self.client.recv(2048).decode("utf-8")
                if message == "NICKNAME":
                    self.client.send(self.name.encode("utf-8"))
                else:
                    self.show_message(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def receive(self):
        while True:
            try:
                message = self.client.recv(2048).decode("utf-8")
                if message == "NICKNAME":
                    self.client.send(self.name.encode("utf-8"))
                else:
                    self.show_message(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

if __name__ == "__main__":
    gui = GUI()