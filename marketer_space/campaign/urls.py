from .views import (
    CampaignViewSet,
    CSVInfoViewSet,
    CampaignTemplateView,
    ContactsView
)
from django.urls import path, include

urlpatterns = [
    path('campaign/', CampaignViewSet.as_view({'get': 'list', 'post': 'create'}), name="campaign"),
    path('campaign/<int:pk>', CampaignViewSet.as_view({'put': 'update'}), name="campaign-update"),
    path('uploadCsv/', CSVInfoViewSet.as_view({'get': 'list', 'post': 'create'}), name="uploadCsv"),
    path('contacts/', ContactsView.as_view({'get': 'list'}), name="contacts"),
    path('campaign-template/', CampaignTemplateView.as_view({'get': 'list', 'post': 'create'}),
         name="campaignTemplate"),
]
