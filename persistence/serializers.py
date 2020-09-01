from rest_framework.serializers import ModelSerializer

from .models import Language, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'language', 'last_remind', 'start_silence', 'end_silence', 'timezone', 'has_reminding']


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']
