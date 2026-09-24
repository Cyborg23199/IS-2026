import socket
import sys
import random

port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))

print(f"Improved UDP server listening on port {port}...")

# Keep track of handled message IDs to avoid executing actions twice
seen_ids = set()

while True:
    data, client_address = s.recvfrom(2048)

    # 50% simulated loss
    if random.randint(0, 1) == 0:
        print(f"Simulating packet drop from {client_address}")
        continue

    decoded = data.decode("utf-8")

    # Protocol format: "<id>:<content>"
    if ":" in decoded:
        msg_id, message_body = decoded.split(":", 1)
        msg_id = msg_id.strip()

        # Check for duplicated datagram
        if msg_id in seen_ids:
            print(f"[DUPLICATE] ID {msg_id} already processed. Re-sending ACK only.")
        else:
            seen_ids.add(msg_id)
            print(f"[ACTION] Processing new message from {client_address} -> [{msg_id}]: {message_body}")

        # Send ACK specifically confirming this message ID
        ack_payload = f"OK {msg_id}".encode("utf-8")
        s.sendto(ack_payload, client_address)
    else:
        print(f"[MALFORMED] Received unformatted message: {decoded}")