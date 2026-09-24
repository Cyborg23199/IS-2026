import socket
import sys

# Get target host and port or use defaults
server_host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

INITIAL_TIMEOUT = 0.25
MAX_TIMEOUT = 2.0

counter = 1

while True:
    text = input("Enter a message (FIN to quit): ")
    if text == "FIN":
        break

    message = f"{counter}: {text}"
    encoded_message = message.encode("utf-8")

    current_timeout = INITIAL_TIMEOUT
    acknowledged = False

    # Retry loop for the current message
    while not acknowledged:
        if current_timeout > MAX_TIMEOUT:
            print("Server is probably not working.")
            s.close()
            sys.exit(1)

        s.settimeout(current_timeout)
        print(f"Sending (attempt with timeout={current_timeout}s): '{message}'")
        s.sendto(encoded_message, (server_host, server_port))

        try:
            data, _ = s.recvfrom(1024)
            response = data.decode("utf-8")

            if response == "OK":
                print(f"[OK] Acknowledgment received for message {counter}")
                acknowledged = True
                counter += 1
            else:
                print(f"[WARNING] Unexpected response: {response}")

        except socket.timeout:
            print(f"[TIMEOUT] No ACK received within {current_timeout}s. Doubling timeout...")
            current_timeout *= 2

s.close()
print("Client closed.")