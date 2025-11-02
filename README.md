# Bonecca Telegram Bot Project

## Описание

- Асинхронный Telegram-бот (aiogram)
- SQLite storage
- Система плагинов
- Мини-приложение Web Admin для Telegram (Web App, открывается через команду `/admin`)
- Админка: статистика, управление пользователями/группами, help, плагины, рестарт

## Запуск

1. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```

2. Впишите свой токен в `main.py`
    ```python
    API_TOKEN = 'YOUR_BOT_TOKEN'
    ```

3. Запустите проект одной командой:
    ```
    python run.py
    ```

4. В Telegram напишите боту команду `/admin` и откройте WebApp мини-приложение.

## Как создавать плагины

Смотрите файл [PLUGIN_GUIDE.md](PLUGIN_GUIDE.md).