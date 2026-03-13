FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install mysql-connector-python python-dotenv

CMD ["python", "seed.py"]