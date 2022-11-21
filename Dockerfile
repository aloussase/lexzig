FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY lexzig lexzig
COPY lexzig_api lexzig_api

ENV PORT=8080

CMD uvicorn --host 0.0.0.0 --port ${PORT} lexzig_api.main:app
