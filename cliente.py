import socket
import threading
from tkinter import *
import tkinter as tk
from tkinter import simpledialog

class Chat:
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 55555

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        login = Tk()
        login.withdraw()

        self.janela_carregada = False
        self.ativo = True

        self.nome = simpledialog.askstring('Nome', 'Digite seu nome!', parent=login)
        self.sala = simpledialog.askstring('Sala', 'Digite a sala que deseja entrar!', parent=login)

        thread = threading.Thread(target=self.conecta)
        thread.start()
        self.janela()

# Function to create a window
    def janela(self):
        self.root = Tk() #To create a Tk
        self.root.geometry("800x800") #The size of this window
        self.root.title('Chat') #Just Title to this window

        self.caixa_texto = Text(self.root) #Kind of window are be created
        self.caixa_texto.place(relx=0.05, rely=0.01, width=700, height=600) #Size of window text message

        self.envia_mensagem = Entry(self.root) #To data entry
        self.envia_mensagem.place(relx=0.05, rely=0.8, width=500, height=20) 

        self.btn_enviar = Button(self.root, text='Enviar', command=self.enviarMensagem)
        self.btn_enviar.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)

        self.root.mainloop() #Need this to open the TK

    def fechar(self):
        self.root.destroy()
        self.client.close()

    def conecta(self):
        while True:
            recebido = self.client.recv(1024)
            if recebido == b'SALA':
                self.client.send(self.sala.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.caixa_texto.insert('end', recebido.decode())
                except:
                    pass

    def enviarMensagem(self):
        mensagem = self.envia_mensagem.get()
        self.client.send(mensagem.encode())
        self.envia_mensagem.delete(0, tk.END)
chat = Chat()

