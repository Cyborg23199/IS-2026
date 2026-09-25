#!/bin/bash
# Script to launch three UDP broadcast servers in Docker

NETWORK_NAME="pruebas"

# Ensure the network exists
docker network inspect $NETWORK_NAME >/dev/null 2>&1 || docker network create $NETWORK_NAME

echo "Starting server 1..."
docker run -d --name srv1 --network $NETWORK_NAME \
  -v "$(pwd)":/app python:3.7 python /app/udp_servidor6_broadcast.py

echo "Starting server 2..."
docker run -d --name srv2 --network $NETWORK_NAME \
  -v "$(pwd)":/app python:3.7 python /app/udp_servidor6_broadcast.py

echo "Starting server 3..."
docker run -d --name srv3 --network $NETWORK_NAME \
  -v "$(pwd)":/app python:3.7 python /app/udp_servidor6_broadcast.py

echo "All 3 servers are running. Check status with: docker ps"