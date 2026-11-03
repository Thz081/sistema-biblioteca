FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y nginx \
    && rm -rf /var/lib/apt/lists/*

COPY backendcombanco/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backendcombanco/app/ /app/app/
COPY backendcombanco/init_db.py /app/init_db.py
COPY backendcombanco/app/start.sh /app/start.sh
COPY frontend-biblioteca/ /tmp/frontend/

RUN mkdir -p /usr/share/nginx/html \
    && cp -r /tmp/frontend/. /usr/share/nginx/html/ \
    && chmod +x /app/start.sh \
    && mkdir -p /tmp/nginx/body /tmp/nginx/proxy /tmp/nginx/fastcgi /tmp/nginx/uwsgi /tmp/nginx/scgi \
    && chown -R 10001:999 /tmp/nginx /usr/share/nginx/html

COPY frontend-biblioteca/nginx/default.conf /etc/nginx/sites-available/default

RUN sed -i 's|/run/nginx.pid|/tmp/nginx/nginx.pid|' /etc/nginx/nginx.conf \
    && sed -i 's|/var/log/nginx/error.log|/dev/stderr|' /etc/nginx/nginx.conf \
    && sed -i 's|/var/log/nginx/access.log|/dev/stdout|' /etc/nginx/nginx.conf

EXPOSE 80

CMD ["/app/start.sh"]
