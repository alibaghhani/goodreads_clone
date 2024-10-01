

from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

