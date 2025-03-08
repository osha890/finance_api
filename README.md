# Finance API using DRF

## Описание
Проект представляет собой систему для ведения личной бухгалтерии с использованием API. Пользователи могут отслеживать свои доходы, расходы и баланс в реальном времени, а также получать информацию о расходах или доходах по счетам и категориям, основываясь на добавленных финансовых операциях.

### 1. Аутентификация и безопасность
Система использует безопасную аутентификацию через токены, чтобы обеспечить доступ к личной информации только авторизованным пользователям.

### 2. Модели данных:
- **Счета**: Пользователи могут создавать несколько счетов, таких как "Кошелек", "Банк", "Кредитная карта", с возможностью отслеживания баланса.
- **Операции**: Возможность добавления операций, с указанием типа (доходы, расходы), категории, счета, суммы и описания.
- **Категории расходов/доходов**: Пользователи могут настраивать категории для классификации своих операций (например, еда, развлечения, зарплата и т.д.). По умолчанию у каждого пользователя имеется одна категория для доходов и одна для расходов.

### 3. API для взаимодействия:
- Все данные можно будет получать и отправлять через API, что позволяет интегрировать систему с внешними сервисами, такими как мобильные приложения или чат-боты.
- API поддерживает создание, чтение, обновление и удаление (CRUD-операции) данных пользователей, с фильтрацией по дате, категориям и типам операций.

### 4. Телеграм-бот:
- Бот для взаимодействия с API, позволяющий быстро добавлять операции, просматривать баланс прямо из Telegram - https://github.com/osha890/finance_tg_bot.

**Проект протестирован с помощью pytest**

---

## Технологии
- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Docker, Docker-compose

---

## Установка и запуск с Docker-compose

### Клонирование репозитория
```sh
git clone https://github.com/osha890/finance_api.git
cd finance_api
```

### Настройка
Создайте файл `.env` в рабочей директории и укажите в нем параметры, указанные в примере. Пример:
```
POSTGRES_DB=finance_api
POSTGRES_USER=osha
POSTGRES_PASSWORD=qwerty123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY='django-insecure-_8su_lkhyoh+2t)%)gpo(5u0t9v!*gf%vtau338*7h($938jp#'
DEBUG=True
```

### Запуск
Запустите контейнеры:
```docker compose up```

API будет доступно по адресу http://localhost:8000/.

### Создание суперпользователя (админа)
Просмотрите запущенные контейнеры:
```sh
docker ps
```

Запустите команду внутри контейнера c образом `finance_api` для создания суперпользователя:
```sh
docker exec -it <container_id> python manage.py createsuperuser
```
Запустите команду для создания токена для суперпользователя:
```sh
docker exec -it <container_id> python manage.py drf_create_token <superuser_name>
```
Сохраните токен для аутентификации.

---

## Установка и запуск без Docker-compose

### Клонирование репозитория
```sh
git clone https://github.com/osha890/finance_api.git
cd finance_api
```

### Создание виртуального окружения и установка зависимостей
Виртуальное окружение позволяет изолировать зависимости проекта, чтобы избежать конфликтов с глобально установленными пакетами.

#### Создание виртуального окружения
Для macOS и Linux:
```sh
python3 -m venv venv
```
Для Windows:
```sh
python -m venv venv
```

#### Активация виртуального окружения
Для macOS и Linux:
```sh
source venv/bin/activate
```
Для Windows (в командной строке):
```sh
venv\Scripts\activate
```
Для Windows (в PowerShell):
```sh
venv\Scripts\Activate.ps1
```

После активации виртуального окружения в командной строке появится префикс `(venv)`, указывающий, что окружение активно.

#### Установка зависимостей
```sh
pip install -r requirements.txt
```

### Настройка
Создайте базу данных postgres. Затем создайте файл `.env` в рабочей директории и укажите в нем параметры, указанные в примере. Пример:
```
POSTGRES_DB=finance_api  # имя базы данных, которую вы создали
POSTGRES_USER=osha
POSTGRES_PASSWORD=qwerty123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY='django-insecure-_8su_lkhyoh+2t)%)gpo(5u0t9v!*gf%vtau338*7h($938jp#'
DEBUG=True
```
В файле finance_api/settings.py найдите словарь `DATABASES`. Раскомментируйте строчку `# 'HOST': env('POSTGRES_HOST'),` и закомментируйте или удалите строчку `'HOST': 'db',`. Измененный словарь должен выглядеть так:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        # 'HOST': env('POSTGRES_HOST'),
        'HOST': 'db',
        'PORT': env('POSTGRES_PORT'),
    }
}
```

Примените миграции:
```sh
python manage.py migrate
```
Создание суперпользователя:
```sh
python manage.py createsuperuser
```
Создание токена для суперпользователя:
```sh
python manage.py drf_create_token <superuser_name>
```
Сохраните токен для аутнетификации.

### Запуск сервера
```sh
python manage.py runserver
```

API будет доступно по адресу http://localhost:8000/.

---

## Использование API
Для удобства используйте сервис для работы с API, например Postman.

### Регистрация
- `POST /api/register/` — зарегистрировать нового пользователя (возвращает `token`)

Все остальные запросы требуют авторизацию. Используйте заголовок Authorization: Token {token}. Например:
`Authorization: Token 5f9b05079002f66108fea596a7b6429c3168fde5`

### Счета (`/api/accounts/`)
- `GET /api/accounts/` — получить список своих счетов
- `POST /api/accounts/` — создать новый счет  
- `GET /api/accounts/{id}/` — получить информацию о счете  
- `PUT /api/accounts/{id}/` — обновить информацию о счете  
- `PATCH /api/accounts/{id}/` — частично обновить счет  
- `DELETE /api/accounts/{id}/` — удалить счет  

### Категории (`/api/categories/`)
- `GET /api/categories/` — получить список своих категорий; параметры для фильтрации:  
  - `?type=<income|expense>` — фильтр по типу категории  
- `POST /api/categories/` — создать новую категорию  
- `GET /api/categories/{id}/` — получить информацию о категории  
- `PUT /api/categories/{id}/` — обновить информацию о категории  
- `PATCH /api/categories/{id}/` — частично обновить категорию  
- `DELETE /api/categories/{id}/` — удалить категорию (нельзя удалить системные категории, если не админ)  

### Операции (`/api/operations/`)
- `GET /api/operations/` — получить список своих операций; параметры для фильтрации:  
  - `?type=<income|expense>` — фильтр по типу операции  
  - `?account=<id>` — фильтр по счету  
  - `?category=<id>` — фильтр по категории  
  - `?date=<YYYY-MM-DD>` — фильтр по точной дате  
  - `?date_after=<YYYY-MM-DD>` — операции, созданные после указанной даты  
  - `?date_before=<YYYY-MM-DD>` — операции, созданные до указанной даты  
- `POST /api/operations/` — создать новую операцию  
- `GET /api/operations/{id}/` — получить информацию об операции  
- `PUT /api/operations/{id}/` — обновить информацию об операции  
- `PATCH /api/operations/{id}/` — частично обновить операцию  
- `DELETE /api/operations/{id}/` — удалить операцию  
- `GET /api/operations/recent/` — получить последние операции; параметры для фильтрации:  
  - `?type=<income|expense>` — фильтр по типу операции
  - `?count=<число>` — количество операций (по умолчанию 5)  

### Пользователи (только для админов) (`/api/users/`)
- `GET /api/users/` — получить список пользователей
- `POST /api/users/` — создать пользователя
- `GET /api/users/{id}/` — получить информацию о пользователе
- `PUT /api/users/{id}/` — обновить информацию о пользователе
- `PATCH /api/users/{id}/` — частично обновить пользователя
- `DELETE /api/users/{id}/` — удалить пользователя

### Токены (только для админов) (`/api/tokens/`)
- `GET /api/tokens/` — получить список токенов

---

## Проект на github - https://github.com/osha890/finance_api
