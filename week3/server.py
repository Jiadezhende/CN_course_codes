"""
UDP Ping-Pong Server

A simple UDP server that listens for 'ping' messages and responds with 'pong'.
"""

import socket
import datetime

HOST = "127.0.0.1"  # Localhost
PORT = 5500         # Port to listen on
BUFFER_SIZE = 1024  # Maximum message size

def main():
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        # Bind socket to address and port
        server.bind((HOST, PORT))
        print(f"[{datetime.datetime.now()}] Server listening on {HOST}:{PORT}")
        
        try:
            while True:
                # Receive message and client address
                data, client_address = server.recvfrom(BUFFER_SIZE)
                message = data.decode()
                
                # Print received message
                timestamp = datetime.datetime.now()
                print(f"[{timestamp}] Received from {client_address}: {message}")
                
                # Prepare and send response
                response = "pong"
                server.sendto(response.encode(), client_address)
                print(f"[{timestamp}] Sent to {client_address}: {response}")
                
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()