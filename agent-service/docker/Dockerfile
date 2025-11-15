FROM python:3.12.11-slim

RUN apt-get update && apt-get install -y \
    pkg-config \
    # default-libmysqlclient-dev \
    build-essential \
    #for docling
    libgl1 libglib2.0-0 curl wget git procps \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY requirements/ /app/requirements/

RUN uv pip install -r requirements/ocr.txt --no-cache-dir --system

# Install docling-tools and download models
RUN docling-tools models download

RUN uv pip install -r requirements/base.txt --no-cache-dir --system

RUN uv pip install -r requirements/langchain.txt --no-cache-dir --system
RUN uv pip install -r requirements/server.txt --no-cache-dir --system

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "main:app"]