from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .services import requests
from .services.db import LanguageDB, UsersDB

udb = UsersDB()
ldb = LanguageDB()


@api_view(['POST'])
def save_user(request):
    data = request.data

    if not requests.Validate.user_request(data):
        return requests.REQUIRED_MISSING_RESPONSE

    lang = ldb.get_by_name(data['language'])

    if lang is None:
        return Response({'message': 'invalid language'}, status=status.HTTP_400_BAD_REQUEST)

    data['language'] = lang
    user = udb.get(data['id'])

    try:
        if user is not None:
            serializer = udb.update(model=user, data=data)
        else:
            serializer = udb.create(data)
    except ValidationError:
        return Response({'message': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def load_user(request, user_id):
    user = udb.get_as_dict(user_id)

    if user is None:
        return Response({'message': f'user with that id {user_id} can not be found'},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response(user, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, user_id):
    user = udb.get(user_id)

    if user is None:
        return Response({'message': f'user with that id {user_id} can not be found'},
                        status=status.HTTP_400_BAD_REQUEST)

    user.delete()

    return Response(status=status.HTTP_200_OK)
