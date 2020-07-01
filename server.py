from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# global constants
HOST = 'localhost'
PORT = 5500
BUFSIZ = 512
MAX_CONNECTIONS = 5
ADDR = (HOST, PORT)
# global variables:
persons=[]
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)     #set up server

def broadcast(msg , name):
    """
    send new msg to all calientd
    :param msg:bytes["utf"]
    :param name:str
    :return:none
    """
    for person in persons:
        client=person.client
        try:
            client.send(bytes(name +": ","utf8" )+ msg)
        except Exception as e:
            print("[Exception]",e)

def client_communication(person):
    """
    thread to handle all the msgs from client
    :param person:Person
    :return:none
    """
    client = person.client
    # get persons name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg=bytes(f"{name} has joined the chat!","utf8")
    broadcast(msg,name)   #broadcasts welcome msg
    while True:
        try:
            msg = client.recv(BUFSIZ)

            if msg == bytes("{quit}", "utf8"):

                client.send(bytes("{quit}", "utf8")  )
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name}has left the chat..","utf8"),"")
                print(f"[DISCONNECTED]{name} disconnected")
                break
            else:
                broadcast(msg, name)
                print(f"{name}:", msg.decode("utf8"))
        except Exception  as e:
            print("[EXCEPTION]", e)
            break

def wait_for_connection():
    """wait for connection from new client,start new thread once connected
    param server=person
    return=none
    """
    while True:
        try:
            client, addr = SERVER.accept()  #wait for a new connection
            person = Person(addr, client)  #create new person fir connection
            persons.append(person)
            print(f"connected {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]", e)
            run = False
            print("server crash")


if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS)  # open server to listen for max connections
    print("waiting for connection..")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

