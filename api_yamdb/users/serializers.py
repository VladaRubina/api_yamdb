from rest_framework import serializers

from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """Docstring."""

    class Meta:
        model = CustomUser
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

    # def create(self, validated_data):
    # return super().create(validated_data)
