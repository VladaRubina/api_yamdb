# Create your views here.
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

# from django.http import BadHeaderError, HttpResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from reviews.models import User

from api_yamdb.settings import ADMIN_EMAIL

from .permissions import IsAdmin, IsAuthorOrReadOnly, IsModerator
from .serializers import SignupSerializer, UserSerializer

# from rest_framework_simplejwt.tokens import AccessToken


class SignUpView(CreateAPIView):
    """Docstring."""

    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    permission_classes = [AllowAny]

    def perform_create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)
            # if self.request.user.username == 'me':
            #     raise ValueError('Нельзя использовать это имя!')
            serializer.save()
            username = serializer.data['username']
            email = serializer.data['email']
            user = get_object_or_404(User, username=username, email=email)
            self.send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def send_confirmation_code(user):
        code = default_token_generator.make_token(user)
        user_mail = user.email
        subject = 'Код подтверждения регистрации'
        message = f'Ваш код: {code}'
        from_email = ADMIN_EMAIL
        to_email = (f'{user_mail}',)
        return send_mail(subject, message, from_email, to_email)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    permission_classes = [IsAdminUser]
    lookup_field = 'username'


class Category(ModelViewSet):
    pass


class Genre(ModelViewSet):
    pass


class Title(ModelViewSet):
    pass


class Review(ModelViewSet):
    pass


class Comment(ModelViewSet):
    pass
