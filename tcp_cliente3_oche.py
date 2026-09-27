import socket
import sys

# Read target host and port from CLI arguments
host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Test messages to transmit
test_messages = [
    "HOLA",
    "PYTHON",
    "RADAR",
    "HELLO WORLD"
]

# Create TCP client socket and establish connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"Connecting to server at {host}:{port}...")
s.connect((host, port))

try:
    for msg in test_messages:
        # Prepare line terminated with \r\n
        payload = msg + "\r\n"
        print(f"Sending: '{msg}'")
        s.sendall(payload.encode("utf-8"))

        # Receive reversed reply
        reply_raw = s.recv(80)
        reply_str = reply_raw.decode("utf-8").strip("\r\n")
        print(f"Server response: '{reply_str}'")

finally:
    s.close()
    print("Connection closed.")