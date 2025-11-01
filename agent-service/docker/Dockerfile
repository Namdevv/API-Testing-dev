FROM python:3.12.11-slim

RUN apt-get update && apt-get install -y \
    pkg-config \
    # default-libmysqlclient-dev \
    build-essential \
    #for docling
    libgl1 libglib2.0-0 curl wget git procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# Install docling-tools and download models
RUN docling-tools models download

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "main:app"]