# Практическая работа: FastAPI + MongoDB (Beanie)

Тема: сайт управления фитнес-клубом. Коллекции: `events`, `users`, `trainings`.
Новая ветка маршрутов: `/training` (CRUD + запись на занятие + поиск по тренеру).

## Запуск (Windows)

**1. MongoDB** -- один из вариантов:
- Docker: `docker compose up -d` (файл docker-compose.yml уже в папке);
- или установленный локально: `mkdir store` и `mongod --dbpath store`.

**2. Приложение:** двойной клик по `run.bat`
(создаст venv, поставит зависимости, запустит сервер).
Документация и ручная проверка: http://localhost:8080/docs

**3. Показ работы:** при запущенном приложении двойной клик по `demo.bat`.
Скрипт прогоняет все маршруты и печатает коды ответов и JSON.

## Запуск (Linux/Mac)
```
docker compose up -d
./run.sh
# в другом окне:
source venv/bin/activate && python demo.py
```

## Структура
```
main.py                  точка входа, подключение роутеров, lifespan
database/connection.py   Settings (.env), init_beanie, класс Database (CRUD)
models/                  документы Beanie: events, users, trainings
routes/                  маршруты: events, users, trainings
demo.py                  автоматическая демонстрация всех маршрутов
REPORT.md                материалы для отчёта (use case, сценарии, BPMN)
```

## Git
```
git init && git add . && git commit -m "Лаб. работа: FastAPI + MongoDB"
git remote add origin <URL> && git push -u origin main
git checkout -b feature/trainings && git push -u origin feature/trainings
```
