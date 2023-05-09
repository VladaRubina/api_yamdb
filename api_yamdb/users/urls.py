from django.urls import path

# from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import RegisterViewSet

# router = DefaultRouter()

# router.register('signup', UserViewSet, basename='auth')


urlpatterns = [
    path(
        'auth/signup/',
        RegisterViewSet.as_view({'post': 'create'}),
        name='signup',
    ),
    path('auth/token/', TokenVerifyView.as_view(), name='token_verify'),
]
