from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread,Lock
import time


class Client:
    """
    for connnection with server

    """
    # global constants
    HOST = 'localhost'
    PORT = 5500
    BUFSIZ = 512
    MAX_CONNECTIONS = 5
    ADDR = (HOST, PORT)
    def  __init__(self, name):
        """
        INIT object and send msg to server
        :param name:str
        """


        self.client_socket =socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages=[]

        receive_thread = Thread(target=self.recieve_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()




    def recieve_messages(self):
        while True:
            try:
                msg=self.client_socket.recv(self.BUFSIZ).decode()
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[Exception]",e)
                break

    def send_message(self,msg):
        """
        send msgs to server
        :param msg:str
        :return:None
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        :returns a list of str messages
        :return:list[str]
        """
        msgs=self.messages[:]

        #make sure that the memory is safe to read from
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return msgs


    def disconnect(self):
        self.send_message("{quit}")