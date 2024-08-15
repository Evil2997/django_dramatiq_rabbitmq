# Установка аргументов
ARG IMAGE_NAME="alpine"
ARG IMAGE_TYPE="python"
ARG IMAGE_VERSION=3.19
ARG LANGUAGE_VERSION=3.12

FROM ${IMAGE_TYPE}:${LANGUAGE_VERSION}-${IMAGE_NAME}${IMAGE_VERSION}

RUN apk update && apk add --no-cache \
    bash \
    curl \
    chromium \
    chromium-chromedriver \
    build-base \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    iproute2 \
    iproute2-tc \
    util-linux \
    iputils

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY test_speed.py /test_speed.py

CMD ["python3", "/test_speed.py"]