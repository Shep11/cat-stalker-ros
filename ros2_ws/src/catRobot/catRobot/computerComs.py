import cv2
import socket
import pickle
import argparse

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.7.56"
ADDR = (SERVER, PORT)

def send(msg, client):
    message = msg
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--server")
    args = parser.parse_args()
    SERVER = args.server
    cap = cv2.VideoCapture(0)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    ret, frame = cap.read()
    send(pickle.dumps(frame), client)
    input()
    while cap.isOpened():
        ret, frame = cap.read()
        send(pickle.dumps(frame), client)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()


