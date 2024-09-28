import subprocess
from scapy.all import rdpcap, TCP, IP

# Lista adresów URL do sprawdzenia
urls = [
    "www.interia.pl",
    "www.wp.pl"
]

results = {}

def nslookup(url):
    try:
        # Uruchomienie polecenia nslookup
        output = subprocess.check_output(["nslookup", url], universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e)

# Przetwarzanie każdego adresu URL
for url in urls:
    print(f"Sprawdzam: {url}")
    output = nslookup(url)
    # Wydobycie adresów IP z wyników
    ip_addresses = []
    for line in output.splitlines():
        if "Address:" in line and not line.startswith("***"):
            # Bezpieczne wydobycie adresu IP
            parts = line.split(":")
            if len(parts) > 1:
                ip_address = parts[1].strip()
                ip_addresses.append(ip_address)

    # Dodanie wyników do słownika
    results[url] = ip_addresses
    # Wypisanie wyników
    print(f"Wyniki dla {url}: {ip_addresses}\n")

# Wypisanie końcowych wyników w strukturze
print("Ostateczne wyniki:")
for url, ips in results.items():
    print(f"{url}: {ips}")

def read_once_from_file():
    packets = rdpcap('output.pcap')

    # Adres IP strony do monitorowania
    monitored_ip = "217.74.72.58"  # Zmień na odpowiedni adres IP

    for packet in packets:
        if IP in packet and packet[IP].dst == monitored_ip:
            print(f"Pakiet z {packet[IP].src} do {packet[IP].dst}, port {packet[TCP].dport}")