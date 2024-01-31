from django.contrib.auth.hashers import check_password

from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated

from .serializers import PublicApplicantRegistrationSerializer, PrivateApplicantProfileSerializer, PublicApplicantLoginSerializer
from accountio.models import User



class PublicUserRegistrationView(CreateAPIView):
    # queryset = Applicant.objects.all()
    serializer_class = PublicApplicantRegistrationSerializer
        
        
class PublicUserLoginView(CreateAPIView):
    serializer_class = PublicApplicantLoginSerializer

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



class PrivateApplicantProfile(RetrieveUpdateAPIView):
    serializer_class = PrivateApplicantProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get_object(self):
        applicant = self.request.user.applicant
        return applicant
        
        
        