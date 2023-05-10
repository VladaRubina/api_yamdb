from rest_framework import serializers
from reviews.models import User


class SignupSerializer(serializers.ModelSerializer):
    """Docstring."""

    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(max_length=254)

    # def create(self, validated_data):
    #     try:
    #         user = User.objects.get_or_create(
    #             username=validated_data['username'],
    #             email=validated_data['email'],
    #         )
    #     except KeyError as err:
    #         raise serializers.ValidationError(f'Отсутствует ключ{err}')
    #     return user

    class Meta:
        model = User
        fields = ('username', 'email')

    # def create(self, validated_data):
    # return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Docstring."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = (
            'id',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
