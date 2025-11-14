# This is a UDP client
# which sends 100 megabytes of data
# then prints the throughput value received from the server

import socket
import os
import sys

SERVER_HOST ="127.0.0.1"    # local host
SERVER_PORT = 6570
BUFFER_SIZE = 1024  # Maximum message size
TOTAL_SIZE = 100 * 1024 * 1024  # 100 MB

def udp_client(name):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_info = f" ({name})" if name else ""
    print(f"Client{client_info} started")

    clientSocket.sendto(b"START", (SERVER_HOST, SERVER_PORT))
    print("Sending 100 MB of data...")

    data_chunk = os.urandom(BUFFER_SIZE)    # randomly generated data
    bytes_sent = 0

    while bytes_sent < TOTAL_SIZE:
        clientSocket.sendto(data_chunk, (SERVER_HOST, SERVER_PORT))
        bytes_sent += len(data_chunk)
    
    clientSocket.sendto(b"END", (SERVER_HOST, SERVER_PORT))
    print("Data sent. Waiting for reply ...")

    throughput_data, _ = clientSocket.recvfrom(BUFFER_SIZE)
    print(f"Throughput received from server: {float(throughput_data.decode()):.2f} KB/s")

if __name__ == "__main__":
    client = sys.argv[1] if len(sys.argv) > 1 else ""
    udp_client(client)

