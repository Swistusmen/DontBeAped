from scapy.all import rdpcap, IP, TCP

packets = rdpcap('Packets/output_7.pcap')


blik_ip = "216.58.215.67"  # Zmień na odpowiedni adres IP Blika


redirect_sources = set()

for packet in packets:
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        # Sprawdzamy, czy pakiet jest do Blika
        if ip_dst == blik_ip:
            redirect_sources.add(ip_src)
            print(f"Przekierowanie z {ip_src} do {ip_dst}")

print("\nUnikalne źródła przekierowania:")
for source in redirect_sources:
    print(source)