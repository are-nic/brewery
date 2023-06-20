# Базовый образ Python
FROM python:3.10-alpine3.18

# Установка зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        default-libmysqlclient-dev \
        rabbitmq-server \
    && rm -rf /var/lib/apt/lists/*

# Копирование кода проекта в контейнер
COPY . /accounting
WORKDIR /accounting

# Установка зависимостей Python
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов настроек Nginx
COPY nginx.conf /etc/nginx/sites-available/default

# Открытие порта для Gunicorn
EXPOSE 8000

# Запуск сервера Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]