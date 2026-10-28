import socket

s = socket.socket()
s.connect(("localhost", 23))
respuesta = s.recv(1024)
print(respuesta)

def mostrar_hex(cadena_bytes):
    for byte in cadena_bytes:
        print(hex(byte), end=" ")
    print()  # Nowa linia na końcu

mostrar_hex(respuesta)