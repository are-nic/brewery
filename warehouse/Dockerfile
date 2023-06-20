# Базовый образ Python
FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копирование кода проекта в контейнер
WORKDIR /brewery

# Установка зависимостей Python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /warehouse