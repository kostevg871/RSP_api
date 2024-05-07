FROM python:3.12.3

COPY . .

RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN pip install -r requirements.txt

CMD ["uvicorn", "main.py", "--host", "--port", "80"]