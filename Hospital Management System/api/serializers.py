from rest_framework import serializers
from app.models import *

class UserWithUserTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserWithUserType
        fields = '__all__'