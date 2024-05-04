FROM python:3.12.3

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "main.py", "--host", "--port", "80"]