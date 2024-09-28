import subprocess
import time
import threading
import os


def capture_tcp_packets():
    while True:
        for i in range(10):
            os.makedirs("Packets", exist_ok=True)
            output_file = f"Packets/output_{i}.pcap"
            print(f"Rozpoczynanie nagrywania do {output_file}...")

            # Uruchomienie tcpdump z nadpisywaniem pliku
            tcpdump_command = ["sudo", "tcpdump", "-i", "en0", "-w", output_file]

            # Uruchomienie tcpdump w osobnym procesie
            process = subprocess.Popen(tcpdump_command)

            # Czekanie 3 sekundy
            time.sleep(3)

            # Zatrzymanie tcpdump
            process.terminate()
            print(f"Zakończono nagrywanie do {output_file}.")

capture_packets = threading.Thread(target=capture_tcp_packets)

capture_packets.start()

time.sleep(20)

capture_packets.join()