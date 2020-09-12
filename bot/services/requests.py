from django.conf import settings
from rest_framework.exceptions import ValidationError


class Validate:
    """Class used to validate requests data."""

    @staticmethod
    def user_request(data):
        """
        Validates User request data.

        Args:
            data (dict): Dictionary containing User data.

        Raises:
            ValidationError: If no language field specified.
        """

        if 'language' in data:
            Validate.language_exists(data['language'])
        else:
            raise ValidationError({'message': 'language field is required'})

    @staticmethod
    def language_exists(language):
        """
        Checks whether language exists in database.

        Args:
            language (str): Language name.

        Raises:
            ValidationError: If language does not exist.
        """

        if language not in settings.AVAILABLE_LANGUAGES:
            raise ValidationError({'message': 'language with that name does not exists'})

    @staticmethod
    def is_id_match(id, data):
        """
        Checks if ID matches in both path and body. In this validation ID must be in body.

        This is used to confirm operations (e.g. deletion).

        Args:
              id (int): ID in path.
              data (dict): Deserialized JSON body with potential ID in it.

        Raises:
            ValidationError: If IDs do not match.
        """

        if 'id' not in data or data['id'] != id:
            raise ValidationError({'message': 'ids in path and body do not match'})
