import socket
import sys
import time

def receive_line(sock):
    """
    Reads byte by byte until the \r\n terminator is found or connection closes.
    Returns the accumulated line as bytes, or empty bytes b'' on EOF.
    """
    buffer = []
    while True:
        chunk = sock.recv(1)
        if not chunk:
            # Client disconnected before sending data
            return b"".join(buffer)
        
        buffer.append(chunk)
        # Check if the buffer ends with CRLF (\r\n)
        if len(buffer) >= 2 and buffer[-2] == b"\r" and buffer[-1] == b"\n":
            return b"".join(buffer)

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", port))
server_socket.listen(5)
print(f"Server 4 (byte-by-byte) listening on port {port}...")

try:
    while True:
        print("\nWaiting for incoming connection...")
        client_sock, client_addr = server_socket.accept()
        print(f"Client connected from {client_addr}")

        # Introduce delay to prove that pipelined messages are handled cleanly
        time.sleep(1)

        try:
            while True:
                line_bytes = receive_line(client_sock)
                if not line_bytes:
                    print("Client disconnected cleanly.")
                    break

                text = line_bytes.decode("utf-8")
                # Remove trailing CRLF
                payload = text[:-2] if text.endswith("\r\n") else text

                reversed_text = payload[::-1]
                print(f"Received: '{payload}' -> Replying: '{reversed_text}'")

                # Transmit response back with CRLF
                client_sock.sendall((reversed_text + "\r\n").encode("utf-8"))
        finally:
            client_sock.close()

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server_socket.close()