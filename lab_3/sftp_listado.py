import getpass
import paramiko
import base64

client = paramiko.SSHClient()

b64_key = b'AAAAC3NzaC1lZDI1NTE5AAAAIIL8aD+Zx43xGkyjGwosy6SlEpT32OjOLuPglF1V644o'

key = paramiko.Ed25519Key(data=base64.b64decode(b64_key))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

host = "localhost"
username = "uo324701"
password = getpass.getpass(f"Enter password for {username}: ")

try:
    client.connect(host, username=username, password=password)
    print("SSH connection established successfully.")

    sftp = client.open_sftp()

    files = sftp.listdir()
    print(f"\nRemote directory content for ({username}):")
    print("-" * 40)
    for filename in files:
        print(filename)

    sftp.close()
    client.close()

except Exception as e:
    print(f"Error during connection: {e}")