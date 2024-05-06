## Настройка

## Команды

Первый запуск:
py -m venv venv - создание локального окружения
.\venv\Scripts\activate - запуск локального окружения
pip install -r .\requirements.txt - установка всех зависимостей

<!--pip freeze > requirements.txt - соххранение локальных зависимостей-->
<!--py pip install git+https://github.com/fiztexlabs/librsp.git - установка библиотеки-->

Для запуска:
uvicorn main:app --reload - запуск сервера
http://127.0.0.1:8000/docs#/ - Swagger или localhost:8000
