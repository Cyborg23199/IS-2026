import socket
import sys

# Read listening port from CLI arguments or use default
port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Create TCP listening socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prevent "Address already in use" errors during quick restarts
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind and listen
s.bind(("", port))
s.listen(5)
print(f"Oche server listening on port {port}...")

try:
    while True:
        print("\nWaiting for incoming connection...")
        sd, origin = s.accept()
        print(f"Client connected from {origin[0]}:{origin[1]}")

        try:
            while True:
                # Read up to 80 bytes
                raw_data = sd.recv(80)

                # An empty bytes object indicates connection closed by client
                if not raw_data:
                    print("Client closed connection cleanly.")
                    break

                # Decode incoming payload
                message = raw_data.decode("utf-8")

                # Strip trailing \r\n characters
                if message.endswith("\r\n"):
                    line = message[:-2]
                elif message.endswith("\n"):
                    line = message[:-1]
                else:
                    line = message

                # Reverse message
                reversed_line = line[::-1]
                print(f"Received: '{line}' -> Sending: '{reversed_line}'")

                # Append \r\n terminator and transmit response
                response = reversed_line + "\r\n"
                sd.sendall(response.encode("utf-8"))

        finally:
            sd.close()
            print("Client socket closed.")

except KeyboardInterrupt:
    print("\nServer interrupted by user.")
finally:
    s.close()
    print("Main server socket closed.")