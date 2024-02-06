from rest_framework import serializers

from accountio.models import User
from common.choices import UserType
from .models import Employee, job_post
from django.contrib.auth.hashers import make_password

class PublicEmployeeRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Employee
        fields = ['name', 'email', 'password', 'confirm_password', 'company_name', "company_exp", "company_address", "company_size", "industry_type", "business_desc", "trade_number","rl_number","web_url"]
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
        
        #Model Fields
        company_exp = validated_data.get("company_exp", None)
        company_addrs= validated_data.get("company_address", None)
        company_size= validated_data.get("company_size", None)
        industry_type= validated_data.get("industry_type", None)
        business_desc= validated_data.get("business_desc", None)
        trade_number= validated_data.get("trade_number", None)
        rl_nmbr= validated_data.get("rl_number", None)
        web_url= validated_data.get("web_url", None)
        
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
                type=UserType.EMPLOYEE,
            )
            employee = Employee.objects.create(
                user=user,
                name=name,
                password=make_password(password),
                company_exp=company_exp,
                company_address=company_addrs,
                company_size=company_size,
                industry_type=industry_type,
                business_desc=business_desc,
                trade_number=trade_number,
                rl_number=rl_nmbr,
                web_url=web_url,
            )
            
            return employee

        except:
            raise serializers.ValidationError({"Error": ["Sorry, Registration failed!"]})
        
    def to_representation(self, instance):
        payload = {"message": f"Registration successful for {instance.name}."}
        return payload
    

class PublicEmployeeLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(max_length=228)
    class Meta:
        model = User
        fields = ["email", "password"]
        
class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'type']
    
class PrivateEmployeeProfileSerializer(serializers.ModelSerializer):
    user = PrivateUserSerializer()
    class Meta:
        model = Employee
        fields = ["uid","name", "user", "designation", "company_name", "company_exp", "company_address", "company_size", "industry_type", "business_desc", "trade_number", "rl_number", "web_url"]

class PrivateEmployeePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = job_post
        fields = "__all__"