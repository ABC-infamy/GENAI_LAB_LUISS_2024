FROM python:3.11-slim

WORKDIR /app/workers

COPY ./requirements.txt /app/workers/

RUN pip install --upgrade pip && pip install -r /app/workers/requirements.txt

COPY . /app/workers/

ENV PYTHONPATH=/app

CMD ["python", "worker.py"]
