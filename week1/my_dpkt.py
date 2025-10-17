"""
my_dpkt.py

PCAP IP extractor using dpkt.

This script opens a pcap file and collects all unique IP addresses
seen in the captured packets. It supports both IPv4 and IPv6.

Usage:
    python my_dpkt.py <pcap_file>
"""

import dpkt
import sys
import socket


def parse_pcap(pcap_file):
    # Open the pcap file for reading in binary mode
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    unique_ips = set()  # store unique IP addresses

    # Iterate through packets in the pcap
    for timestamp, data in pcap:
        try:
            # Parse Ethernet frame
            eth = dpkt.ethernet.Ethernet(data)

            # Skip packets that do not contain IPv4 or IPv6
            if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
                continue

            ip = eth.data

            # Handle IPv4 addresses
            if isinstance(ip, dpkt.ip.IP):
                src = socket.inet_ntoa(ip.src)
                dst = socket.inet_ntoa(ip.dst)
                unique_ips.add(src)
                unique_ips.add(dst)

            # Handle IPv6 addresses
            elif isinstance(ip, dpkt.ip6.IP6):
                src = socket.inet_ntop(socket.AF_INET6, ip.src)
                dst = socket.inet_ntop(socket.AF_INET6, ip.dst)
                unique_ips.add(src)
                unique_ips.add(dst)

        except Exception:
            # Skip packets that raise parsing errors
            continue

    f.close()

    # Print results to stdout
    print(f"Total unique IP addresses: {len(unique_ips)}")
    print("---------------------------------")
    for addr in sorted(unique_ips):
        print(addr)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No pcap file specified!")
    else:
        parse_pcap(sys.argv[1])
