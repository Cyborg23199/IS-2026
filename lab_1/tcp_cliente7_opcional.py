import socket
import struct
import sys

def recv_exact(sock, num_bytes):
    """Reads exactly num_bytes from the socket. Returns None if connection closes."""
    chunks = []
    bytes_read = 0
    while bytes_read < num_bytes:
        chunk = sock.recv(num_bytes - bytes_read)
        if not chunk:
            return None
        chunks.append(chunk)
        bytes_read += len(chunk)
    return b"".join(chunks)

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

test_messages = ["FIRST BINARY MSG", "SECOND", "THIRD LONGER TEST MESSAGE"]

try:
    for msg in test_messages:
        msg_bytes = msg.encode("utf-8")
        # Pack length into 2 bytes big-endian
        header = struct.pack(">H", len(msg_bytes))

        # Transmit 2-byte header followed immediately by body
        client_socket.sendall(header + msg_bytes)
        print(f"Sent: '{msg}' (Declared length: {len(msg_bytes)} bytes)")

        # Read 2-byte response header
        resp_header = recv_exact(client_socket, 2)
        if not resp_header:
            print("Server closed connection.")
            break

        (resp_length,) = struct.unpack(">H", resp_header)

        # Read exact response body
        reply_bytes = recv_exact(client_socket, resp_length)
        print(f"Received ({resp_length} bytes): '{reply_bytes.decode('utf-8')}'\n")

finally:
    client_socket.close()
    print("Client connection closed.")