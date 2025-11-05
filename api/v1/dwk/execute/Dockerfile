FROM python:3.12-slim

WORKDIR /python-docker
EXPOSE 5000
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]