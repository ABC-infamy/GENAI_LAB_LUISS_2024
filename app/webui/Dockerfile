FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 8501


CMD ["streamlit", "run", "webui/webui.py", "--server.port=8501", "--server.enableCORS=false"]