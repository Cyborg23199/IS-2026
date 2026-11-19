import telnetlib

HOST = "localhost"
USER = "uo324701"
PASSWORD = "Zaq12wsx"

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(USER.encode('utf-8') + b"\n")
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode('utf-8') + b"\n")

tn.read_until(b"$")

tn.write(b'docker ps -a --format "{{.Names}}|{{.Status}}"\n')
respuesta_docker = tn.read_until(b"$").decode('utf-8')

tn.write(b"exit\n")
tn.read_all()

print("Contenedores Docker detenidos:")
detenidos = 0

for linea in respuesta_docker.splitlines():
    linea = linea.strip()
    if "|" in linea and "{{.Names}}" not in linea:
        nombre, estado = linea.split("|", 1)
        if not estado.startswith("Up"):
            print(f"Nombre: {nombre} - Estado: {estado}")
            detenidos += 1

if detenidos == 0:
    print("No hay contenedores detenidos.")