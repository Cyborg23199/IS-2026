# coding: utf-8
import os
import ssl
import getpass
import logging
from slixmpp import ClientXMPP


class MiBot(ClientXMPP):
    def __init__(self, jid, clave):
        super().__init__(jid, clave)
        self.add_event_handler("session_start", self.callback_para_session_start)
        self.add_event_handler("message", self.callback_para_message)

    async def callback_para_session_start(self, evento):
        self.send_presence()
        await self.get_roster()

    async def callback_para_message(self, evento):
        print(f"Recibido un mensaje de tipo {evento['type']} desde {evento['from']}")
        print(f"Que dice: {evento['body']}")

        if evento["type"] == "chat":
            body = evento["body"]
            msg = self.Message()
            msg["to"] = evento["from"]
            msg["type"] = "chat"
            msg["body"] = f"¿{body}?"
            msg.send()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")

    jid = os.environ.get("BOT_JID") or input("JID del bot (ej. bot@ingserv222): ")
    clave = os.environ.get("BOT_PASS") or getpass.getpass("Contraseña del bot: ")
    ip = os.environ.get("XMPP_HOST") or input("IP del servidor (ej. localhost): ")
    puerto = 5222

    cliente = MiBot(jid, clave)

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    cliente.ssl_context = ssl_context

    cliente.connect((ip, puerto))
    cliente.process(forever=True)
