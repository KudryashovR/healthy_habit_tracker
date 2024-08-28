from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from main.apps import MainConfig
from users.views import UserCreate

app_name = MainConfig.name


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreate.as_view(), name='create_user'),
]
