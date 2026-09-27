import socket
import sys

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

# Wrap client socket to read incoming lines cleanly
file_stream = client_socket.makefile(mode="r", encoding="utf-8", newline="\r\n")

messages = ["UNO\r\n", "DOS\r\n", "TRES\r\n"]

print("Pipelining 3 requests sequentially...")
for msg in messages:
    client_socket.sendall(msg.encode("utf-8"))

print("\nReading 3 responses back using readline():")
for i in range(3):
    reply = file_stream.readline()
    print(f"Response #{i + 1}: {repr(reply)}")

file_stream.close()
client_socket.close()
print("Client connection terminated.")