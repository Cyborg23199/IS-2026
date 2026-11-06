import email.message
import email.policy
import email.utils

# 1. Crear el objeto de mensaje
mensaje = email.message.EmailMessage()
mensaje['To'] = 'Destinatario <destinatario@example.com>'
mensaje['From'] = 'Remitente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje de prueba con adjunto'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()

# 2. Agregar el cuerpo del mensaje
mensaje.set_content("Hola, adjunto el logotipo pedido.")

# 3. Leer la imagen y añadirla como adjunto
with open("logoatc.gif", "rb") as f:
    gif_data = f.read()

mensaje.add_attachment(gif_data, maintype="image", subtype="gif", filename="atc.gif")

# 4. Imprimir el resultado en pantalla para observar las cabeceras, el boundary y el Base64
binario = mensaje.as_bytes()
print(binario.decode("utf-8", errors="ignore"))