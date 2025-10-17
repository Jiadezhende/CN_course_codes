import socket
HOST ="127.0.0.1"
PORT = 52600

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    data, addr = server.recvfrom(1024) # buffer size is 1024 bytes
    print(f"Data reveived: {data.decode()}")
    print(f"From address: {addr}")