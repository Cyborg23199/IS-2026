import socket
import sys
import time

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", port))
server_socket.listen(5)
print(f"Server 5 (makefile/readline) listening on port {port}...")

try:
    while True:
        print("\nWaiting for incoming connection...")
        client_sock, client_addr = server_socket.accept()
        print(f"Client connected from {client_addr}")

        # Intentional delay to accumulate messages in the OS network buffer
        time.sleep(1)

        # Wrap socket into a text-oriented file stream
        file_stream = client_sock.makefile(mode="r", encoding="utf-8", newline="\r\n")

        try:
            while True:
                # readline() reads until \r\n, returning an empty string on EOF
                line = file_stream.readline()
                if not line:
                    print("Client reached EOF and disconnected.")
                    break

                # Strip trailing CRLF
                payload = line[:-2] if line.endswith("\r\n") else line.rstrip("\r\n")

                reversed_payload = payload[::-1]
                print(f"Received: '{payload}' -> Replying: '{reversed_payload}'")

                # Send formatted response back over the raw socket
                client_sock.sendall((reversed_payload + "\r\n").encode("utf-8"))
        finally:
            file_stream.close()
            client_sock.close()

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server_socket.close()