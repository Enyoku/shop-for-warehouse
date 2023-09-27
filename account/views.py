from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.serializers import SignUpSerializer, UserSerializer


@api_view(['POST'])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password']),
            )
            return Response({'details': 'Successfully registered'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User is already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    current_user = User.objects.get(email=request.user)
    serializer = UserSerializer(current_user, many=False)
    return Response({'user': serializer.data})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']

    if data['password'] != "":
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    
    return Response(serializer.data)
