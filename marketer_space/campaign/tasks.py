import csv
import pytz
from django.db.utils import IntegrityError
from campaign.models import CsvInfo, Contacts, Campaign, CampaignTemplate
from config.celery import app
from datetime import datetime
from celery import shared_task
from .service import send_email
from django.utils import timezone


@app.task
def fill_contacts_from_csv(path, file_id):
    with open(path) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        csv_info = CsvInfo.objects.get(id=file_id)
        error_count = 0
        contact_count = 0
        for row in reader:
            try:
                Contacts.objects.update_or_create(first_name=row[0], last_name=row[1], email=row[2],
                                                  company_name=row[3], job_title=row[3], csv_file=csv_info)
            except IntegrityError:
                error_count += 1
            finally:
                contact_count += 1

    return error_count, contact_count


@app.task
def send_report(error_count, contact_count, mail):
    message = f''' 
    All contacts - {contact_count}
    Successful created - {contact_count - error_count}
    Can't create - {error_count}
    '''
    send_email(
        subject='Contact creation report',
        message=message,
        receiver=mail
    )

    return True


@shared_task()
def check_campaign_schedule_time():
    completed_campaigns = []
    all_campaigns = Campaign.objects.all()
    for campaign in all_campaigns:
        if campaign.status == "NOT STARTED" and campaign.scheduled_time < timezone.now():
            campaign.to_started()
            # querysetCsvInfo = CsvInfo.objects.filter(campaign=campaign.id).values('id')
            # querysetContacts = Contacts.objects.filter(csv_file=querysetCsvInfo.id).values('email')
            # querysetTemplate = CampaignTemplate.objects.filter(campaign_id=campaign.id).values('subject', 'content')
            # send_email(
            #     subject=querysetTemplate.subject,
            #     message=querysetTemplate.content,
            #     receiver=querysetContacts.emails
            # )
        # for item in Campaign.objects.prefetch_related('csv_info'):

    return completed_campaigns
