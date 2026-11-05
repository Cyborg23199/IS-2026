import socket
import sys

def RecvReply(sock, expected_code):
    """
    Receives bytes from the socket, prints the server response,
    and checks if the response code matches the expected code.
    """
    data = sock.recv(1024)
    print("SERVER:", data.decode('utf-8', errors='ignore').strip())

    # Extract the first 3 bytes representing the status code
    code = data[:3]
    if code != expected_code:
        print(f"[ERROR] Expected status code {expected_code.decode()}, but received {code.decode()}")
        sock.close()
        sys.exit(1)

def main():
    # 1. Configuration parameters
    server = "relay.uniovi.es"
    port = 25
    fromaddr = "xxxxxxxx@uniovi.es"
    toaddr = "xxxxxxxx@uniovi.es" 
    subject = "SMTP Raw Socket Test"
    data_text = "Thhis is test email sent using raw Python sockets over SMTP."

    # 2. Create TCP Socket and connect to server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Receive initial server greeting (Expected code: 220)
    RecvReply(s, b"220")

    # 3. Send HELO command (Expected code: 250)
    helo_cmd = b"HELO lab-pc\r\n"
    print("CLIENT:", helo_cmd.decode().strip())
    s.sendall(helo_cmd)
    RecvReply(s, b"250")

    # 4. Send MAIL FROM command (Expected code: 250)
    mail_from_cmd = f"MAIL FROM:<{fromaddr}>\r\n".encode()
    print("CLIENT:", mail_from_cmd.decode().strip())
    s.sendall(mail_from_cmd)
    RecvReply(s, b"250")

    # 5. Send RCPT TO command (Expected code: 250)
    rcpt_to_cmd = f"RCPT TO:<{toaddr}>\r\n".encode()
    print("CLIENT:", rcpt_to_cmd.decode().strip())
    s.sendall(rcpt_to_cmd)
    RecvReply(s, b"250")

    # 6. Send DATA command (Expected code: 354)
    data_cmd = b"DATA\r\n"
    print("CLIENT:", data_cmd.decode().strip())
    s.sendall(data_cmd)
    RecvReply(s, b"354")

    # 7. Construct message headers, body, and terminating sequence (\r\n.\r\n)
    message = f"To: {toaddr}\r\nFrom: {fromaddr}\r\nSubject: {subject}\r\n\r\n{data_text}\r\n.\r\n"
    print("CLIENT: [Sending email message headers, content, and terminating dot]")
    s.sendall(message.encode('utf-8'))
    RecvReply(s, b"250")

    # 8. Send QUIT command (Expected code: 221)
    quit_cmd = b"QUIT\r\n"
    print("CLIENT:", quit_cmd.decode().strip())
    s.sendall(quit_cmd)
    RecvReply(s, b"221")

    # Close the socket connection
    s.close()
    print("\n[SUCCESS] Email sent successfully!")

if __name__ == "__main__":
    main()