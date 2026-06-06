# 🔐 JWT Auth Service

> Развитие и переосмысление оригинального проекта [Demo User Authentication Methods](https://github.com/Gleboster/Demo-user-authentication-methods).
>
> От учебной демонстрации различных способов аутентификации к отдельному сервису авторизации на FastAPI с JWT, PostgreSQL, Docker и современной Python-инфраструктурой.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python\&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136+-009688?logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?logo=postgresql\&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker\&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Что внутри

Проект создавался как практическое исследование того, как должен выглядеть современный сервис аутентификации на FastAPI.

В репозитории реализованы:

* 🛡️ JWT-аутентификация по схеме **Access + Refresh Tokens**
* 🐳 Docker-инфраструктура с отдельными конфигурациями для `dev` и `prod`
* ⚡ Управление зависимостями через **uv**
* 🗃️ Миграции базы данных на **Alembic**
* 🏗️ Слоистая архитектура с разделением на DAL, DTO, Mappers и Services
* 🔑 Работа с пользователями, регистрацией, входом и обновлением токенов
* 🧪 База для дальнейшего расширения и интеграции в более крупные системы

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/Gleboster/auth_2.0.git
cd auth_2.0
```

### 2. Настрой окружение

```bash
cp .env.example .env
# Отредактируй .env — задай свои пароли и JWT-секрет
```

### 3. Запусти через Docker

**Development** (с горячей перезагрузкой и пробросом портов):
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```
- API: http://localhost:8090
- PostgreSQL: `localhost:5433`

**Production**:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```
- API: http://localhost:8000

---

## 📡 API Endpoints

| Метод | Эндпоинт | Описание | Авторизация |
|-------|----------|----------|-------------|
| `GET` | `/jwt_auth/public` | Публичные данные | Не требуется |
| `POST` | `/jwt_auth/users` | Регистрация | Не требуется |
| `POST` | `/jwt_auth/tokens` | Логин (получить токены) | Не требуется |
| `POST` | `/jwt_auth/tokens/refresh` | Обновить Access-токен | Bearer + Refresh |
| `GET` | `/jwt_auth/protected` | Защищённые данные | Bearer |
| `GET` | `/jwt_auth/users/me` | Информация о себе | Bearer |
| `DELETE` | `/jwt_auth/sessions/me` | Выйти (revoke refresh) | Bearer |
| `DELETE` | `/jwt_auth/users/me` | Удалить аккаунт | Bearer |

> Полная интерактивная документация доступна по `/docs` (Swagger UI) или `/redoc` (ReDoc).

---

## 🏗️ Архитектура проекта

```
auth_2.0/
├── src/
│   ├── api/
│   │   ├── schemes/          # Pydantic-схемы запросов/ответов
│   │   └── v1/
│   │       ├── dependencies/ # FastAPI Depends (DB, сервисы, текущий юзер)
│   │       └── handlers/     # Роутеры и контроллеры
│   ├── core/
│   │   ├── configs/          # Pydantic Settings (DB, Auth)
│   │   ├── dto/              # Data Transfer Objects
│   │   ├── mappers/          # Преобразования ORM ↔ DTO
│   │   ├── security/         # Хеширование, JWT-кодек
│   │   └── utils/            # Вспомогательные функции
│   ├── infrastructure/
│   │   └── db/
│   │       ├── connections/  # SQLAlchemy Engine & Session
│   │       ├── dals/         # Data Access Layer
│   │       └── models/       # SQLAlchemy ORM-модели
│   └── services/             # Бизнес-логика (Auth & User)
├── alembic/                  # Миграции базы данных
├── docker/
│   ├── dev/app/Dockerfile    # Dev-образ с uv + reload
│   └── prod/app/Dockerfile   # Production-образ (минималистичный)
├── docker-compose.yml        # Базовая конфигурация сервисов
├── docker-compose.dev.yml    # Оверлей для разработки
├── docker-compose.prod.yml   # Оверлей для продакшена
├── pyproject.toml            # Зависимости и метаданные (uv)
└── requirements.txt          # Фиксированные зависимости для prod
```

---

## 🔑 Модель безопасности

| Токен | TTL (по умолчанию) | Хранение | Назначение |
|-------|-------------------|----------|------------|
| **Access Token** | 15 минут | Только в памяти клиента | Доступ к защищённым ресурсам |
| **Refresh Token** | 7 дней | База данных (UUID + expire_at) | Получение новой пары токенов |

- Пароли хешируются через **bcrypt**
- Refresh-токены **ротируются** — при обновлении старый удаляется, выдаётся новый
- Алгоритм подписи: **HS256**

---

## 🛠️ Технологический стек

- **Python 3.12+**
- **FastAPI** — асинхронный веб-фреймворк
- **Uvicorn** — ASGI-сервер
- **SQLAlchemy 2.0** — ORM с поддержкой asyncio
- **PostgreSQL** — реляционная БД
- **asyncpg / psycopg** — асинхронные драйверы PostgreSQL
- **Alembic** — миграции схемы БД
- **PyJWT** — работа с JSON Web Tokens
- **bcrypt + passlib** — надёжное хеширование паролей
- **Pydantic Settings** — типизированная конфигурация через ENV
- **uv** — современный менеджер зависимостей и виртуальных окружений
- **Docker & Docker Compose** — контейнеризация и оркестрация

---

## 🧪 Пример использования

### Регистрация
```bash
curl -X POST "http://localhost:8090/jwt_auth/users" \
  -H "Content-Type: application/json" \
  -d '{"username": "gleb", "password": "supersecret", "bio": "Backend dev"}'
```

### Логин
```bash
curl -X POST "http://localhost:8090/jwt_auth/tokens" \
  -H "Content-Type: application/json" \
  -d '{"username": "gleb", "password": "supersecret"}'
# → {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}
```

### Доступ к защищённому ресурсу
```bash
curl -X GET "http://localhost:8090/jwt_auth/protected" \
  -H "Authorization: Bearer <access_token>"
```

### Обновление токенов
```bash
curl -X POST "http://localhost:8090/jwt_auth/tokens/refresh" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

---

## 🐳 Docker-инфраструктура

Проект использует **многоконфигурационный Docker Compose**:

- `docker-compose.yml` — общая часть (сети, тома, зависимости)
- `docker-compose.dev.yml` — проброс портов `8090` (app) и `5433` (DB), dev-образ с `uv` и hot-reload
- `docker-compose.prod.yml` — порт `8000`, production-образ на чистом `pip`, только скомпилированные артефакты

---

## 📁 Переменные окружения

Создай `.env` на основе `.env.example`:

```env
# Database
DB_USER=postgres
DB_PASS=your_secure_password
DB_NAME=jwt_access_refresh_auth_db
DB_HOST=localhost
DB_PORT=5432

# JWT
AUTH_JWT_SECRET_KEY=openssl_rand_hex_32
AUTH_JWT_ALGORITHM=HS256
AUTH_ACCESS_TOKEN_TTL=900
AUTH_REFRESH_TOKEN_TTL=604800
```

---

## 🔄 Миграции

Локально (если PostgreSQL доступна на хосте):
```bash
alembic upgrade head
```

Внутри контейнера:
```bash
docker compose exec jwt_auth alembic upgrade head
```

---

## 📜 Лицензия

MIT — бери, учись, форкай, улучшай. Идеи из оригинального репозитория приветствуются: [Demo-user-authentication-methods](https://github.com/Gleboster/Demo-user-authentication-methods)

---

<p align="center">
  Сделано с ❤️
</p>
