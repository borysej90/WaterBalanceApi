from rest_framework import status
from rest_framework.response import Response

REQUIRED_MISSING_RESPONSE = Response({'message': "required fields missing"}, status=status.HTTP_400_BAD_REQUEST)


class Validate:
    """Class used to validate requests data."""

    @staticmethod
    def user_request(data):
        """
        Validate User request data.

        Args:
            data (dict): Dictionary containing User data.

        Returns:
            Response: True if data valid, otherwise False.
        """

        valid = 'language' in data and 'id' in data

        return valid
