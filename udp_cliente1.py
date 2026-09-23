import socket
import sys

# 1. Odczyt hosta i portu z wiersza poleceń lub wartości domyślne
host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# 2. Utworzenie gniazda UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 3. Pętla czytania tekstu z klawiatury i wysyłania do serwera
while True:
    tekst = input("Wpisz wiadomość (FIN aby zakończyć): ")
    if tekst == "FIN":
        break

    # Konwersja tekstu na bajty i wysłanie do serwera
    s.sendto(tekst.encode("utf-8"), (host, port))

# 4. Zamknięcie gniazda po wyjściu z pętli
s.close()
print("Klient zakończył pracę.")