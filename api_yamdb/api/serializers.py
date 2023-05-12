from rest_framework import serializers
from reviews.models import Category, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def to_internal_value(self, data):
        email = data.get('email')
        username = data.get('username')
        if email and username:
            try:
                user = User.objects.get(email=email, username=username)
                return user
            except User.DoesNotExist:
                pass
        return super().to_internal_value(data)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):
    """Docstring."""

    class Meta:
        model = User
        fields = (
            # 'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
