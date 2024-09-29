import subprocess
from scapy.all import rdpcap, TCP, IP
import time
import threading
import os
import socket

urls = [
    "www.interia.pl",
    "www.wp.pl"
]

results = {}

nazwapliku = ''

def capture_tcp_packets():
    while True:
        for i in range(10):
            os.makedirs("Packets", exist_ok=True)
            output_file = f"Packets/output_{i}.pcap"

            with open(os.devnull, 'w') as devnull:
                tcpdump_command = ["sudo", "tcpdump", "-i", "en0", "-w", output_file]
                process = subprocess.Popen(tcpdump_command)

            global nazwapliku
            nazwapliku = f"output_{i}.pcap"

            time.sleep(6)

            process.terminate()
            process.wait() 

def nslookup(url):
    try:
        output = subprocess.check_output(["nslookup", url], universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e)
    
def get_hostname(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return None

def extract_ips_from_pcap(file_path):
    packets = rdpcap(file_path)
    ip_addresses = set()

    for packet in packets:
        if packet.haslayer('IP'):
            ip_addresses.add(packet['IP'].src)
            ip_addresses.add(packet['IP'].dst)

    return ip_addresses

def look_for_suspicious_ips_in_file(filename):
    file_path = filename
    ip_addresses = extract_ips_from_pcap(file_path)

    for ip in ip_addresses:
        hostname = get_hostname(ip)
        if hostname:
            print(f"Adres IP: {ip} odpowiada stronie: {hostname}")
            if ip in results:
                return ip
    return None

def find_redirection_ip(ip,filename):
    packets = rdpcap(filename)

    redirect_sources = set()

    for packet in packets:
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            if ip_dst == ip:
                redirect_sources.add(ip_src)
                return ip_src

def deamon_in_the_background():
    time.sleep(6)
    while True:
        for i in range(10):
            output_file = f"Packets/output_{i}.pcap"
            ip=look_for_suspicious_ips_in_file(output_file)
            if ip!=None:
                redirection_ip=find_redirection_ip(ip,output_file) #moze byc ryzyko ze trzeba bedzie isc wiecej niz 1 plik do tylu
                print("zostales przekierowany z "+ redirection_ip)
                #TODO tutaj leci robota
            time.sleep(6)

#getting list of ips which we are interested in
for url in urls:
    output = nslookup(url)
    ip_addresses = []
    for line in output.splitlines():
        if "Address:" in line and not line.startswith("***"):
            parts = line.split(":")
            if len(parts) > 1:
                ip_address = parts[1].strip()
                ip_addresses.append(ip_address)
    results[url] = ip_addresses

#starting capturing packets with tcpdump
capture_packets = threading.Thread(target=capture_tcp_packets)
capture_packets.start()

deamon_in_the_background()


#end of the program
capture_packets.join()





