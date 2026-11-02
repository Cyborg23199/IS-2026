import paramiko
import getpass
import time

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

clave = getpass.getpass("Type the password for user uo324701: ")

client.connect('localhost', username='uo324701', password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls -la')

for line in stdout:
    print(line.rstrip())

time.sleep(1)
client.close()