FROM python:3.12-slim

# Установка зависимостей, включая curl, ping и netcat
RUN apt-get update && apt-get install -y \
    iputils-ping \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --requirement requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
