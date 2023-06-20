# Базовый образ Python
FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копирование кода проекта в контейнер
WORKDIR /accounting

# Установка зависимостей Python
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /accounting