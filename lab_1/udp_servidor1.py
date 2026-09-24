import socket
import sys

# Get port from command line arguments or use 9999 as default
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 9999

# Create a UDP socket (IPv4, datagram)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to all available interfaces ("" means INADDR_ANY)
s.bind(("", port))
print(f"UDP server listening on port {port}...")

# Infinite loop to receive and display datagrams
while True:
    data, client_address = s.recvfrom(2048)
    message = data.decode("utf-8")
    print(f"Received from {client_address}: {message}")