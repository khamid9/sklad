# Мой Склад — Backend

## Локальный запуск

1. Установите Python 3.12+ и PostgreSQL.
2. Создайте БД `my_sklad`, скопируйте `.env.example` в `.env` и задайте безопасный `SECRET_KEY`.
3. В терминале выполните:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API: `http://localhost:8000`, Swagger: `http://localhost:8000/docs`.

## Docker

Если установлен Docker Desktop:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Начальная миграция уже включена. После изменения моделей создавайте новую: `alembic revision --autogenerate -m "описание изменения"`, затем `alembic upgrade head`.
