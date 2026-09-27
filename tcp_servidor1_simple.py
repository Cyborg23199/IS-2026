import socket
import sys

# Read listening port from CLI arguments or else 9999
port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999

# Create TCP listening socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to all available interfaces on the selected port
s.bind(("", port))

# Mark socket as passive to accept incoming connections
s.listen(5)
print(f"TCP server listening on port {port}...")

# Main loop waiting for incoming clients
while True:
    print("\nWaiting for a client...")
    sd, origin = s.accept()
    print("New client connected from %s, %d" % origin)

    continuar = True
    # Processing loop for connected client
    while continuar:
        # Read a fixed block of 5 bytes from the dedicated client socket (sd)
        data = sd.recv(5)
        text = data.decode("ascii")

        if text == "":
            print("Connection closed unexpectedly by client")
            sd.close()
            continuar = False
        elif text == "FINAL":
            print("Termination message received")
            sd.close()
            continuar = False
        else:
            print(f"Received message: {text}")