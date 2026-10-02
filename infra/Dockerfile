FROM node:20-alpine AS frontend-builder
WORKDIR /app

COPY package.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM python:3.11-slim AS runner
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt-get/list/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai/ ./ai
COPY infra/ ./infra
COPY .env* ./

COPY --from=frontend-builder /app/dist ./dist

ENV PYTHONUMBUFFERED=1 PYTHONPATH=/app

EXPOSE 8000

CMD ["python3", "ai/scripts/check_llm_connecetion.py"]
