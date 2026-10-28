import time
import telnetlib

HOST = "localhost"
USER = "uo324701"      
PASSWORD = "Zaq12wsx"   

tn = telnetlib.Telnet(HOST)

# Logowanie
tn.read_until(b"login: ")
tn.write(USER.encode('utf-8') + b"\n")
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode('utf-8') + b"\n")

# Czekamy na gotowość powłoki
tn.read_until(b"$")

# Sprawdzamy procesy
tn.write(b"ps -ef\n")
respuesta_ps = tn.read_until(b"$").decode('utf-8')

if "udp_servidor_con_ok" in respuesta_ps:
    print("El servidor ya está en ejecución.")
else:
    print("El servidor no está en ejecución. Lanzando...")
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    time.sleep(1)

tn.write(b"exit\n")
print(tn.read_all().decode('utf-8'))