import socket
import sys

# Default destination host and port
host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Establish connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

messages = ["UNO\r\n", "DOS\r\n", "TRES\r\n"]

print("Sending 3 consecutive messages without waiting...")
for msg in messages:
    client_socket.sendall(msg.encode("utf-8"))

print("\nAttempting to read 3 responses back-to-back...")
for i in range(3):
    print(f"Waiting for response #{i + 1}...")
    response_bytes = client_socket.recv(80)
    print(f"recv() #{i + 1} returned: {repr(response_bytes.decode('utf-8'))}")

client_socket.close()
print("Client connection terminated.")