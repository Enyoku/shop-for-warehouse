import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Profile
from account.serializers import SignUpSerializer, UserSerializer
from utils.common import get_current_host


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
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    current_user = User.objects.get(email=request.user)
    serializer = UserSerializer(current_user, many=False)
    return Response({'user': serializer.data}, status=status.HTTP_200_OK)


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

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = User.objects.get(email=request.user)
    user.delete()
    return Response({'details': 'deleted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def forgot_password(request):
    data = request.data

    user = get_object_or_404(User, email=data['email'])

    token = get_random_string(length=32)
    exp_date = datetime.datetime.now() + datetime.timedelta(minutes=30)

    user.profile.reset_password_token = token
    user.profile.reset_password_expire = exp_date

    user.profile.save()

    host = get_current_host(request)
    link = f"{host}/api/account/reset_password/{token}"

    msg = f"Здравствуйте, {user.first_name}.\n Скопируйте приведеную ниже ссылку и вставьте её в адресную строку браузера.\n {link}"

    send_mail(
        subject="Инструкция по сбросу пароля.",
        message=msg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[data['email']]
    )

    return Response({'details': 'Инструкция по сбросу пароля отправлена на почту: {email}'.format(email=data['email'])})


@api_view(['POST'])
def reset_password(request, token):
    data = request.data

    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.datetime.now():
        return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['confirm_password']:
        return Response({"error": "Passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)

    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None

    user.profile.save()
    user.save()

    return Response({'details': 'Passwords reset successfully'})
