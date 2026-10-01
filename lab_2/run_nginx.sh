#!/bin/bash

# Stop existing container if it is running
docker stop nginx 2>/dev/null

# Launch Nginx container with both sites and configuration mounted
docker run --rm -d \
  --network pruebas \
  --name nginx \
  -p 80:80 \
  -p 81:81 \
  -v "$(pwd)/configuracion_nginx/nginx.conf:/etc/nginx/nginx.conf" \
  -v "$(pwd)/html:/usr/share/nginx/html" \
  -v "$(pwd)/html2:/usr/share/nginx/html2" \
  -v "$(pwd)/sitios_nginx:/etc/nginx/conf.d" \
  nginx
  

echo "Nginx container launched successfully."

