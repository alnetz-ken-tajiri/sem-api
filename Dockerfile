# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 依存ファイルを先にコピー
COPY requirements.txt .

# ---- OS パッケージと Python 依存をインストール ----
RUN apt-get update && apt-get install -y \
        gcc libxml2-dev libxslt1-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
# ------------------------------------------------------

# アプリケーションコード
COPY app/ ./app

EXPOSE 8000

# dev 用：--reload（本番では外す）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
