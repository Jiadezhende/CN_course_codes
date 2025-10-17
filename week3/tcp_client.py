"""
TCP Client

A simple TCP client that connects to the server and sends
periodic ping messages, then displays the server's response.

Usage:
    Make sure tcp_server.py is running first, then run this script.
"""

import socket
import time

SERVER_HOST = "127.0.0.1"  # Server hostname
SERVER_PORT = 52600        # Server port
INTERVAL = 5              # Seconds between pings

def main():
    print(f"Connecting to server at {SERVER_HOST}:{SERVER_PORT}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            # Connect to the server
            client.connect((SERVER_HOST, SERVER_PORT))
            print("Connected to server")
            
            # Send periodic ping messages
            while True:
                # Prepare and send message
                message = "ping"
                client.sendall(message.encode())
                print(f"Sent: {message}")
                
                # Receive and print server's response
                response = client.recv(1024).decode()
                print(f"Received: {response}")
                
                # Wait before sending next ping
                time.sleep(INTERVAL)
                
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Is it running?")
        except KeyboardInterrupt:
            print("\nClosing connection...")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()