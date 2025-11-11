# syntax=docker/dockerfile:1
FROM python:3.14

ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /python-docker
EXPOSE 5000

RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD [ "python3", "-m", "flask", "run" ]