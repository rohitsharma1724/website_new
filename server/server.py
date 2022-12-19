from socket import AF_INET
from socket import socket
from socket import SOCK_STREAM
from threading import Thread
from Users import Users
import time


host_name = "localhost"
size = 1024
port_no = 5500
users = []
comm_server = socket(AF_INET, SOCK_STREAM)
comm_server.bind((host_name, port_no))  # set up server
comm_server.listen(10)
print("Setting the connections...")

def client_messages(user):

    socket_obj = user.client
    name = socket_obj.recv(size).decode("utf8")
    user.set_name(name)

    msg = f"{name} has joined the chat!".encode(encoding="utf8",errors="ignore")
    # broadcast(msg, "")  # broadcast welcome message
    # for person in users:
    #     client = person.client
    #     try:
    #
    #         client.send(str(name + msg.decode("utf8")).encode(encoding="utf8", errors="ignore"))
    #     except Exception as e:
    #         print("[EXCEPTION]+3", e)
    while True:
        try:
            msg = socket_obj.recv(size)
            print(type(msg))
            # print(msg+"1")
            if msg == "{quit}".encode(encoding="utf8",errors="ignore") :  # if message is qut disconnect client
                socket_obj.close()
                users.remove(user)
                print(f"{name} left the chat")
                # broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                for item in users:
                    #broadcasting the messages to each client
                    client = item.client
                    try:

                        client.send(str(name + msg.decode("utf8")).encode(encoding="utf8",errors="ignore"))
                    except Exception as e:
                        print("[EXCEPTION]+3", e)

                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:  # otherwise send message to all other clients
                # broadcast(msg, name+": ")
                print("coming")
                for person in users:
                    client = person.client
                    try:
                        msg=msg.decode("utf8")
                        # name=name.decode("utf8")
                        print(type(msg))
                        print(type(name))
                        client.send((name+": "+ msg).encode(encoding="utf8",errors="ignore"))
                    except Exception as e:
                        print(type(msg))
                        print(type(name))
                        client.send((name + ": " + msg).encode(encoding="utf8", errors="ignore"))
                        # print("[EXCEPTION]+ 0", e)
                print(f"{name}: ", msg)

        except Exception as e:
            print("[EXCEPTION]+2", e)
            break


def setting_connection():
    bool1 = True
    while bool1:
        try:
            addr, obj = comm_server.accept()
            #comm.accept() will wait for any connections are trying to connect
            user = Users(addr, obj)
            #creating the user for connection
            Thread_2 = Thread(target=client_messages, args=(user,))
            users.append(user)
            Thread_2.start()
        except Exception as e:
            bool1 = False
            print("exception with threads", e)


Thread1 = Thread(target=setting_connection)
Thread1.start()
Thread1.join()
comm_server.close()