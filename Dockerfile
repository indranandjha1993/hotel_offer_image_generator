FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN mkdir -p /app/images /app/fonts

ENV PYTHONPATH=/app

FROM base as final

EXPOSE 8000
CMD ["python", "run_api.py"]