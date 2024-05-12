# Build the frontend
FROM node:22.1-alpine3.18 as build

WORKDIR /build
COPY ./client /build
RUN npm ci
RUN npm run build

# Switch to main image
FROM ubuntu:22.04

# Install dependencies
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y software-properties-common python3 python3-launchpadlib gnupg curl
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
RUN echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
RUN apt-get update && apt-get install -y nginx supervisor python3.12 mongodb-org
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.12
RUN apt-get clean && apt-get autoremove --purge && rm -rf /var/lib/apt/lists/*

# Setup supervisor
RUN mkdir -p /var/log/supervisor
COPY ./docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup nginx
COPY --from=build /build/dist /frontend
COPY ./docker/default /etc/nginx/sites-available/default

# Setup FastAPI
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /backend
COPY ./server /backend
RUN python3.12 -m pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Setup MongoDB
RUN mkdir -p /data/db

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
