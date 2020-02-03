FROM python:3.7

WORKDIR /app

COPY ./webapp/ /app

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python app.py
