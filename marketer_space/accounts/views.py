from django.shortcuts import render
import datetime
import pytz
import smtplib
import uuid
from datetime import timedelta
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import Account, Organization
from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse
from .models import Invitation
from rest_framework import status
from .serializers import (
    MyTokenObtainPairSerializer,
    AccountSerializer,
    OrganizationSerializer,
    InvitationSerializer
)
from rest_framework.response import Response
from .mixin import PermissionPolicyMixin
from .permissions import (
    IsSuperAdmin,
    IsOrganizationAdmin,
    IsUser
)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.none()
    permission_classes_per_method = {
        "list": [IsOrganizationAdmin | IsSuperAdmin],
        "retrieve": [IsUser | IsOrganizationAdmin | IsSuperAdmin],
        "create": [IsOrganizationAdmin | IsSuperAdmin],
        "update": [IsUser | IsOrganizationAdmin | IsSuperAdmin],
        "partial_update": [IsOrganizationAdmin | IsSuperAdmin],
        "destroy": [IsOrganizationAdmin | IsSuperAdmin],
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Account.objects.none()
        elif user.is_superuser:
            return Account.objects.all()
        elif user.is_org_admin:
            return Account.objects.filter(organization=user.organization)
        else:
            return Account.objects.filter(id=user.id)


class OrganizationViewSet(PermissionPolicyMixin, viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.none()
    permission_classes_per_method = {
        "list": [IsSuperAdmin],
        "retrieve": [IsOrganizationAdmin | IsSuperAdmin],
        "create": [IsSuperAdmin],
        "update": [IsOrganizationAdmin | IsSuperAdmin],
        "partial_update": [IsOrganizationAdmin | IsSuperAdmin],
        "destroy": [IsOrganizationAdmin | IsSuperAdmin],
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Organization.objects.none()
        elif user.is_superuser:
            return Organization.objects.all()
        else:
            return Organization.objects.filter(id=user.organization.id)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class InviteUserApiView(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    permission_classes = [AllowAny]
    permission_classes_per_method = {
        "create": [IsOrganizationAdmin | IsSuperAdmin],
    }

    def create(self, request, *args, **kwargs):
        invitor = self.request.user
        token = uuid.uuid4().hex
        link = reverse(
            "invited-registration",
            kwargs={
                'token': token
            }
        )
        subject = f'Invitation from {invitor.full_name}: {invitor.organization.name}'
        message = f'{invitor.full_name} has invited you to join {invitor.organization.name} organization: \n' \
                  f'Please follow the link[http://{request.get_host()}{link}] to create account'
        print(message)
        data = {
            'invitor': invitor.email,
            'organization': invitor.organization.pk,
            'receiver': request.data.get('receiver', ''),
            'status': request.data.get('status', ''),
            'token': token
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        try:
            send_mail(
                subject=subject,
                from_email=EMAIL_HOST_USER,
                message=message,
                recipient_list=[request.data.get('receiver', '')],
            )
        except smtplib.SMTPException:
            return Response(
                {'message': 'Error for SMTP misconfiguration - Having trouble'
                            ' sending an activation email. Please, contact to'
                            ' our support.'},
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers
            )

        return Response({'message': "Your email has been sent successfully"}, status=status.HTTP_201_CREATED,
                        headers=headers)


class InviteUserCreationView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        token = kwargs.get('token')
        invite_info = Invitation.objects.get(token=token)

        if (invite_info.created_at + timedelta(1)) > datetime.datetime.utcnow().replace(tzinfo=pytz.UTC):
            data = {
                'email': invite_info.receiver,
                'organization': invite_info.organization.pk,
                'is_admin': request.GET.get('is_admin', False),
                'is_superuser': request.GET.get('is_superuser', False),
                'first_name': request.POST.get('first_name', ''),
                'last_name': request.POST.get('first_name', ''),
                'profile_picture': request.POST.get('profile_picture'),
                'country': request.POST.get('country'),
                'password': request.POST.get('password')
            }
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response({'message': 'The invitation link is expired'}, status=status.HTTP_400_BAD_REQUEST,)
