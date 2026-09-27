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

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", port))
server_socket.listen(5)
print(f"Server 7 (Binary 2-byte length header) listening on port {port}...")

try:
    while True:
        print("\nWaiting for incoming connection...")
        client_sock, client_addr = server_socket.accept()
        print(f"Client connected from {client_addr}")

        try:
            while True:
                # 1. Read fixed 2-byte binary header
                header_bytes = recv_exact(client_sock, 2)
                if not header_bytes:
                    print("Client disconnected cleanly.")
                    break

                # 2. Decode length (>H means big-endian unsigned short)
                (payload_length,) = struct.unpack(">H", header_bytes)

                # 3. Read exactly payload_length bytes of message
                payload_bytes = recv_exact(client_sock, payload_length)
                if not payload_bytes:
                    print("Connection dropped unexpectedly while reading payload.")
                    break

                text = payload_bytes.decode("utf-8")
                reversed_text = text[::-1]
                print(f"Received ({payload_length} bytes): '{text}' -> Replying: '{reversed_text}'")

                # 4. Prepare response with 2-byte binary header
                resp_bytes = reversed_text.encode("utf-8")
                resp_header = struct.pack(">H", len(resp_bytes))
                
                # Send header + body
                client_sock.sendall(resp_header + resp_bytes)
        finally:
            client_sock.close()

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server_socket.close()