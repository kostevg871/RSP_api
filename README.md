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
5432 - номер порта базы данных (стандарт)
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
- Дальше вводим: `alembic upgrade heads` - вносяться изменения в базу данных

### Docker

```
sudo chmod 666 /var/run/docker.sock - добавление доступа к сборке образов (для linux)
docker run -it --rm rsp_api-app bash - запустить bash в докере

docker compose build - запустить сборку приложения (rsp_api-app)
docker compose up - поднять контейнеры

docker-compose -f .\docker-compose-local.yaml up -d - еще команда для поднятия контейнеров
docker ps - просмотр запущенных контейнеров


docker compose -f docker-compose-local.yaml up -d - запуск локальной базы для разработки
docker compose -f docker-compose-local.yml down - отключение локально базы для разработки
```

