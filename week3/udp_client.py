import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 52600

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
    message = b"Hello, UDP Server!"
    client.sendto(message, (SERVER_HOST, SERVER_PORT))

