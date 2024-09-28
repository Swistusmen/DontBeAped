import subprocess
import time
import threading
import os

nazwapliku = ''

def capture_tcp_packets():
    while True:
        for i in range(10):
            os.makedirs("Packets", exist_ok=True)
            output_file = f"Packets/output_{i}.pcap"
            # print(f"Rozpoczynanie nagrywania do {output_file}...")

            # Uruchomienie tcpdump z nadpisywaniem pliku, bez wyświetlania outputu
            with open(os.devnull, 'w') as devnull:
                tcpdump_command = ["sudo", "tcpdump", "-i", "en0", "-w", output_file]
                process = subprocess.Popen(tcpdump_command, stdout=devnull, stderr=devnull)
            
            # Zaktualizowanie zmiennej nazwapliku
            global nazwapliku
            nazwapliku = f"output_{i}.pcap"
            
            # Czekanie 3 sekundy
            time.sleep(3)

            # Zatrzymanie tcpdump
            process.terminate()
            process.wait()  # Upewnij się, że tcpdump zakończył się poprawnie
            # print(f"Zakończono nagrywanie do {output_file}.")

# Uruchomienie tcpdump w osobnym wątku
capture_packets = threading.Thread(target=capture_tcp_packets)

def start_capturing_tcp_packets():
    capture_packets.start()

# Zakończenie wątku
capture_packets.join()
