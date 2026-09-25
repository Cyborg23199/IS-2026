#!/bin/bash
# Script to launch UDP broadcast client in Docker

NETWORK_NAME="pruebas"
BROADCAST_IP=${1:-"172.18.255.255"}

echo "Running broadcast client using broadcast IP: $BROADCAST_IP"

docker run -it --rm --network $NETWORK_NAME --name cliente_broadcast \
  -v "$(pwd)":/app python:3.7 \
  python /app/udp_cliente6_broadcast.py "$BROADCAST_IP"