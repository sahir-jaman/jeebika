from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.response import Response

import logging
logger = logging.getLogger(__name__)

from applicants.models import Applicant
from accountio.models import User
from common.choices import UserType



class PublicApplicantRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Applicant
        fields = ['name', 'email', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('confirm_password')

        if password != password2:
            raise serializers.ValidationError({"Error": ["Passwords do not match!"]})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email", None)
        name = validated_data.pop("name", None)
        
        if name is None:
            raise serializers.ValidationError({"Error": ["You must have a name!"]})
        if email is not None:
            email_existance = User.objects.filter(email = email)
            if email_existance:
                raise serializers.ValidationError({"Error": ["This email already exists!"]})

        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                type=UserType.APPLICANT,
            )
            applicant = Applicant.objects.create(user=user, name=name, password=make_password(password))
            
            return applicant

        except Exception as e:
            logger.error(f"Registration failed. Error: {str(e)}")
            raise serializers.ValidationError({"Error": ["Sorry, Registration failed!"]})
        
    def to_representation(self, instance):
        payload = {"message": f"Registration successful for {instance.name}."}
        return payload

    
class PublicApplicantLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(max_length=228)
    class Meta:
        model = User
        fields = ["email", "password"]
        
class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'type']

class PrivateApplicantProfileSerializer(serializers.ModelSerializer):
    user = PrivateUserSerializer()

    class Meta:
        model = Applicant
        fields = ["uid", "name", "user"]