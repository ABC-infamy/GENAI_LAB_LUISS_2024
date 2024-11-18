FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

EXPOSE 8080

COPY . /app

#CMD ["python", "api.py"]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]