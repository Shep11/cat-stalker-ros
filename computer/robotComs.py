import socket
import pickle
import cv2

# msg lenght
HEADER = 64

PORT = 5500

SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

FORMAT = 'utf-8'

IMGTEXT = "!IMG"

DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            if msg_length > 4096:
                msgb = b""
                while msg_length > 4096:
                    pack = conn.recv(4096)
                    msg_length -= 4096
                    msgb += pack
                pack = conn.recv(msg_length)
                msgb += pack
                msg = pickle.loads(msgb)
            else:
                msg = pickle.loads(conn.recv(msg_length))
            cv2.imshow("resutlt.jpg", msg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    conn.close()

def start():
    server.listen()
    print(f"[LISTENTING] Server is listenting on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

print("[Starring] starting the server ...")
start()
