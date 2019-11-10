FROM python:3.7

COPY . /app

EXPOSE 80
EXPOSE 8000

WORKDIR /app

RUN pip install -r requirements.txt

CMD flask run --host=0.0.0.0
