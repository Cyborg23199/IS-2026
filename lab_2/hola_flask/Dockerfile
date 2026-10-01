# Base image
FROM python:3.7

# Optional maintainer information
# MAINTAINER Jose Luis Diaz <jldiaz@uniovi.es>

# Install application dependencies globally inside the container
RUN pip install --no-cache-dir flask gunicorn

# Prepare application directory and copy source code
RUN mkdir /app
COPY hola_flask.py /app

# Set default working directory
WORKDIR /app

# Document the port the application listens on
EXPOSE 5000

# Default command executed when starting the container
CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "hola_flask:app"]