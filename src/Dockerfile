FROM python:3.12-alpine

# Install packages
RUN apk add --no-cache --update supervisor

# Upgrade pip
RUN python -m pip install --upgrade pip

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Create user and chmod /app
RUN adduser -s /bin/sh -S webapp
RUN chown -R webapp /app

# Add application
COPY requirements.txt .
COPY application.py .
COPY unshorten.py .
RUN python -m pip install -r requirements.txt 

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 8000

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# start supervisord
COPY --chown=root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
