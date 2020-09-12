from collections import OrderedDict

from rest_framework.serializers import ModelSerializer

from .models import Language, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'language', 'last_remind', 'start_silence', 'end_silence', 'timezone', 'has_reminding']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Here we filter the null values and creates a new dictionary
        # We use OrderedDict like in original method
        ret = OrderedDict(filter(lambda x: x[1] is not None, ret.items()))
        return ret


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']
