from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail
from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterViewSet(ModelViewSet):
    """Docstring."""

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    # def get_email(user):
    #     email = CustomUser.kwargs.get('email')
    #     return email

    def send_email(user):
        token = default_token_generator.make_token
        message = 'Код подтверждения'
        email = CustomUser('email')
        if token and message and email:
            try:
                send_mail(
                    token,
                    message,
                    'admin@example.com',
                    [f'{email}'],
                    recipient_list=False,
                )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

    def perform_create(self, serializer):
        return super().perform_create(serializer)
