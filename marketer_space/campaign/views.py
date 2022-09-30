from django.shortcuts import render
import json
import io
from django.core.serializers import serialize
from .tasks import fill_contacts_from_csv, send_report, check_campaign_schedule_time
import csv
from drf_fsm.mixins import FsmViewSetMixin
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import (
    CampaignSerializer,
    ContactsSerializer,
    CsvInfoSerializer,
    CampaignTemplateSerializer
)
from .models import (
    Campaign,
    Contacts,
    CsvInfo,
    CampaignTemplate
)


class CampaignViewSet(FsmViewSetMixin, viewsets.ModelViewSet):
    serializer_class = CampaignSerializer
    queryset = Campaign.objects.all()
    fsm_fields = ['status']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id
        data = {
            'user': user_id,
            'goal': request.data.get('goal', ''),
            'scheduled_time': request.data.get('scheduled_time', ''),
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = {
            'goal': request.data.get('goal'),
            'scheduled_time': request.data.get('scheduled_time'),
            'campaign_template': request.data.get('campaign_template'),
        }
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Campaign.objects.none()
        elif user.is_superuser:
            return Campaign.objects.all()
        else:
            return Campaign.objects.filter(user=user.id)


class CSVInfoViewSet(viewsets.ModelViewSet):
    serializer_class = CsvInfoSerializer
    queryset = CsvInfo.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = {
            'file_path': request.FILES['file_path'],
            'uploaded_by': user.id,
            'campaign': request.data.get('campaign', '')
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        csv_path = f'csv/{data["file_path"]}'
        file_id = serializer.data.get('id')

        error_count, contacts_count = fill_contacts_from_csv(csv_path, 2)

        # send_report.delay(error_count, contacts_count, user.email)
        check_campaign_schedule_time.delay()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Campaign.objects.none()
        elif user.is_superuser:
            return Campaign.objects.all()
        else:
            return Campaign.objects.filter(uploded_by=user.id)


class CampaignTemplateView(viewsets.ModelViewSet):
    serializer_class = CampaignTemplateSerializer
    queryset = CampaignTemplate.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            'subject': request.data.get('subject', ' '),
            'content': request.data.get('content', ' '),
            'campaign_id': request.data.get('campaign_id', ' ')
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactsView(viewsets.ModelViewSet):
    serializer_class = ContactsSerializer
    queryset = Contacts.objects.all()
    permission_classes = [IsAuthenticated]
