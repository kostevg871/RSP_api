# ** RSP App **

# Swagger UI - http://rsp-api.online/docs#/

## Команды

### Первый запуск:

```
python -m venv venv - создание локального окружения
.\venv\Scripts\activate - запуск локального окружения
```

<!--pip install -r .\requirements.txt - установка всех зависимостей-->

<!--pip freeze > requirements.txt - соххранение локальных зависимостей-->
<!--py pip install git+https://github.com/fiztexlabs/librsp.git - установка библиотеки-->

### Контроль зависимостей

```
poetry install - проверка и установка зависимостей
poetry add "пакет" - добавление "пакета"
poetry update --only rsp - обновление ТОЛЬКО rsp
```

### Для запуска:

```
uvicorn app:app --reload - запуск сервера
http://127.0.0.1:8000/docs#/ - Swagger или localhost:8000
uvicorn app:app --host 0.0.0.0 --port 80 - запуск на сервере
```

### Тестирование

pytest - запуск тестов
pytest --tb=long -vv - более подробное описание