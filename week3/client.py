"""
UDP Ping-Pong Client

A simple UDP client that sends 'ping' messages to the server
and receives 'pong' responses back. Can include an optional
client name in the ping messages.

Usage:
    python client.py [client_name]
"""

import socket
import sys
import time
import datetime

SERVER_HOST = "127.0.0.1"  # Server hostname
SERVER_PORT = 5500         # Server port
BUFFER_SIZE = 1024        # Maximum message size
INTERVAL = 1              # Seconds between pings

def main():
    # Get optional client name from command line
    client_name = sys.argv[1] if len(sys.argv) > 1 else ""
    
    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client_info = f" ({client_name})" if client_name else ""
        print(f"[{datetime.datetime.now()}] Client{client_info} started")
        
        try:
            while True:
                # Prepare and send message
                message = f"ping {client_name}" if client_name else "ping"
                client.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
                timestamp = datetime.datetime.now()
                print(f"[{timestamp}] Sent: {message}")
                
                # Receive response from server
                data, _ = client.recvfrom(BUFFER_SIZE)
                response = data.decode()
                timestamp = datetime.datetime.now()
                print(f"[{timestamp}] Received: {response}")
                
                # Wait before next ping
                time.sleep(INTERVAL)
                
        except KeyboardInterrupt:
            print(f"\nClient{client_info} shutting down...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()