import poplib
import getpass
import email

def main():
    # 1. Server configuration
    server = "pop.gmail.com"

    # 2. Prompt for user credentials
    username = input("Usuario (Gmail): ").strip()
    password = getpass.getpass("Contraseña de aplicación: ").strip()

    try:
        # 3. Instantiate POP3_SSL connection on default SSL port 995
        print(f"\n[INFO] Connecting to {server} via POP3_SSL...")
        pop3_mail = poplib.POP3_SSL(server)

        # Enable high level debug output (level 2 shows full protocol exchange)
        pop3_mail.set_debuglevel(2)

        # 4. Authenticate using user() and pass_()
        print("[INFO] Authenticating...")
        pop3_mail.user(username)
        pop3_mail.pass_(password)

        # 5. Retrieve status to ensure messages are available
        stat_response = pop3_mail.stat()
        num_messages = stat_response[0]
        print(f"\n[INFO] Messages count: {num_messages}")

        if num_messages > 0:
            # 6. Retrieve the first message using retr(1)
            # Returns tuple: (response_string, lines_list, octets_size)
            print("\n[INFO] Retrieving message 1...")
            response, lines, octets = pop3_mail.retr(1)

            print("\n" + "=" * 40)
            print("RAW MESSAGE CONTENT RETURNED BY POPLIB:")
            print("=" * 40)
            
            # Reconstruct lines for display
            for line in lines:
                print(line.decode('utf-8', errors='ignore'))

            # Optional: Parse using email module to get Subject/From nicely
            raw_email_bytes = b"\r\n".join(lines)
            msg = email.message_from_bytes(raw_email_bytes)

            print("\n" + "=" * 40)
            print(f"Parsed From:    {msg.get('From')}")
            print(f"Parsed Subject: {msg.get('Subject')}")
            print("=" * 40)
        else:
            print("[INFO] No messages available to retrieve.")

        # 7. Quit session
        pop3_mail.quit()
        print("\n[SUCCESS] Session closed successfully.")

    except Exception as e:
        print(f"\n[ERROR] POP3 error: {e}")

if __name__ == "__main__":
    main()