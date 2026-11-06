import email.message, email.policy, email.utils

mensaje = email.message.EmailMessage()
mensaje['To'] = 'Desti Natario <destinatario@example.com>'
mensaje['From'] = 'Remi Tente <remitente@example.com>'
mensaje['Subject'] = 'Mensąajeń de prueba'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una ę prueba")

binario = mensaje.as_bytes()
print(binario.decode("utf-8"))