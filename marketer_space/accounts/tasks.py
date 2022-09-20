# Create your tasks here
from config.celery import app
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    print("################################## I'm here ######################################")
    return sum(numbers)


