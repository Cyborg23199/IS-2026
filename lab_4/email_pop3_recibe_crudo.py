import socket
import sys
import ssl
import getpass
import email

def RecvReply(sock):
    """
    Receives up to 1024 bytes from the socket, prints the server response for debugging,
    and verifies if it starts with the '+OK' success prefix. Exits on error.
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
    # 1. Server configuration
    server = "pop.gmail.com"
    port = 995

    # 2. Prompt for user credentials
    username = input("Usuario (Gmail): ").strip()
    password = getpass.getpass("Contraseña de aplicación: ").strip()

    # 3. Create TCP socket and wrap with SSL
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
        context = ssl.create_default_context()
        sc = context.wrap_socket(s, server_hostname=server)
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # 4. Receive server greeting
    RecvReply(sc)

    # 5. Send USER command
    user_cmd = f"USER {username}\r\n".encode()
    print("CLIENT:", user_cmd.decode().strip())
    sc.sendall(user_cmd)
    RecvReply(sc)

    # 6. Send PASS command
    pass_cmd = f"PASS {password}\r\n".encode()
    print("CLIENT: PASS *******")
    sc.sendall(pass_cmd)
    RecvReply(sc)

    # 7. Send STAT command to check available messages
    stat_cmd = b"STAT\r\n"
    print("CLIENT: STAT")
    sc.sendall(stat_cmd)
    stat_reply = RecvReply(sc)

    # Parse status response (+OK NumMsg NumBytes)
    parts = stat_reply.decode('utf-8', errors='ignore').split()
    if len(parts) >= 2:
        num_msg = int(parts[1])
        print(f"\n[INFO] Messages available on server: {num_msg}")
        if num_msg == 0:
            print("[INFO] No messages available to read.")
            sc.sendall(b"QUIT\r\n")
            sc.close()
            return

    # 8. Retrieve the first message (RETR 1)
    retr_cmd = b"RETR 1\r\n"
    print("\nCLIENT: RETR 1")
    sc.sendall(retr_cmd)

    # Read the full message until \r\n.\r\n
    raw_response = receive_full_message(sc)

    # 9. Parse message headers using email module
    # Strip the initial +OK status line from the POP3 payload before parsing
    first_newline = raw_response.find(b"\r\n")
    if first_newline != -1:
        raw_email = raw_response[first_newline + 2:]
    else:
        raw_email = raw_response

    msg = email.message_from_bytes(raw_email)

    print("\n" + "=" * 40)
    print(f"From:    {msg.get('From')}")
    print(f"Subject: {msg.get('Subject')}")
    print("=" * 40 + "\n")

    # 10. Close POP3 session
    sc.sendall(b"QUIT\r\n")
    sc.close()
    print("[SUCCESS] POP3 session closed.")

if __name__ == "__main__":
    main()