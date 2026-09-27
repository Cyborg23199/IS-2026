import socket
import sys

def recvall(sock, count):
    # Helper function to receive eactly 'count' bytes from a TCP socket
    # Returns bytes if all data is read, or b"" if connection closes prematurely.

    buffer = b""
    while len(buffer) < count:
        missing = count - len(buffer)
        chunk = sock.recv(missing)
        if not chunk:
            return b""
        buffer += chunk
    return buffer

# Read listening port from CLI arguments or else 9999
port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Create TCP listening socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow immediate reuse of local addresses (prevents Errno 98: Address already in use)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to all available interfaces on the selected port
s.bind(("", port))

# Mark socket as passive to accept incoming connections
s.listen(5)
print(f"TCP server listening on port {port}...")

# Main loop waiting for incoming clients
while True:
    print("\nWaiting for a client...")
    sd, origin = s.accept()
    print("New client connected from %s, %d" % origin)

    continuar = True
    # Processing loop for connected client
    while continuar:
        # Read a fixed block of 5 bytes from the dedicated client socket (sd)
        raw_bytes = recvall(sd, 5)
        text = raw_bytes.decode("ascii", errors="replace")

        if text == "":
            print("Connection closed unexpectedly by client")
            sd.close()
            continuar = False
        elif text == "FINAL":
            print("Termination message received")
            sd.close()
            continuar = False
        else:
            print(f"Received message: {text}")