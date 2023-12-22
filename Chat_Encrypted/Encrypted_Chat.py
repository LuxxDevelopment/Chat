import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Do you want to host (1) or to connect (2): ")

ip = "10.16.205.66"

if choice == "1":
    while True:
        port = input("Enter a port: ")
        try:
            port = int(port)
            break
        except ValueError:
            print("There was something worng try another number!")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen()
    client, addr = server.accept()
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    print("Connection Success \n")
elif choice == "2":
    while True:
        port = input("Enter a port: ")
        try:
            port = int(port)
            break
        except ValueError:
            print("There was something worng try another number!")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
    client.send(public_key.save_pkcs1("PEM"))
    print("Connection Success \n")
else:
    exit()


def recieving_message(c):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())


def sending_messages(c):
    while True:
        message = input("")
        try:
            if len(message) > 117:
                print("Message is to long! 117 Characters MAX")
            else:
                c.send(rsa.encrypt(message.encode(), public_partner))
        except:
            print("Well that didin't work out, try again!")
        if message == "§exit":
            c.close()

        # print("You: " + message)


threading.Thread(target=sending_messages, args=(client,)).start()
threading.Thread(target=recieving_message, args=(client,)).start()
