# syntax=docker/dockerfile:1

FROM python:3

COPY . /app/

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install -r requirements.txt

#CMD ["python", "marketer_space/manage.py", "runserver"]
