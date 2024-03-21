from rest_framework import serializers

from django.utils.text import gettext_lazy as _
from datetime import datetime

class RegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    birth = serializers.DateField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    zipcode = serializers.CharField(required=True)

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

class CertificationNumberSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    certification_number = serializers.CharField(required=True)

class FindEmailSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)