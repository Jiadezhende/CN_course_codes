"""
TCP Server

A simple TCP server that listens for incoming connections and
echoes back any received messages.

Usage:
    Run this script first, then run tcp_client.py to connect to it.
"""

import socket

HOST = "127.0.0.1"  # Localhost
PORT = 52600        # Port to listen on

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Configure socket for reuse (avoid "Address already in use" error)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to the address and port
        server.bind((HOST, PORT))
        
        # Listen for incoming connections (max 5 queued)
        server.listen(5)
        print(f"Server is listening on {HOST}:{PORT}")
        
        while True:
            # Accept new connection
            client_socket, client_address = server.accept()
            print(f"Connected by {client_address}")
            
            with client_socket:
                while True:
                    # Receive data from client
                    data = client_socket.recv(1024)
                    if not data:
                        # Connection closed by client
                        print(f"Client {client_address} disconnected")
                        break
                    
                    # Decode and print received message
                    message = data.decode()
                    print(f"Received from {client_address}: {message}")
                    
                    # Echo back the message
                    response = f"Server received: {message}"
                    client_socket.sendall(response.encode())

if __name__ == '__main__':
    main()
    