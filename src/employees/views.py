from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate

from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import PublicEmployeeRegistrationSerializer, PrivateEmployeeProfileSerializer, PublicEmployeeLoginSerializer, PrivateEmployeePostSerializer
from accountio.models import User
from common.permissions import IsEmployeeUser
from .models import Employee, job_post


class PublicEmployeeRegistrationView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = PublicEmployeeRegistrationSerializer
        
class PublicEmployeeLogin(CreateAPIView):
    serializer_class = PublicEmployeeLoginSerializer

    def generate_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _email = serializer.validated_data['email']
        _password = serializer.validated_data['password']

        try:
            user = User.objects.get(email__iexact=_email)  # Case-insensitive email comparison

            if not check_password(_password, user.password):
                raise AuthenticationFailed()

            tokens = self.generate_tokens_for_user(user)

            return Response({'tokens': tokens, 'status': 'Login successful'}, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            raise AuthenticationFailed()
        
        
class PrivateEmployeeProfile(RetrieveUpdateAPIView):
    serializer_class = PrivateEmployeeProfileSerializer
    authentication_classes = [JWTAuthentication]
        
    def get_object(self):
        # Access the related Applicant object of the current user
        employee = self.request.user.employee
        return employee
    
    
class PrivateEmployeeposts(ListCreateAPIView):
    serializer_class = PrivateEmployeePostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    queryset = job_post.objects.all()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # This will create a new job_post object with the data from the request
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PrivateEmployeePostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateEmployeePostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    queryset = job_post.objects.all()
    
    def get_object(self):
        uid = self.kwargs.get("post_uid", None)
        
        return get_object_or_404(
            job_post.objects.filter(), uid=uid
        )

    

    
