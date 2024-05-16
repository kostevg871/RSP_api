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
```

### Для запуска:

```
uvicorn main:app --reload - запуск сервера
http://127.0.0.1:8000/docs#/ - Swagger или localhost:8000
uvicorn main:app --host 0.0.0.0 --port 80 - запуск на сервере
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
