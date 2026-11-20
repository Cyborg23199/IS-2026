FROM python:3.11-slim

WORKDIR /app
RUN pip install --no-cache-dir wheel slixmpp==1.8.6

COPY bot_completo.py /app/bot.py

CMD ["python", "-u", "/app/bot.py"]
