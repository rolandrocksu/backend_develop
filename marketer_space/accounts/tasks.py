# Create your tasks here
from logging import log
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    log.info("################################## I'm here ######################################")
    return sum(numbers)
