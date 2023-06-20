# Базовый образ Python
FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей
# RUN apk update && apk add mysql-server libmysqlclient-dev

# Копирование кода проекта в контейнер
COPY . /warehouse
WORKDIR /warehouse

# Установка зависимостей Python
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt