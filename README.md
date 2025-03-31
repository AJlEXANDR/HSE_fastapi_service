# HSE FastAPI Short Link Service

## 📘 Описание API

🔗 Сервис позволяет сокращать длинные ссылки, задавать для них срок жизни, получать статистику переходов, использовать кастомные алиасы, а также управлять своими ссылками через регистрацию и авторизацию.

### Основные эндпоинты

#### 🔐 Авторизация и пользователи

- `POST /auth/jwt/login` — вход пользователя
- `POST /auth/jwt/register` — регистрация пользователя
- `GET /auth/users/me` — получить текущего пользователя
- `PATCH /auth/users/me` — обновить данные профиля

#### 🔗 Работа со ссылками

- `POST /links/shorten` — создать короткую ссылку
- `GET /{short_code}` — переход по короткой ссылке (публичный)
- `GET /links/{short_code}/stats` — статистика по ссылке (количество переходов, дата создания, последнего использования и т.д.)
- `GET /links/search?original_url=` — найти ссылку по оригинальному адресу
- `PUT /links/{short_code}` — обновить оригинальную ссылку
- `DELETE /links/{short_code}` — удалить ссылку

## 📡 Примеры запросов

### POST /links/shorten

```json
{
  "original_url": "https://example.com/very/long/url",
  "custom_alias": "myalias",  // необязательно
  "expires_at": "2025-03-30T12:30:00"  // необязательно
}
```

Ответ:

```json
{
  "id": "12345678-abcdefg-...",
  "short_code": null,
  "original_url": "https://example.com/very/long/url",
  "custom_alias": "myalias",
  "created_at": "2025-03-29T12:30:00",
  "expires_at": "2025-03-30T12:30:00",
  "short_url": "http://localhost:8000/myalias"
}
```

### GET /myalias

```
307 Temporary Redirect на оригинальный URL
```

### GET /links/myalias/stats

```json
{
  "original_url": "https://example.com/very/long/url",
  "clicks": 1,
  "created_at": "2025-03-29T12:30:00",
  "last_clicked": "2025-03-29T12:31:00",
  "expires_at": "2025-03-30T12:30:00"
}
```

### GET /links/search?original_url=https\://example.com/very/long/url

```json
[
  {
    "id": "12345678-abcdefg-...",
    "short_code": null,
    "original_url": "https://example.com/very/long/url",
    "custom_alias": "myalias",
    "created_at": "2025-03-29T12:30:00",
    "clicks": 1
  }
]
```

## ⚙️ Инструкция по запуску

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Работа с миграциями
alembic upgrade head

# Запуск приложения
uvicorn src.main:app
```

Создайте файл `.env` в корне и добавьте туда настройки:

```
DB_USER=your_user
DB_PASS=your_pass
DB_HOST=your_host
DB_PORT=1234
DB_NAME=your_db_name

JWT_SECRET_KEY=your_SECRET
DEFAULT_EXPIRATION_DAYS=30
```

## 🗃️ Описание базы данных

### Модель User (от FastAPI Users)

- `id`: UUID
- `email`: str
- `hashed_password`: str
- `is_active`: bool
- `created_at`: datetime

### Модель ShortURL

- `id`: UUID
- `original_url`: str — оригинальная длинная ссылка
- `short_code`: str — сгенерированный alias
- `custom_alias`: Optional[str] — кастомный alias, если был задан
- `clicks`: int — количество переходов
- `created_at`: datetime — Дата создания ссылки
- `expires_at`: Optional[datetime] — Дата окончания работы ссылки
- `last_used`: Optional[datetime] — Последнее время перехода по ссылке
- `user_id`: Optional[UUID] — владелец ссылки (может быть null)

## 📎 Дополнительно

- Неавторизованные пользователи могут создавать ссылки, но управлять (удалять, обновлять) — только после регистрации