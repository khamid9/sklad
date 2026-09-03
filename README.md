# Мой Склад

Система управления складом для товаров, поставок и продаж.

## Возможности

- регистрация пользователей с ручным одобрением администратора;
- роли администратора и владельца склада;
- каталог товаров с поиском по названию, артикулу, штрих-коду и ID;
- серверная пагинация каталога;
- создание и редактирование товаров;
- приём партий по коробкам и количеству единиц;
- поиск товара USB-сканером штрих-кодов или ручным вводом;
- продажи с автоматическим уменьшением остатка;
- запрет продажи при недостаточном остатке;
- журнал операций и статистика;
- управление пользователями из админ-панели;
- адаптивный интерфейс для компьютера, планшета и телефона.

## Структура

```text
backend/   FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT
frontend/  React, Vite, React Router, Axios, Recharts
```

## Локальный запуск

### Backend

Требуются Python 3.11+ и PostgreSQL.

```powershell
cd backend
Copy-Item .env.example .env
# Заполните DATABASE_URL, SECRET_KEY, POSTGRES_PASSWORD и ADMIN_EMAIL
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

API: `http://localhost:8000`  
Документация: `http://localhost:8000/docs`

### Frontend

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Сайт: `http://localhost:5173`

## Docker

```powershell
cd backend
Copy-Item .env.example .env
docker compose up --build
```

Compose запускает PostgreSQL, применяет миграции, поднимает API и собирает frontend в nginx. Перед запуском обязательно измените секреты в `.env`.

## Рабочий процесс доступа

1. Пользователь регистрируется.
2. Его заявка появляется в админ-панели со статусом ожидания.
3. Администратор одобряет или удаляет пользователя.
4. После одобрения пользователь может войти и работать со своим складом.

## Production

Для публикации укажите реальный адрес API через `VITE_API_URL`, включите HTTPS, используйте отдельные секреты и настройте резервное копирование PostgreSQL. Frontend можно разместить на Vercel, а FastAPI и PostgreSQL требуют отдельного сервера или managed-хостинга.