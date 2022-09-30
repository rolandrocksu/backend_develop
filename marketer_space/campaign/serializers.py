from rest_framework import serializers
from .models import (
    Campaign,
    Contacts,
    CsvInfo,
    CampaignTemplate
)


class CampaignTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignTemplate
        fields = ('subject', 'content', 'campaign_id')


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ('csv_file', 'email', 'first_name', 'last_name', 'company_name', 'job_title')


class CsvInfoSerializer(serializers.ModelSerializer):
    contacts = ContactsSerializer(many=True, read_only=True)

    class Meta:
        model = CsvInfo
        fields = ('file_path', 'uploaded_at', 'uploaded_by', 'campaign', 'contacts')


class CampaignSerializer(serializers.ModelSerializer):
    csv_info = CsvInfoSerializer(many=True, read_only=True)
    campaign_template = CampaignTemplateSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ('id', 'goal', 'scheduled_time', 'user', 'status', 'campaign_template', 'csv_info')

