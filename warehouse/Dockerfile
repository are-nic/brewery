# Базовый образ Python
FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копирование кода проекта в контейнер
WORKDIR /usr/src/warehouse

# Установка зависимостей Python
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# создание директории для статики
RUN mkdir ./static

COPY . .