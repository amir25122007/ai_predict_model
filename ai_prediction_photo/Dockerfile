FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for Pillow + basic builds
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libjpeg62-turbo \
      zlib1g \
      libpng16-16 \
      libfreetype6 \
      libglib2.0-0 \
      libsm6 \
      libxext6 \
      libxrender1 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
