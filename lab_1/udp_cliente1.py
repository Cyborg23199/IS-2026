import socket
import sys

# Get host and port from command line arguments or use defaults
server_host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Loop to read text from keyboard and send it to the server
while True:
    text = input("Enter a message (FIN to quit): ")
    if text == "FIN":
        break

    # Encode string to bytes and send to server
    s.sendto(text.encode("utf-8"), (server_host, server_port))

s.close()
print("Client shut down.")