from client.client import Client
import time
from threading import Thread


def update_message():
    """
    update the current list of msgs
    :return:
    """
    msgs=[]
    run = True
    while True:
        time.sleep(0.1)
        new_messages=c1.get_messages()
        msgs.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg =="{quit}":
                run = False
                break

Thread(target=update_message).start()

c1=Client("Anurag")
c2=Client("garima")

c1.send_message("aihbv")
time.sleep(1)
c2.send_message("hello")
time.sleep(1)

c1.send_message("qejfna;ekl")
time.sleep(1)
c2.send_message("eqrgqergqg")
time.sleep(1)

c1.send_message("hwgwgwv")

time.sleep(1)

c2.send_message("wanna come over?")

time.sleep(1)
c1.send_message("sure why not")

time.sleep(5)
c1.disconnect()
time.sleep(2)
c2.disconnect()
