# ** RSP App **

# Swagger UI - http://rsp-api.online/docs#/

## Команды

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
```
pytest - запуск тестов
pytest --tb=long -vv - более подробное описание
```

```
pytest --cov .  - процент покрытия тестами 
pytest --cov-report html --cov . - процент покрытия тестами, в виде отчета в html
```