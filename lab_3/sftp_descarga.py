import getpass
import os
from stat import S_ISDIR
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
    sftp = client.open_sftp()

    remote_dir = "."
    local_target_dir = "./descargas_sftp"

    if not os.path.exists(local_target_dir):
        os.makedirs(local_target_dir)

    items = sftp.listdir(remote_dir)

    print(f"\nDownloading regular files from '{remote_dir}'...")

    for item in items:
        remote_path = (
            f"{remote_dir}/{item}"
            if remote_dir != "."
            else item
        )

        attr = sftp.stat(remote_path)

        # Check if the item is a directory
        if S_ISDIR(attr.st_mode):
            print(f"[SKIPPED] '{item}' is a directory.")
        else:
            # Download regular files only
            local_path = os.path.join(local_target_dir, item)
            print(f"[DOWNLOADING] '{item}' ({attr.st_size} B) -> '{local_path}'")
            sftp.get(remote_path, local_path)

    print("\nDownload completed successfully!")

    sftp.close()
    client.close()

except Exception as e:
    print(f"Error: {e}")