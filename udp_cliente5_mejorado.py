import socket
import sys

server_host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
server_port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# In UDP, connect() binds the socket to this specific remote peer.
# It automatically filters out packets from any other source and allows using send()/recv().
s.connect((server_host, server_port))

INITIAL_TIMEOUT = 0.25
MAX_TIMEOUT = 2.0
counter = 1

while True:
    text = input("Enter a message (FIN to quit): ")
    if text == "FIN":
        break

    # Protocol payload with explicit ID
    expected_ack = f"OK {counter}"
    payload = f"{counter}:{text}".encode("utf-8")

    current_timeout = INITIAL_TIMEOUT
    acknowledged = False

    while not acknowledged:
        if current_timeout > MAX_TIMEOUT:
            print("Server is probably not working.")
            s.close()
            sys.exit(1)

        s.settimeout(current_timeout)
        print(f"Sending [{counter}]: '{text}' (timeout={current_timeout}s)")
        s.send(payload)

        try:
            # Using recv() because connect() was called
            data = s.recv(1024)
            response = data.decode("utf-8").strip()

            if response == expected_ack:
                print(f"[ACK RECEIVED] Confirmed: {response}")
                acknowledged = True
                counter += 1
            else:
                # Late ACK from an older message or mismatched ID: discard and wait
                print(f"[IGNORED] Stale or mismatched ACK received: '{response}' (waiting for '{expected_ack}')")

        except (socket.timeout, ConnectionRefusedError):
            print(f"[TIMEOUT] No valid ACK for message {counter}. Retrying...")
            current_timeout *= 2

s.close()
print("Client shut down cleanly.")