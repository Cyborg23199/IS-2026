import socket
import sys

# Read target host and port from CLI arguments or use defaults
host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Create TCP socket and establish connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Connecting to server {host}:{port}...")
s.connect((host, port))

# Send fixed 5-byte payload 5 times using sendall()
for _ in range(4):
    s.sendall(b"ABCDE")
# Send final termination message
s.sendall(b"FINAL")

# Close connection
s.close()
print("All messages sent using sendall(). Connection closed.")