import socket

if __name__ == "__main__":
    udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpsocket.bind(('', 12345))

    while True:
        msg, sender = udpsocket.recvfrom(50)
        print(msg.decode('utf-8'))

