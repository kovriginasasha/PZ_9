@echo off
chcp 65001 >nul
cd /d %~dp0
if not exist venv (
    echo [1/3] Создаю виртуальное окружение...
    python -m venv venv
)
echo [2/3] Устанавливаю зависимости...
call venv\Scripts\activate
pip install -q -r requirements.txt
echo [3/3] Запускаю приложение: http://localhost:8080/docs
python main.py
pause
