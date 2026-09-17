# API для Yatube

REST API для социальной платформы Yatube. Через API можно читать и создавать
публикации и комментарии, просматривать сообщества, подписываться на авторов и
искать подписки. Изменять и удалять публикацию или комментарий может только его
автор. Для аутентификации используются JWT-токены.

## Технологии

- Python 3.11
- Django 5.1
- Django REST Framework 3.15
- Simple JWT

## Локальный запуск

Клонируйте репозиторий и перейдите в его директорию:

```bash
git clone <адрес-репозитория>
cd api_final_yatube
```

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate
```

Для Windows команда активации:

```powershell
venv\Scripts\activate
```

Установите зависимости, примените миграции и запустите сервер:

```bash
python -m pip install -r requirements.txt
python yatube_api/manage.py migrate
python yatube_api/manage.py runserver
```

Документация будет доступна по адресу
`http://127.0.0.1:8000/redoc/`.

## Примеры запросов

Получить список публикаций:

```http
GET /api/v1/posts/
```

Получить JWT-токены:

```http
POST /api/v1/jwt/create/
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

Создать публикацию:

```http
POST /api/v1/posts/
Authorization: Bearer <access-токен>
Content-Type: application/json

{
  "text": "Новая публикация",
  "group": 1
}
```

Подписаться на автора:

```http
POST /api/v1/follow/
Authorization: Bearer <access-токен>
Content-Type: application/json

{
  "following": "author"
}
```
