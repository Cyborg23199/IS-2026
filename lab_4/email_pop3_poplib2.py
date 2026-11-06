import poplib
import getpass
import email
import email.header

def imprime_resumen_mensaje(msg_bytes):
    """
    Parses raw email bytes, decodes MIME/Unicode headers (From, Subject),
    handles multipart message bodies gracefully, and prints a formatted summary.
    """
    # Build an EmailMessage object from the raw bytes
    msg = email.message_from_bytes(msg_bytes)
    
    # Extract headers "From" and "Subject"
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")
    
    # Decode Encoded-Word headers if they contain non-ASCII/Unicode characters
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))
    
    # Extract the payload (body content)
    cuerpo = msg.get_payload()
    
    # Handle multipart messages (getpayload returns a list of sub-parts)
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + str(parte_1)
    else:
        cuerpo = str(cuerpo)
        
    # Print the summary: parsed headers and first 500 characters of body
    print(f"From:    {remite}")
    print(f"Subject: {asunto}")
    print("Body preview:")
    print(cuerpo[:500])
    if len(cuerpo) > 500:
        print("...[omitido]")
    print("-" * 80)

def main():
    # 1. Server configuration
    server = "pop.gmail.com"

    # 2. Securely prompt for user credentials
    username = input("Usuario (Gmail): ").strip()
    password = getpass.getpass("Contraseña de aplicación: ").strip()

    try:
        # 3. Establish SSL POP3 connection
        print(f"\n[INFO] Connecting to {server} via POP3_SSL...")
        pop3_mail = poplib.POP3_SSL(server)

        # 4. Authenticate
        print("[INFO] Logging in...")
        pop3_mail.user(username)
        pop3_mail.pass_(password)

        # 5. Get message count
        num_messages = len(pop3_mail.list()[1])
        print(f"[INFO] Total messages available: {num_messages}\n")

        # 6. Iterate through all available messages
        for i in range(1, num_messages + 1):
            print(f"=== Message {i} of {num_messages} ===")
            
            # retr() returns tuple: (response, lines_list, octets)
            response, lines, octets = pop3_mail.retr(i)
            
            # Join line list with CRLF into a single bytes sequence
            raw_msg_bytes = b"\r\n".join(lines)
            
            # Print parsed summary
            imprime_resumen_mensaje(raw_msg_bytes)

        # 7. Close session cleanly
        pop3_mail.quit()
        print("[SUCCESS] POP3 session closed cleanly.")

    except Exception as e:
        print(f"\n[ERROR] POP3 Exception: {e}")

if __name__ == "__main__":
    main()