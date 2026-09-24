import socket
import sys

PORT = 12345

# Get broadcast address from argument or fallback to local broadcast
if len(sys.argv) > 1:
    broadcast_ip = sys.argv[1]
else:
    # 255.255.255.255 is the generic limited broadcast address
    broadcast_ip = "255.255.255.255"

# Create UDP socket and enable broadcast sending
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Step 1: Send broadcast probe
print(f"Broadcasting discovery message to {broadcast_ip}:{PORT}...")
probe_message = "BUSCANDO HOLA".encode("utf-8")
s.sendto(probe_message, (broadcast_ip, PORT))

# Step 2: Collect all server responses until timeout expires
s.settimeout(2.0)  # Wait up to 2 seconds for any server to answer
discovered_servers = []

print("Listening for available servers...")
while True:
    try:
        data, server_address = s.recvfrom(1024)
        reply = data.decode("utf-8").strip()

        if reply == "IMPLEMENTO HOLA":
            server_ip = server_address[0]
            print(f"Discovered server at: {server_address}")
            if server_address not in discovered_servers:
                discovered_servers.append(server_address)

    except socket.timeout:
        # Timeout reached: no more servers responded
        print("Discovery window closed.")
        break

# Step 3: Test service with the first server that responded
if len(discovered_servers) > 0:
    first_server = discovered_servers[0]
    print(f"\nContacting first server directly: {first_server}")

    # Remove socket timeout or set a standard response timeout
    s.settimeout(2.0)
    s.sendto("HOLA".encode("utf-8"), first_server)

    try:
        data, _ = s.recvfrom(1024)
        print(f"Server response: {data.decode('utf-8')}")
    except socket.timeout:
        print("Server did not reply to 'HOLA' request.")
else:
    print("No servers found on this subnet.")

s.close()
print("Client finished.")