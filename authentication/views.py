







from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import UserSerializer
from authentication.models import User


class RegisterUserViewSet(ViewSet):
    """
    Register a new user.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'invalid form'}, status=status.HTTP_403_FORBIDDEN)





