import socket
import sys

# 1. Odczyt portu z wiersza poleceń lub wartość domyślna 9999
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 9999

# 2. Utworzenie gniazda UDP (AF_INET dla IPv4, SOCK_DGRAM dla UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3. Powiązanie gniazda z adresem lokalnym (pusty ciąg "" oznacza INADDR_ANY)
s.bind(("", port))
print(f"Serwer UDP nasłuchuje na porcie {port}...")

# 4. Nieskończona pętla odbierania datagramów
while True:
    dane, adres_klienta = s.recvfrom(2048)  # bufor 2048 bajtów
    tekst = dane.decode("utf-8")
    print(f"Odebrano od {adres_klienta}: {tekst}")