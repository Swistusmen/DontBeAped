from scapy.all import sniff, TCP, Raw

# Funkcja do analizy pakietów
def packet_callback(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors="ignore")
        print("Przechwycony pakiet:")
        print(payload)  # Wyświetl surowe dane

        if "HTTP" in payload:
            lines = payload.splitlines()
            for line in lines:
                if line.startswith("GET") or line.startswith("POST"):
                    url_part = line.split(" ")[1]
                    print("Odwiedzana strona:", url_part)
                    break
                if "Host:" in line:
                    host = line.split(":")[1].strip()
                    full_url = f"http://{host}{url_part}"
                    print("Odwiedzana strona:", full_url)

# Rozpoczęcie przechwytywania pakietów
sniff(filter="tcp port 80", prn=packet_callback, store=0)
