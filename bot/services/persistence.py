from . import requests
import datetime
from ..models import Language, User
from ..serializers import UserSerializer
from rest_framework import exceptions


def save_user(user_id, data):
    """
    Save User with data passed to database.

    Args:
         user_id (int): ID in Telegram of a user to save.
         data (dict): User's data to save.

    Returns:
        UserSerializer: created or updated User object wrapped in Serializer.

    Raises:
        request.InvalidRequestData: If `data` argument is not valid.
    """

    data['language'] = Language.objects.get(name=data['language'])

    if {'start_silence', 'end_silence'} <= set(data):
        data['start_silence'] = datetime.time.fromisoformat(data['start_silence'])
        data['end_silence'] = datetime.time.fromisoformat(data['end_silence'])

    user, created = User.objects.update_or_create(data, id=user_id)

    serializer = UserSerializer(user)

    return serializer


def load_user(user_id):
    """
    Load User with corresponding ID.

    Args:
        user_id (int): ID in Telegram of a user to load.

    Returns:
        dict: Loaded User object if exists.

    Raises:
        User.DoesNotExists: If no user found with passed ID.
    """

    user = User.objects.select_related('language').get(id=user_id)

    output = UserSerializer(user).data

    output['language'] = user.language.name

    if {'start_silence', 'end_silence'} <= set(output):
        output['start_silence'] = output['start_silence'].isoformat()
        output['end_silence'] = output['end_silence'].isoformat()

    return output


def load_all_users():
    """
    Load all existing Users.

    Returns:
         list: List of dictionaries of User objects.
    """

    users = User.objects.select_related('language').all()

    users_data = UserSerializer(users, many=True).data

    for i, user in enumerate(users):
        users_data[i]['language'] = user.language.name

    return users_data


def delete_user(user_id):
    """
    Deletes User with passed ID.

    Args:
        user_id (int): ID of User to delete.

    Returns:
        dict: Deleted User's ID in dictionary.

    Raises:
        User.DoesNotExists: If no user found with passed ID.
    """

    user = User.objects.get(id=user_id)

    user.delete()

    return {'id': user_id}
