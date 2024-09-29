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
                tcpdump_command = ["sudo", "tcpdump", "-i", "wlo1", "-w", output_file]
                process = subprocess.Popen(tcpdump_command, stdout=devnull, stderr=devnull)

            global nazwapliku
            nazwapliku = output_file  # Ustawienie pełnej ścieżki pliku

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
    # Uzyskaj IP z nslookup
    print(urls)
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

    # Uzyskaj IP z pliku pcap
    file_path = filename
    ip_addresses = extract_ips_from_pcap(file_path)

    # Sprawdź, czy jakikolwiek IP odpowiada adresom uzyskanym z nslookup
    for ip in ip_addresses:
        if any(ip in ips for ips in results.values()):  # Sprawdź, czy IP jest w wynikach nslookup
            print(f"Adres IP: {ip} odpowiada stronie.")
            return ip  # Zwróć ten IP
    return None

def find_redirection_ip(ip, filename):
    packets = rdpcap(filename)

    for packet in packets:
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            if ip_dst == ip:
                return ip_src  # Zwróć adres IP źródłowy, który przekierowuje

def daemon_in_the_background():
    time.sleep(6)
    while True:
        for i in range(10):
            output_file = f"Packets/output_{i}.pcap"
            ip = look_for_suspicious_ips_in_file(output_file)
            if ip is not None:
                redirection_ip = find_redirection_ip(ip, output_file)
                print("Zostałeś przekierowany z " + redirection_ip)
            time.sleep(6)

# Rozpocznij przechwytywanie pakietów
capture_packets = threading.Thread(target=capture_tcp_packets)
capture_packets.start()

daemon_in_the_background()

# Zakończenie programu
capture_packets.join()
