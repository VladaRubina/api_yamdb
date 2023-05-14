from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, GetTokenView, SignUpView,
                    TitleViewSet, UsersViewSet)

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        SignUpView.as_view(),
        name='signup',
    ),
    path('v1/auth/token/', GetTokenView.as_view(), name='token_verify'),
]
