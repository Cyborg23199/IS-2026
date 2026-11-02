import base64
import getpass
import paramiko
import time

client = paramiko.SSHClient()

b64_key = b'key_from_friend'

key = paramiko.Ed25519Key(data=base64.b64decode(b64_key))
client.get_host_keys().add('localhost', 'ssh-ed25519', key)

clave = getpass.getpass("Type the password for user uo324707: ")

client.connect('localhost', username='uo324707', password=clave)
print("Connected securely!!")

stdin, stdout, stderr = client.exec_command('ls -la')

for line in stdout:
    print(line.rstrip())

time.sleep(1)
client.close()