import socket
import sys

# Get host and port from command-line arguments or use defaults
server_host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set maximum wait time for socket operations (0.5 seconds)
s.settimeout(0.5)

counter = 1

while True:
    text = input("Enter a message (FIN to quit): ")
    if text == "FIN":
        break

    message = f"{counter}: {text}"
    s.sendto(message.encode("utf-8"), (server_host, server_port))

    # Wait for acknowledgment with timeout handling
    try:
        data, sender_address = s.recvfrom(1024)
        response = data.decode("utf-8")

        if response == "OK":
            print(f"[OK] Acknowledgment received for message {counter}")
        else:
            print(f"[WARNING] Unexpected datagram received: {response}")

    except socket.timeout:
        print(f"[ERROR] Confirmation datagram timed out for message {counter}")

    except Exception:
        # Re-raise any other unexpected exception
        raise

    counter += 1

s.close()
print("Client closed.")