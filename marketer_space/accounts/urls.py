from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyObtainTokenPairView,
    AccountViewSet,
    OrganizationViewSet,
    InviteUserApiView,
    InviteUserCreationView
)
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('organizations', OrganizationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('invitations/', InviteUserApiView.as_view({'post': 'create'}), name='invitation-mail'),
    path('invited/register/<str:token>', InviteUserCreationView.as_view({'post': 'create'}),
         name='invited-registration'),
    # path('accounts/', AccountView.as_view(), name="account"),
    # path('organizations/', OrganizationView.as_view(), name="organization")
]
