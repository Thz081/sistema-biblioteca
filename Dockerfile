
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala Nginx e Supervisor
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências do backend
COPY backendcombanco/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copia o backend
COPY backendcombanco/app ./backendcombanco/app
COPY backendcombanco/database ./backendcombanco/database

# Copia o frontend estático
COPY frontend-biblioteca/index.html /usr/share/nginx/html/
COPY frontend-biblioteca/config.js /usr/share/nginx/html/
COPY frontend-biblioteca/script.js /usr/share/nginx/html/
COPY frontend-biblioteca/assets/ /usr/share/nginx/html/assets/
COPY frontend-biblioteca/style.css /usr/share/nginx/html/

# Configuração do Nginx
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Configuração do Supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Usuário sem privilégios
RUN useradd --system --uid 10001 --create-home appuser \
    && mkdir -p /tmp/nginx \
    && chown -R appuser:appuser /app /usr/share/nginx/html /tmp/nginx

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/health', timeout=3)"

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
