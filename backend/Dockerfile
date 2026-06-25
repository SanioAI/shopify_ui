# Build: docker build -f Dockerfile.shopify-api -t shopify-api:latest .
# Run:  docker run --rm -p 8080:8080 --env-file .env shopify-api:latest
#
# We copy only api_server + Shopify modules (not COPY . .) so src/, data/, etc. stay out of the image.

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_server.py shopify_config.py shopify_http.py shopify_token_store.py shopify_oauth.py ./
COPY shopify_app/ ./shopify_app/
COPY shopify_writeback/ ./shopify_writeback/

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -sf http://127.0.0.1:8080/api/health || exit 1

CMD ["gunicorn", "api_server:app", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "600"]