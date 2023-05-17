from api_yamdb.settings import ADMIN_EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title, User

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import IsAdmin, IsAuthorModeratorOrReadOnly, IsAuthorModeratorAdminOrReadOnly,  IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          SignupSerializer, ReadOnlyTitleSerializer,
                          TitleSerializer, TokenSerializer, UserSerializer,
                          ReviewSerializer, CommentsSerializer)

# class CategoryViewSet(generics.ListCreateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     filter_backends = (SearchFilter,)
#     search_fields = ("name",)
#     lookup_field = "slug"

class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = (IsAdminUser) #000000000000000000000000000000000000000000000000000000
    filter_backends = (filters.SearchFilter)
    search_fields = ("name",)
    lookup_field = "slug"


class SignUpView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.data)
        user.save()
        confirmation_code = default_token_generator.make_token(user)
        mail_subject = 'Подтверждение регистрации'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(mail_subject, message, ADMIN_EMAIL, [user.email])
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(generics.CreateAPIView):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data.get('username')
        )
        confirmation_code = serializer.validated_data.get('confirmation_code')
        if default_token_generator.check_token(user, confirmation_code):
            token = {'token': str(AccessToken.for_user(user))}
            return Response(token, status=status.HTTP_200_OK)
        return Response(
            serializer.error_messages, status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(ModelViewSet):
    """Docstring."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('username',)
    permission_classes = [IsAdmin]
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_users(self, request):
        users = User.objects.all()
        serialaizer = UserSerializer(users)
        return Response(serialaizer.data, status=status.HTTP_200_OK)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #permission_classes = (IsAdminUser) #000000000000000000000000000000000000000000000000000000000
    filter_backends = (filters.SearchFilter)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")    
    serializer_class = TitleSerializer
    #permission_classes = (IsAdminOrReadOnly) #00000000000000000000000000000000000000000000000000000000000
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title

    def get_queryset(self):
        title = self.get_title()   
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly]

    def get_title(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title
    
    def get_queryset(self):
        title = self.get_title()
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('Отзыв отсутствует')
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = self.get_title()
        try:
            review = title.reviews.get(id=self.kwargs.get('review_id'))
        except TypeError:
            TypeError('Отзыв отсутствует')
        serializer.save(author=self.request.user, review=review)
