import smtplib
import getpass
import email.message
import email.utils

def main():
    # 1. Server configuration
    server = "smtp.gmail.com"
    port = 587

    # 2. Prompt user for credentials and destination safely
    username = input("Usuario (Gmail): ").strip()
    password = getpass.getpass("Contraseña de aplicación: ").strip()
    toaddr = input("Destinatario: ").strip()
    
    subject = "Pruebaąąąęęę SMTP usando la biblioteca smtplib"
    data_text = "Another test message."

    # 3. Construct RFC-5322 compliant message object
    msg = email.message.EmailMessage()
    msg['To'] = toaddr
    msg['From'] = username
    msg['Subject'] = subject
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid()
    msg.set_content(data_text)

    try:
        # 4. Instantiate SMTP object and connect to server
        print(f"\n[INFO] Connecting to {server}:{port}...")
        s = smtplib.SMTP(server, port)

        # Enable debug level 1 to print all outgoing/incoming SMTP commands
        s.set_debuglevel(1)

        # 5. Start TLS encryption
        print("[INFO] Initiating STARTTLS...")
        s.starttls()

        # 6. Authenticate with server
        print("[INFO] Logging in...")
        s.login(username, password)

        # 7. Send email using sendmail()
        #as_bytes() converts the message object without needing an explicit terminating dot
        print("[INFO] Sending message...")
        s.sendmail(username, [toaddr], msg.as_bytes())

        # 8. Close SMTP session nicely (sends QUIT)
        s.quit()
        print("\n[SUCCESS] Email successfully delivered via smtplib!")

    except Exception as e:
        print(f"\n[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    main()