## Активация виртуального окружения:

    source .venv/bin/activate


## Запуск:

    poetry run uvicorn app:create_app --host 0.0.0.0 --port 8000 --reload

    poetry run uvicorn app:create_app --reload