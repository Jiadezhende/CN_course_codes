import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000
BUFFER_SIZE = 1024

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(BUFFER_SIZE)
            if not data:
                continue
            message = data.decode()
            print(f"Server received: {message}")
            if message.lower() == "ping":
                conn.sendall(b"pong")
            else:
                conn.sendall(b"unknown")

if __name__ == "__main__":
    tcp_server()
