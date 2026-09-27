import socket
import sys

def receive_line(sock):
    buffer = []
    while True:
        chunk = sock.recv(1)
        if not chunk:
            return b"".join(buffer)
        buffer.append(chunk)
        if len(buffer) >= 2 and buffer[-2] == b"\r" and buffer[-1] == b"\n":
            return b"".join(buffer)

host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

messages = ["UNO\r\n", "DOS\r\n", "TRES\r\n"]

print("Pipelining 3 requests sequentially...")
for msg in messages:
    client_socket.sendall(msg.encode("utf-8"))

print("\nReading 3 delimited responses using receive_line():")
for i in range(3):
    reply_bytes = receive_line(client_socket)
    print(f"Response #{i + 1}: {repr(reply_bytes.decode('utf-8'))}")

client_socket.close()
print("Client closed connection.")