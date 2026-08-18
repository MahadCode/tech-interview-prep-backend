from django.core.mail import send_mail
from rest_framework.renderers import JSONRenderer
from django.utils import timezone
from django.conf import settings
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from .models import User, EmailVerificationToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated

import secrets

def send_verification_email(user, token):
    verification_url = "http://localhost:8000/auth/verify-email/" + token + "/"
    send_mail(
        subject="Verify your email",
        message="Click this link to verify your email: " + verification_url,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        token = secrets.token_urlsafe(32)

        EmailVerificationToken.objects.create(
            user=user,
            token=token
        )
        
        send_verification_email(user, token)

class EmailVerificationView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request, token):
        token_column = EmailVerificationToken.objects.filter(token = token).first()
        current_time = timezone.now()
        if token_column is None:
            return Response({"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        
        if  token_column.user.account_status ==  User.AccountStatus.ACTIVE:
            return Response({"Your Email has already verified"})
        
        if token_column.expires_at > current_time:
            token_column.user.account_status = User.AccountStatus.ACTIVE
            token_column.user.save()
            return Response({"Your Email has verified"})
        
        return Response({"Your Token has expired"}, status=status.HTTP_410_GONE)
        
class LoginView(APIView):
    
    def post(self, request):
        if request.user.is_authenticated:
            return Response({
                    "detail": "You are already Login"
            })
             
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        
        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response({
            "detail": "Login successful"
        })
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)  
        return Response({"message": "You are logout"}, status=status.HTTP_200_OK)
        
        
        
            
        
        