# FROM python:3.7

# WORKDIR /app

# COPY ./webapp/ /app

# RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uwsgi","app.ini"]

FROM tiangolo/uwsgi-nginx-flask:python3.7

WORKDIR /app

COPY ./webapp/ /app

RUN chmod +x /app/app.py

# RUN pip install --no-cache-dir -r requirements.txt