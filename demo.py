"""Демонстрация работы: прогоняет все маршруты и печатает ответы.
Запускать при уже работающем приложении (run.bat) и MongoDB."""
import json
import sys
import time

import requests

BASE = "http://127.0.0.1:8080"
uniq = str(int(time.time()))


def show(title, resp):
    print(f"\n=== {title}")
    print(f"{resp.request.method} {resp.request.url.replace(BASE, '')}  ->  HTTP {resp.status_code}")
    try:
        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except ValueError:
        print(resp.text)


def get_id(doc):
    return doc.get("id") or doc.get("_id")


try:
    requests.get(BASE + "/docs", timeout=3)
except requests.exceptions.ConnectionError:
    sys.exit("Приложение не запущено. Сначала запустите run.bat (и MongoDB).")

print("##### Ветка /training (персональная тема: фитнес-клуб) #####")
title = "Йога " + uniq
r = requests.post(f"{BASE}/training/new", json={
    "title": title, "trainer": "Иванова А.", "hall": "Зал 2",
    "start_time": "2026-11-05T08:00:00", "capacity": 2})
show("1. Создание занятия (Create)", r)

r = requests.get(f"{BASE}/training/")
show("2. Все занятия (Read all)", r)
tid = get_id(next(t for t in r.json() if t["title"] == title))

show("3. Одно занятие по ID (Read one)", requests.get(f"{BASE}/training/{tid}"))
show("4. Запись клиента a@b.ru", requests.post(f"{BASE}/training/{tid}/enroll", json={"email": "a@b.ru"}))
show("5. Повторная запись a@b.ru (ожидаем 409)", requests.post(f"{BASE}/training/{tid}/enroll", json={"email": "a@b.ru"}))
show("6. Запись второго клиента c@d.ru", requests.post(f"{BASE}/training/{tid}/enroll", json={"email": "c@d.ru"}))
show("7. Мест нет, третий клиент (ожидаем 400)", requests.post(f"{BASE}/training/{tid}/enroll", json={"email": "e@f.ru"}))
show("8. Частичное обновление: hall -> Зал 3 (Update)", requests.put(f"{BASE}/training/{tid}", json={"hall": "Зал 3"}))
show("9. Поиск по тренеру", requests.get(f"{BASE}/training/search/by-trainer", params={"trainer": "Иванова А."}))
show("10. Удаление (Delete)", requests.delete(f"{BASE}/training/{tid}"))
show("11. Повторный GET удалённого (ожидаем 404)", requests.get(f"{BASE}/training/{tid}"))

print("\n\n##### Маршруты /event из методички #####")
r = requests.post(f"{BASE}/event/new", json={
    "title": "FastAPI Book Launch " + uniq, "image": "https://linktomyimage.com/image.png",
    "description": "Обсуждение книги", "tags": ["python", "fastapi"], "location": "Google Meet"})
show("12. Создание события", r)
r = requests.get(f"{BASE}/event/")
ev = next(e for e in r.json() if e["title"].endswith(uniq))
eid = get_id(ev)
show("13. Обновление location -> Hybrid", requests.put(f"{BASE}/event/{eid}", json={"location": "Hybrid"}))
show("14. Удаление события", requests.delete(f"{BASE}/event/{eid}"))

print("\n\n##### Маршруты /user #####")
email = f"user{uniq}@mail.ru"
show("15. Регистрация", requests.post(f"{BASE}/user/signup", json={"email": email, "password": "strong!!!", "events": []}))
show("16. Повторная регистрация (ожидаем 409)", requests.post(f"{BASE}/user/signup", json={"email": email, "password": "strong!!!", "events": []}))
show("17. Вход с верным паролем", requests.post(f"{BASE}/user/signin", json={"email": email, "password": "strong!!!"}))
show("18. Вход с неверным паролем (ожидаем 401)", requests.post(f"{BASE}/user/signin", json={"email": email, "password": "wrong"}))
print("\nГотово.")
