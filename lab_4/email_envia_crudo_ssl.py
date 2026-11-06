import socket
import sys
import ssl
import base64
import getpass
import email.message
import email.utils

def RecvReply(sock, expected_code):
    """
    Receives bytes from the socket, prints the server's reply,
    and verifies if the status code matches the expected code.
    """
    data = sock.recv(1024)
    print("SERVER:", data.decode('utf-8', errors='ignore').strip())

    code = data[:3]
    if code != expected_code:
        print(f"[ERROR] Expected status code {expected_code.decode()}, but received {code.decode()}")
        sock.close()
        sys.exit(1)

def main():
    # 1. Configuration parameters
    server = "smtp.gmail.com"
    port = 587
    
    # Prompt for credentials from the CLI securely
    username = input("Usuario (Gmail): ").strip()
    password = getpass.getpass("Contraseña de aplicación: ").strip()

    toaddr = input("Destinatario: ").strip()
    subject = "Prueba SMTP con STARTTLS y AUTH LOGIN"
    data_text = "Hola! Este correo fue enviado usando ganchos (sockets), STARTTLS y la biblioteca email."

    # 2. Build RFC-5322 message structure
    msg = email.message.EmailMessage()
    msg['To'] = toaddr
    msg['From'] = username
    msg['Subject'] = subject
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()
    msg.set_content(data_text)

    # Convert message to bytes payload with terminating dot sequence (\r\n.\r\n)
    raw_payload = msg.as_bytes() + b"\r\n.\r\n"

    # 3. Establish initial plain TCP connection on port 587
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Initial server greeting (Expected code: 220)
    RecvReply(s, b"220")

    # 4. Send EHLO command
    ehlo_cmd = b"EHLO mycomputer\r\n"
    print("CLIENT:", ehlo_cmd.decode().strip())
    s.sendall(ehlo_cmd)
    RecvReply(s, b"250")

    # 5. Issue STARTTLS command
    starttls_cmd = b"STARTTLS\r\n"
    print("CLIENT:", starttls_cmd.decode().strip())
    s.sendall(starttls_cmd)
    RecvReply(s, b"220")

    # 6. Upgrade raw socket to secure TLS/SSL socket
    print("[INFO] Upgrading connection to TLS/SSL...")
    context = ssl.create_default_context()
    sc = context.wrap_socket(s, server_hostname=server)

    # Send EHLO again over the secured connection as required by ESMTP
    ehlo_sec_cmd = b"EHLO mycomputer\r\n"
    print("CLIENT (SSL):", ehlo_sec_cmd.decode().strip())
    sc.sendall(ehlo_sec_cmd)
    RecvReply(sc, b"250")

    # 7. Perform Authentication (AUTH LOGIN)
    auth_cmd = b"AUTH LOGIN\r\n"
    print("CLIENT (SSL):", auth_cmd.decode().strip())
    sc.sendall(auth_cmd)
    RecvReply(sc, b"334")

    # Send Base64-encoded username
    user_b64 = base64.b64encode(username.encode("ascii")) + b"\r\n"
    print("CLIENT (SSL): [Sending Base64 Username]")
    sc.sendall(user_b64)
    RecvReply(sc, b"334")

    # Send Base64-encoded password
    pass_b64 = base64.b64encode(password.encode("utf8")) + b"\r\n"
    print("CLIENT (SSL): [Sending Base64 Password]")
    sc.sendall(pass_b64)
    RecvReply(sc, b"235")  # Code 235 indicates successful authentication

    # 8. MAIL FROM
    mail_from_cmd = f"MAIL FROM:<{username}>\r\n".encode()
    print("CLIENT (SSL):", mail_from_cmd.decode().strip())
    sc.sendall(mail_from_cmd)
    RecvReply(sc, b"250")

    # 9. RCPT TO
    rcpt_to_cmd = f"RCPT TO:<{toaddr}>\r\n".encode()
    print("CLIENT (SSL):", rcpt_to_cmd.decode().strip())
    sc.sendall(rcpt_to_cmd)
    RecvReply(sc, b"250")

    # 10. DATA
    data_cmd = b"DATA\r\n"
    print("CLIENT (SSL):", data_cmd.decode().strip())
    sc.sendall(data_cmd)
    RecvReply(sc, b"354")

    # 11. Send payload
    print("CLIENT (SSL): [Sending RFC-5322 payload and terminating dot]")
    sc.sendall(raw_payload)
    RecvReply(sc, b"250")

    # 12. QUIT
    quit_cmd = b"QUIT\r\n"
    print("CLIENT (SSL):", quit_cmd.decode().strip())
    sc.sendall(quit_cmd)
    RecvReply(sc, b"221")

    # Close connection
    sc.close()
    print("\n[SUCCESS] Email sent successfully using STARTTLS and Gmail SMTP!")

if __name__ == "__main__":
    main()