from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import User
from .services import persistence, requests
from .services.db import LanguageDB, UsersDB

udb = UsersDB()
ldb = LanguageDB()


@api_view(['POST'])
def save_user(request, user_id):
    body = request.data

    try:
        requests.Validate.user_request(body)

        serializer = persistence.save_user(user_id, body)
    except ValidationError as e:
        return Response(e.detail, e.status_code, exception=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def load_user(request, user_id):
    try:
        user_data = persistence.load_user(user_id)
    except User.DoesNotExist:
        return Response({'message': "user not found"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def load_all_users(request):
    users = persistence.load_all_users()

    return Response(users, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, user_id):
    body = request.data

    try:
        requests.Validate.is_id_match(user_id, body)
    except ValidationError as e:
        return Response(e.detail, status=e.status_code, exception=True)

    user = None
    try:
        user = persistence.delete_user(user_id)
    except User.DoesNotExist:
        return Response({'message': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(user, status=status.HTTP_200_OK)
