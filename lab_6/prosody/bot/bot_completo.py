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
        self.add_event_handler("chatstate_active", self.callback_active)
        self.add_event_handler("chatstate_composing", self.callback_composing)
        self.add_event_handler("chatstate_paused", self.callback_paused)
        self.add_event_handler("chatstate_inactive", self.callback_inactive)

    async def callback_para_session_start(self, evento):
        self.send_presence()
        await self.get_roster()

    async def callback_active(self, evento):
        print(f"{evento['from'].bare} está activo")

    async def callback_composing(self, evento):
        print(f"{evento['from'].bare} está escribiendo...")

    async def callback_paused(self, evento):
        print(f"{evento['from'].bare} ha parado de escribir")

    async def callback_inactive(self, evento):
        print(f"{evento['from'].bare} está inactivo")

    async def callback_para_message(self, evento):
        if evento["type"] == "chat":
            body = evento["body"].strip()
            if body.startswith("="):
                try:
                    resultado = str(eval(body[1:]))
                except Exception as e:
                    resultado = f"Error: {e}"
            else:
                resultado = f"¿{body}?"

            msg = self.Message()
            msg["to"] = evento["from"]
            msg["type"] = "chat"
            msg["body"] = resultado
            msg["chat_state"] = "active"
            msg.send()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")

    jid = os.environ.get("BOT_JID") or input("JID del bot (ej. bot@ingserv222): ")
    clave = os.environ.get("BOT_PASS") or getpass.getpass("Contraseña del bot: ")
    ip = os.environ.get("XMPP_HOST") or input("IP del servidor (ej. localhost): ")
    puerto = 5222

    cliente = MiBot(jid, clave)
    cliente.register_plugin("xep_0085")

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    cliente.ssl_context = ssl_context

    cliente.connect((ip, puerto))
    cliente.process(forever=True)
