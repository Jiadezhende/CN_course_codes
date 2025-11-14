# a proxy server
# which extracts the server’s IP from the message and forward the message to the server.
# Once the server responds, the proxy forwards the message back to the client
# Besides, the proxy will block 

import json
import socket

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 6600
BUFFER_SIZE = 1024  # Maximum message size
BLOCKED_IPS = {"127.0.0.2", "10.0.0.1"}

def proxy_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_socket.bind((PROXY_HOST, PROXY_PORT))

        proxy_socket.listen(5)   # Listen for incoming connections (max 5 queued)
        print(f"Server is listening on {PROXY_HOST}:{PROXY_PORT}")

        try:
            while True:
                # Accept new connection
                client_socket, client_address = proxy_socket.accept()
                print(f"Connected by {client_address}")

                with client_socket:
                    while True:
                        # Receive data from client
                        data = client_socket.recv(BUFFER_SIZE)
                        if not data:
                            print(f"Client {client_address} disconnected")
                            break

                        # Decode and parse received message
                        message = data.decode()
                        print(f"Received from {client_address}: {message}")

                        # Extract server IP and actual message
                        try:
                            req = json.loads(data.decode())
                            server_ip = req["server_ip"]
                            server_port = req["server_port"]
                            message = req["message"]
                        except (json.JSONDecodeError, KeyError):
                            client_socket.sendall(b"Invalid JSON format")
                            continue

                        # Check blocklist
                        if server_ip in BLOCKED_IPS:
                            print(f"Blocked attempt to {server_ip}")
                            client_socket.sendall(b"Error: IP blocked")
                            continue

                        # Forward the message to the server
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                            server_socket.connect((server_ip, server_port))
                            server_socket.sendall(message.encode())
                            print(f"Forwarded to server {server_ip}:{server_port}: {message}")

                            # Receive response from the server
                            response = server_socket.recv(BUFFER_SIZE)
                            print(f"Received from server {server_ip}:{server_port}: {response.decode()}")

                        # Forward the response back to the client
                        client_socket.sendall(response)
        except KeyboardInterrupt:
            print("\nProxy server shutting down...")
            proxy_socket.close()

if __name__ == "__main__":
    proxy_server()