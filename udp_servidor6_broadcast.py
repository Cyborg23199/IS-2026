import socket

PORT = 12345

# Create UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable broadcast support on the socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind to all interfaces on the predefined port
s.bind(("", PORT))

print(f"HOLA service server running on port {PORT}...")

while True:
    data, client_address = s.recvfrom(1024)
    message = data.decode("utf-8").strip()

    # Client is searching for servers
    if message == "BUSCANDO HOLA":
        print(f"Discovery probe received from {client_address}")
        response = "IMPLEMENTO HOLA"
        s.sendto(response.encode("utf-8"), client_address)

    # Client is requesting the service
    elif message == "HOLA":
        client_ip = client_address[0]
        print(f"Service request 'HOLA' received from {client_address}")
        response = f"HOLA: {client_ip}"
        s.sendto(response.encode("utf-8"), client_address)

    else:
        print(f"Unknown message received from {client_address}: {message}")