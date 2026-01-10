FROM python:latest
LABEL authors="denischepik"
WORKDIR /django-app
COPY . /django-app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
