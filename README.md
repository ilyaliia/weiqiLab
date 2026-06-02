# Weiqi Lab — Лаборатория для обучения и игры в Го

## Описание
Веб-приложение для обучения игре Го: уроки, задачи, интерактивная доска, рейтинг и онлайн-игра.

## 🚀 Быстрый старт

### Требования
- Python 3.10+
- pip

### Установка

```bash
cd weiqiLab
pip install -r requirements.txt
```

### Запуск

```bash
python main.py
```

Приложение откроется на `http://127.0.0.1:8000`

## 📚 API документация

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 📁 Структура проекта

```
weiqiLab/
├── api/              # Маршруты API
│   ├── auth.py       # Авторизация, регистрация, logout
│   ├── users.py      # Профили, друзья, заявки
│   ├── books.py      # Материалы, учебники
│   ├── game.py       # Игра между пользователями
│   └── puzzles.py    # Задачи (цуме-го)
├── models/           # Модели БД (SQLAlchemy)
│   ├── users.py
│   ├── friends.py
│   ├── books.py
│   ├── game.py
│   └── puzzles.py
├── schemas/          # Pydantic-схемы для запросов/ответов
│   ├── auth/
│   ├── users/
│   ├── books/
│   ├── game/
│   └── puzzles/
├── core/             # Утилиты
│   ├── security.py   # Хеширование паролей (Argon2)
│   └── dependencies.py # Зависимости (JWT, текущий пользователь)
├── engine/           # Логика игры
│   └── board.py      # Интерактивная доска 19x19
├── bots/             # ИИ и боты
├── uploads/          # Загруженные материалы
├── database.py       # Конфиг БД (SQLAlchemy + SQLite)
├── main.py           # Точка входа
├── requirements.txt   # Зависимости
└── README.md         # Документация
```

## 🔐 Ключевые эндпоинты

### Авторизация
- `POST /register` — Регистрация нового пользователя
- `POST /login` — Вход в аккаунт
- `POST /logout` — Выход из аккаунта
- `POST /setup_database` — Создание БД (только разработка)

### Пользователи
- `GET /users/{username}` — Получить профиль по юзернейму
- `GET /users/me` — Получить мой профиль
- `PATCH /users/me` — Обновить профиль (био, аватар, страна, язык)
- `GET /users/me/friends` — Список друзей
- `GET /users/me/friends/requests` — Входящие заявки
- `POST /users/me/friends/{user_id}` — Отправить заявку
- `PATCH /users/me/friends/{user_id}` — Ответить на заявку (accept/decline)

## 🔧 Разработка

### Первый запуск (создание БД)
```bash
curl -X POST http://127.0.0.1:8000/setup_database
```

### Тестирование API
Используй **Swagger UI** на `http://127.0.0.1:8000/docs` — там можно протестировать все эндпоинты прямо в браузере.

### Пример: Регистрация через curl
```bash
curl -X POST "http://127.0.0.1:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "saito",
    "email": "saito@example.com",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

### Пример: Вход
```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "saito",
    "password": "password123"
  }'
```

## 📊 Модель данных

### User (Пользователь)
```
- id, username, email, password_hash
- avatar_filename, bio, country, language
- rating (ELO), games_played, games_won_in_row, win_rate
- created_at, last_seen, is_online
- is_admin, permissions (JSON)
```

### Friends (Друзья)
```
- sender_id, receiver_id, status (pending/accepted/declined)
```

### Остальные модели
- **Game** — партии между пользователями
- **Puzzles** — задачи (цуме-го)
- **Books** — учебники и материалы

## 🎯 Планы развития

### Высокий приоритет ✅ / ⏳
- [x] Авторизация, профили, друзья
- [x] Роли игрок/админ (структурно)
- [ ] Загрузка материалов
- [ ] Категории книг по сложности
- [ ] API для списка/поиска материалов

### Средний приоритет
- [ ] Интерактивная доска 19x19
  - [ ] Базовые правила Го
  - [ ] Подсчёт очков
  - [ ] История ходов
- [ ] Материалы задач (цуме-го)
  - [ ] Генератор задач
  - [ ] Проверка решений
  - [ ] Прогресс пользователя
- [ ] Игра против ИИ (начальный уровень)
- [ ] Система уроков/курсов

### Низкий приоритет
- [ ] Лидерборд (система рейтинга)
- [ ] Материалы (профессиональные партии)
- [ ] Турнирная система
- [ ] Онлайн-игра между пользователями
- [ ] Чат во время игры
- [ ] Мобильное приложение
- [ ] Интеграция с OGS/KGS

## 🔒 Безопасность

- Пароли хешируются через **Argon2**
- Авторизация через **JWT** (токены в cookies)
- `access_token` срок действия — 7 дней
- `refresh_token` срок действия — 30 дней

## 🗄️ База данных

- **SQLite** с поддержкой асинхронности (`aiosqlite`)
- **SQLAlchemy** ORM
- Файл БД: `weiqi.db` (создаётся при первом запуске)

## 🛠️ Стек технологий

- **FastAPI** — веб-фреймворк
- **Uvicorn** — ASGI сервер
- **SQLAlchemy** — ORM
- **Pydantic** — валидация данных
- **AuthX** — JWT авторизация
- **Passlib** — хеширование паролей
- **aiosqlite** — асинхронный драйвер SQLite

## 📝 Лицензия

MIT

## 👨‍💻 Контрибьютинг

Приветствуются pull requests и issues!
