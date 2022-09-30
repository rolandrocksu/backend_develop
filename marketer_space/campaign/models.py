from django.db import models
from accounts.models import Account
from django_fsm import FSMField, transition
from django.core.validators import FileExtensionValidator


# Create your models here.

class Campaign(models.Model):

    goal = models.CharField(max_length=50)
    scheduled_time = models.DateTimeField()
    status = FSMField(default='NOT STARTED', protected=True)
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False
    )

    @transition(field=status, source='NOT STARTED', target='STARTED')
    def to_started(self):
        pass

    @transition(field=status, source='STARTED', target='PAUSED')
    def to_paused(self):
        pass

    @transition(field=status, source=['STARTED', 'PAUSED'], target='COMPLETED')
    def to_completed(self):
        pass


class CsvInfo(models.Model):
    file_path = models.FileField('csv', upload_to='csv/',
                                 validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    uploaded_by = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=False
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, null=False, related_name='csv_info'
    )


class Contacts(models.Model):
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    csv_file = models.ForeignKey(
        'CsvInfo', on_delete=models.SET_NULL, null=True
    )


class CampaignTemplate(models.Model):
    subject = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    campaign_id = models.ForeignKey(
        'Campaign', on_delete=models.SET_NULL, null=True, related_name='campaign_template'
    )
