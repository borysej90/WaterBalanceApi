from django.db.models import Model, QuerySet
from rest_framework.serializers import ModelSerializer

from ..models import Language, User
from ..serializers import LanguageSerializer, UserSerializer


class ModelsDB:
    """
    `ModelsDB` used as bridge between **database** and **Django Models**

    To start working with it, create an instance with **Model** you want
    to use.

    Args:
        model (Model): Model to operate with.
    """

    def __init__(self, model):
        self._model = model

    def get(self, pk):
        """
        Returns single Model object if exists.

        Args:
            pk: Model's Primary key.

        Raises:
            django.db.models.Model.DoesNotExist: If there is no model with that primary key.
        """

        user = self._model.objects.get(pk=pk)
        return user

    def get_all(self):
        """
        Returns all existing Models from database.

        Returns:
            QuerySet: Queryset with all Models if exists.
        """

        users = self._model.objects.all()

        return users

    def create(self, data):
        """
        Creates single Model object, saves it to database and returns its Serializer. If Model with that primary key is
        already exists returns `None`.

        Args:
            data (dict): Dictionary containing Model fields to create.

        Returns:
            ModelSerializer: Serializer based on passed data or None if Model already exists.

        Raises:
            ValidationError: if data is not valid for Model.
        """

        # Get a name of Primary Key field
        pk_name = self._model._meta.pk.name

        # Get a Primary Key value from passed data
        pk = data.get(pk_name)

        if pk is not None and self.get(pk) is not None:
            return None

        serializer = self._serialize(data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer

    def update(self, model, data):
        """
        Updates Model with new data, saves it to database and returns it Serializer.

        Args:
            model (ModelSerializer): Existing Model to update.
            data (dict): Dictionary containing Model fields to update.

        Returns:
            ModelSerializer: Serializer based on passed model and data.

        Raises:
            ValidationError: if data is not valid for Model.
        """

        serializer = self._serialize(data, model=model)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer

    def _serialize(self, data, model=None) -> ModelSerializer:
        raise NotImplemented


class UsersDB(ModelsDB):
    """UsersDB is a bridge between **database** and **User Models**"""

    def __init__(self):
        super().__init__(User)

    def _serialize(self, data, model=None):
        data_copy = data.copy()
        if isinstance(data['language'], Language):
            data_copy['language'] = data['language'].id

        return UserSerializer(instance=model, data=data_copy)

    def get_as_serializer(self, user_id: int):
        """
        Gets User Model as dictionary if exists, otherwise returns empty `dict`.

        Returns:
            UserSerializer: Dictionary with User Model fields as keys or empty.

        Raises:
            django.db.models.Model.DoesNotExist: If there is no User with that user_id.
        """

        user = self.get(user_id)

        return UserSerializer(user)

    def get_all_as_serializer(self):
        """
        Gets all User Models if exist, otherwise returns empty `list`.

        Returns:
             UserSerializer: UserSerializer with User Models.
        """

        users = self.get_all()

        serializer = UserSerializer(users, many=True)

        return serializer


class LanguageDB(ModelsDB):
    """LanguageDB is a bridge between **database** and **Language Models**"""

    def __init__(self):
        super().__init__(Language)

    def _serialize(self, data, model=None):
        return LanguageSerializer(instance=model, data=data)

    def get_by_name(self, name):
        """
        Returns single Language object if exists, otherwise returns `None`

        Raises:
            django.db.models.Model.DoesNotExist: If there is no User with that user_id.
        """

        lang = self._model.objects.get(name=name)

        return lang
