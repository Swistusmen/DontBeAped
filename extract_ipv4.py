from scapy.all import rdpcap
import socket

def get_hostname(ip_address):
    try:
        # Uzyskiwanie nazwy hosta na podstawie adresu IP
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return None

def extract_ips_from_pcap(file_path):
    # Wczytanie pliku PCAP
    packets = rdpcap(file_path)
    ip_addresses = set()  # Używamy zbioru, aby uniknąć duplikatów

    # Iteracja przez pakiety i zbieranie adresów IPv4
    for packet in packets:
        if packet.haslayer('IP'):
            ip_addresses.add(packet['IP'].src)
            ip_addresses.add(packet['IP'].dst)

    return ip_addresses

def main():
    file_path = 'Packets/output_7.pcap'  # Zmień na ścieżkę do swojego pliku PCAP
    ip_addresses = extract_ips_from_pcap(file_path)

    print("Znalezione adresy IP i odpowiadające im hosty:")
    for ip in ip_addresses:
        hostname = get_hostname(ip)
        if hostname:
            print(f"Adres IP: {ip} odpowiada stronie: {hostname}")
        #else:
            #print(f"Adres IP: {ip} - brak odpowiadającej strony")

if __name__ == "__main__":
    main()