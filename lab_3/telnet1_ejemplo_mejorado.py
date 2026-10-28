import getpass
import telnetlib

HOST = "localhost"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.read_until(b"$")

tn.write(b"ls /home\n")

salida = tn.read_until(b"$")
print(salida.decode('utf-8'))

tn.write(b"exit\n")
tn.close()