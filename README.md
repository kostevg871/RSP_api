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
uvicorn src.app:app --reload - запуск сервера
http://127.0.0.1:8000/docs#/ - Swagger или localhost:8000
uvicorn src.app:app --host 0.0.0.0 --port 80 - запуск на сервере
```

### Тестирование
```
pytest - запуск тестов
pytest --tb=long -vv - более подробное описание

pytest --cov .  - процент покрытия тестами 
pytest --cov-report html --cov . - процент покрытия тестами, в виде отчета в html
```

### Библиотеки

```
poetry add psycopg2-binary - postgress для linux (думаю в через doker не понадобиться)
5433 - номер порта базы данных
```

### Миграции

Для накатывания миграций, если alembic.init нет, нужно запустить

```
alembic init migration
```

После этого будет создана папка с миграциями и конфигурационный файл для алембика.

- В alembic.ini нужно задать адрес базы данных, в которую будем катать миграции.
- Дальше идём в папку с миграциями и открываем env.py, там вносим изменения в блок, где написано

```
from myapp import mymodel
```

- Дальше вводим: `alembic revision --autogenerate -m "comment"` - делается при любых изменениях моделей
- Будет создана миграция
- Дальше вводим: `alembic upgrade heads`

### Docker

```
docker-compose -f .\docker-compose-local.yaml up -d
docker ps
```

