import socket
import sys
import time

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(("", port))
server_socket.listen(5)
print(f"Oche server listening on port {port}...")

try:
    while True:
        print("\nWaiting for an incoming connection...")
        client_conn, client_address = server_socket.accept()
        print(f"Connected by {client_address}")

        # Introduce a 1-second delay to let incoming messages pile up in the OS buffer
        time.sleep(1)

        try:
            while True:
                raw_payload = client_conn.recv(80)
                if not raw_payload:
                    print("Client disconnected.")
                    break

                received_str = raw_payload.decode("utf-8")
                print(f"Raw buffer received: {repr(received_str)}")

                # Flawed approach: strips only the trailing \r\n and reverses the whole chunk
                stripped_str = received_str[:-2]
                reversed_str = stripped_str[::-1]

                client_conn.sendall((reversed_str + "\r\n").encode("utf-8"))
        finally:
            client_conn.close()

except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    server_socket.close()