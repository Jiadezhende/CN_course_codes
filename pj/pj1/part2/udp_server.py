# This is a UDP server
# which measures the throughput (amount of data received / time taken to receive them)
# and sends it back to the client

import socket
import time

HOST ="127.0.0.1"   # local host
PORT = 6570
BUFFER_SIZE = 1024  # Maximum message size

def udp_server():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.settimeout(2.0)    # timeout to allow clean exit on Ctrl+C
    print(f"UDP server listening on {HOST,PORT}...")

    total_data = 0
    start_time = None

    try:
        while True:
            try:
                data, addr = serverSocket.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                # enter Ctrl+C to shut down the server
                continue
            if data == b"START":
                total_data = 0  # reset
                start_time = time.time()
                continue
            elif data == b"END":
                end_time = time.time()

                # Calculate throughput
                duration = end_time - start_time
                throughput_kbps = (total_data / 1024) / duration
                print(f"Received {total_data/1e6:.2f} MB in {duration:.2f} s")
                print(f"Throughput: {throughput_kbps:.2f} KB/s")

                # Send throughput back to client
                serverSocket.sendto(str(throughput_kbps).encode(), addr)
                total_data = 0
                continue

            total_data += len(data)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        serverSocket.close()

if __name__ == "__main__":
    udp_server()