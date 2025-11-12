# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /python-docker

RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY .. .

EXPOSE 5000

CMD [ "python3", "-m", "flask", "run" ]