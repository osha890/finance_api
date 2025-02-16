# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Команда запуска контейнера (указывается в docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
