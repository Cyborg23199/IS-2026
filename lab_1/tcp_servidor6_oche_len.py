import socket
import sys

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", port))
server_socket.listen(5)
print(f"Server 6 (ASCII length prefix) listening on port {port}...")

try:
    while True:
        print("\nWaiting for incoming connection...")
        client_sock, client_addr = server_socket.accept()
        print(f"Client connected from {client_addr}")

        # Wrap socket into a text-mode stream for buffered reading
        file_stream = client_sock.makefile(mode="r", encoding="utf-8")

        try:
            while True:
                # 1. Read ASCII length header up to the newline delimiter
                length_line = file_stream.readline()
                if not length_line:
                    print("Client disconnected cleanly.")
                    break

                message_length = int(length_line.strip())

                # 2. Read exactly message_length characters of payload
                payload = file_stream.read(message_length)
                print(f"Received payload ({message_length} chars): '{payload}'")

                # Reverse payload
                reversed_payload = payload[::-1]

                # 3. Construct response: ASCII length + \n + payload
                response_bytes = reversed_payload.encode("utf-8")
                header = f"{len(response_bytes)}\n"
                
                # Send back header and payload
                client_sock.sendall(header.encode("utf-8") + response_bytes)
                print(f"Sent reply: '{reversed_payload}' (Header: {repr(header)})")
        finally:
            file_stream.close()
            client_sock.close()

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server_socket.close()