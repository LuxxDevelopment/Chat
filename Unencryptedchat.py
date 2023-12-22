import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Do you want to host (1) or to connect (2): ")

if choice == "1":
    while True:
        port = input("Enter a port: ")
        try:
            port = int(port)
            break
        except ValueError:
            print("There was something worng try another number!")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("10.16.205.66", port))
    server.listen()
    client, addr = server.accept()
elif choice == "2":
    while True:
        port = input("Enter a port: ")
        try:
            port = int(port)
            break
        except ValueError:
            print("There was something worng try another number!")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", port))
else:
    exit()


def recieving_message(c):
    while True:
        print("Partner: " + c.recv(1024).decode())


def sending_messages(c):
    while True:
        message = input("")
        c.send(message.encode())
        # print("You: " + message)


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=recieving_message, args=(client,)).start()
