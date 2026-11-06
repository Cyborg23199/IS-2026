import socket
import sys
import email.message
import email.utils

def RecvReply(sock, expected_code):
    """
    Receives data from the socket, prints the server's reply,
    and verifies if the 3-digit status code matches the expected one.
    """
    data = sock.recv(1024)
    print("SERVER:", data.decode('utf-8', errors='ignore').strip())

    # Extract the status code (first 3 bytes)
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
    subject = "RFC-5322 Standard Test with Accents: ĄŻŚÓĘ áéíóú"
    data_text = "Hello! This message is formatted according to RFC-5322 using Python's email module."

    # 2. Construct the message using email.message.EmailMessage (RFC-5322)
    msg = email.message.EmailMessage()
    msg['To'] = toaddr
    msg['From'] = fromaddr
    msg['Subject'] = subject
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()
    msg.set_content(data_text)

    # Convert the EmailMessage object to bytes
    msg_bytes = msg.as_bytes()

    # Append the raw SMTP terminating dot sequence (\r\n.\r\n) to the bytes payload
    raw_payload = msg_bytes + b"\r\n.\r\n"

    # 3. Create TCP socket and connect to the SMTP relay
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Receive initial server greeting (Expected code: 220)
    RecvReply(s, b"220")

    # 4. Send HELO command (Expected code: 250)
    helo_cmd = b"HELO lab-pc\r\n"
    print("CLIENT:", helo_cmd.decode().strip())
    s.sendall(helo_cmd)
    RecvReply(s, b"250")

    # 5. Send MAIL FROM command (Expected code: 250)
    mail_from_cmd = f"MAIL FROM:<{fromaddr}>\r\n".encode()
    print("CLIENT:", mail_from_cmd.decode().strip())
    s.sendall(mail_from_cmd)
    RecvReply(s, b"250")

    # 6. Send RCPT TO command (Expected code: 250)
    rcpt_to_cmd = f"RCPT TO:<{toaddr}>\r\n".encode()
    print("CLIENT:", rcpt_to_cmd.decode().strip())
    s.sendall(rcpt_to_cmd)
    RecvReply(s, b"250")

    # 7. Send DATA command (Expected code: 354)
    data_cmd = b"DATA\r\n"
    print("CLIENT:", data_cmd.decode().strip())
    s.sendall(data_cmd)
    RecvReply(s, b"354")

    # 8. Send the RFC-5322 compiled payload including the terminating dot
    print("CLIENT: [Sending RFC-5322 formatted message payload + terminating dot]")
    s.sendall(raw_payload)
    RecvReply(s, b"250")

    # 9. Send QUIT command (Expected code: 221)
    quit_cmd = b"QUIT\r\n"
    print("CLIENT:", quit_cmd.decode().strip())
    s.sendall(quit_cmd)
    RecvReply(s, b"221")

    # Close connection
    s.close()
    print("\n[SUCCESS] RFC-5322 email sent successfully!")

if __name__ == "__main__":
    main()