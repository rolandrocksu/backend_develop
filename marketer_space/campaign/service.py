from django.core.mail import send_mail
from celery import shared_task
from config.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status

import smtplib


def send_email(subject, message, receiver):
    try:
        send_mail(
            subject=subject,
            from_email=EMAIL_HOST_USER,
            message=message,
            recipient_list=receiver,
        )
    except smtplib.SMTPException:
        return Response(
            {'message': 'Error for SMTP misconfiguration - Having trouble'
                        ' sending an activation email. Please, contact to'
                        ' our support.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
