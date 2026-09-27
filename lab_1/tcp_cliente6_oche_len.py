import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Wrap socket to read length headers and bodies easily
file_stream = client_socket.makefile(mode="r", encoding="utf-8")

test_messages = ["FIRST MESSAGE", "SECOND", "THIRD LONG MESSAGE TO TEST BUFFERING"]

try:
    for msg in test_messages:
        msg_bytes = msg.encode("utf-8")
        # Format ASCII length followed by newline delimiter
        header = f"{len(msg_bytes)}\n"
        
        # Send header + body together
        client_socket.sendall(header.encode("utf-8") + msg_bytes)
        print(f"Sent: '{msg}' (Declared length: {len(msg_bytes)})")

        # Read response length header
        resp_length_line = file_stream.readline()
        if not resp_length_line:
            print("Server closed connection unexpectedly.")
            break

        resp_length = int(resp_length_line.strip())
        
        # Read exact response payload
        reply_payload = file_stream.read(resp_length)
        print(f"Received response ({resp_length} bytes): '{reply_payload}'\n")

finally:
    file_stream.close()
    client_socket.close()
    print("Client connection terminated.")