from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetTokenView, SignUpView, UsersViewSet

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path('v1/auth/token/', GetTokenView.as_view(), name='token_verify'),
]
