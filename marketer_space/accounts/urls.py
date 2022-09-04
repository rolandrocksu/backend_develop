from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyObtainTokenPairView,
    AccountViewSet,
    OrganizationViewSet)
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('organizations', OrganizationViewSet)


urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
    # path('accounts/', AccountView.as_view(), name="account"),
    # path('organizations/', OrganizationView.as_view(), name="organization")
]