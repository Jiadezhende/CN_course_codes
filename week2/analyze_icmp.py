"""
analyze_icmp.py

Usage:
    python3 analyze_icmp.py <file_path>

Reads a pcap file and prints:
    a. Total ICMP packets captured
    b. Count of each ICMP type (Echo Request=8, Echo Reply=0, Time Exceeded=11)
    c. List of router IPs which sent Time Exceeded messages
"""
import sys
import socket
from collections import Counter

import dpkt

def analyze(pcap_path):
    # counters and containers
    total_icmp = 0
    ipv4_counter = Counter()   # keys: numeric icmpv4 types
    ipv6_counter = Counter()   # keys: numeric icmpv6 types
    time_exceeded_routers = set()  # store IP strings (v4 and v6)

    # Open the pcap file for reading in binary mode
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except Exception:
            continue

        ip = eth.data

        # IPv4 + ICMP
        if isinstance(ip, dpkt.ip.IP):
            # ip.data could be dpkt.icmp.ICMP or other protocols
            if isinstance(ip.data, dpkt.icmp.ICMP):
                icmp = ip.data
                total_icmp += 1
                icmp_type = getattr(icmp, "type", None)
                if icmp_type is None:
                    continue
                ipv4_counter[icmp_type] += 1

                # IPv4 Time Exceeded is type 11
                if icmp_type == 11:
                    try:
                        time_exceeded_routers.add(socket.inet_ntoa(ip.src))
                    except Exception:
                        pass

        # IPv6 + ICMPv6
        elif isinstance(ip, dpkt.ip6.IP6):
            # ip.data could be dpkt.icmp6.ICMP6 or other next-header data
            # dpkt represents ICMPv6 as dpkt.icmp6.ICMP6
            if hasattr(dpkt, "icmp6") and isinstance(ip.data, dpkt.icmp6.ICMP6):
                icmp6 = ip.data
                total_icmp += 1
                icmp6_type = getattr(icmp6, "type", None)
                if icmp6_type is None:
                    continue
                ipv6_counter[icmp6_type] += 1

                # ICMPv6 Time Exceeded is type 3
                if icmp6_type == 3:
                    try:
                        time_exceeded_routers.add(socket.inet_ntop(socket.AF_INET6, ip.src))
                    except Exception:
                        pass

        else:
            # not IPv4/IPv6
            continue

    f.close()

    # Print results
    print("=== ICMP Analysis ===\n")
    print(f"Total ICMP packets captured: {total_icmp}\n")

    # IPv4 interesting types
    print("IPv4 ICMP counts:")
    for t, name in [(8, "Echo Request (8)"), (0, "Echo Reply (0)"), (11, "Time Exceeded (11)")]:
        print(f"  {name}: {ipv4_counter.get(t, 0)}")

    print("\nIPv6 ICMP counts:")
    # ICMPv6 echo/types
    for t, name in [(128, "Echo Request (128)"), (129, "Echo Reply (129)"), (3, "Time Exceeded (3)")]:
        print(f"  {name}: {ipv6_counter.get(t, 0)}")

    # Routers that sent Time Exceeded (both v4 and v6)
    print("\nRouters that sent Time Exceeded messages:")
    if time_exceeded_routers:
        for ipstr in sorted(time_exceeded_routers):
            print(f"  {ipstr}")
    else:
        print("  (None captured)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_icmp.py <file_path>")
        sys.exit(1)
    pcap_file = sys.argv[1]
    analyze(pcap_file)
