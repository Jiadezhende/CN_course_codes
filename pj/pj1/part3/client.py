import socket
import json

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 6600
BUFFER_SIZE = 1024

def tcp_client():
    data = {
        "server_ip": "127.0.0.1",
        "server_port": 7000,
        "message": "ping"
    }

    # # Blocked IP test
    # data = {
    #     "server_ip": "127.0.0.2",
    #     "server_port": 7000,
    #     "message": "ping"
    # }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((PROXY_HOST, PROXY_PORT))
        client_socket.sendall(json.dumps(data).encode())
        print(f"Client sent: {data}")
        response = client_socket.recv(BUFFER_SIZE)
        print(f"Client received: {response.decode()}")

if __name__ == "__main__":
    tcp_client()
