import socket
import sys
import ssl
import getpass
import email

def RecvReply(sock):
    """
    Receives up to 1024 bytes from the socket, prints the response for debugging,
    and verifies if it starts with the '+OK' success prefix.
    """
    data = sock.recv(1024)
    print("SERVER:", data.decode('utf-8', errors='ignore').strip())

    if not data.startswith(b"+OK"):
        print("[ERROR] Server replied with an error or unexpected status code.")
        sock.close()
        sys.exit(1)
    return data

def receive_full_message(sock):
    """
    Reads data from the socket continuously until the POP3 multiline termination sequence (\r\n.\r\n) is received.
    """
    buffer = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        buffer += chunk
        if b"\r\n.\r\n" in buffer:
            break
    return buffer

def main():
    server = "pop.gmail.com"
    port = 995

    username = input("Usuario (Gmail): ").strip()
    password = getpass.getpass("Contraseña de aplicación: ").strip()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
        context = ssl.create_default_context()
        sc = context.wrap_socket(s, server_hostname=server)
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Initial server greeting
    RecvReply(sc)

    # USER & PASS
    sc.sendall(f"USER {username}\r\n".encode())
    RecvReply(sc)

    sc.sendall(f"PASS {password}\r\n".encode())
    RecvReply(sc)

    # STAT command
    sc.sendall(b"STAT\r\n")
    stat_reply = RecvReply(sc)

    parts = stat_reply.decode('utf-8', errors='ignore').split()
    num_msg = 0
    if len(parts) >= 2:
        num_msg = int(parts[1])

    print(f"\n[INFO] Total messages to retrieve: {num_msg}\n")

    # Iterate through all available messages
    for i in range(1, num_msg + 1):
        print(f"--- Fetching Message {i} of {num_msg} ---")
        sc.sendall(f"RETR {i}\r\n".encode())
        raw_response = receive_full_message(sc)

        # Separate the +OK line from the actual RFC-5322 raw bytes
        first_newline = raw_response.find(b"\r\n")
        if first_newline != -1:
            raw_email = raw_response[first_newline + 2:]
        else:
            raw_email = raw_response

        # Parse message using email module
        msg = email.message_from_bytes(raw_email)

        print(f"Msg #{i} | From:    {msg.get('From')}")
        print(f"Msg #{i} | Subject: {msg.get('Subject')}")
        print("-" * 40)

    # QUIT session
    sc.sendall(b"QUIT\r\n")
    sc.close()
    print("\n[SUCCESS] All message headers retrieved successfully.")

if __name__ == "__main__":
    main()