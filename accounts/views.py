from django.core.mail import send_mail
from rest_framework.renderers import JSONRenderer
from django.utils import timezone
from django.conf import settings
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from .models import User, EmailVerificationToken, PasswordResetToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.contrib.sessions.models import Session
from django.contrib.auth.password_validation import validate_password
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from .serializers import ProfileSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

import secrets

def logout_all_sessions(user):
    sessions = Session.objects.all()

    for session in sessions:
        data = session.get_decoded()

        if data.get("_auth_user_id") == str(user.pk):
            session.delete()


def send_verification_email(user, token):
    verification_url = "http://localhost:8000/auth/verify-email/" + token + "/"
    send_mail(
        subject="Verify your email",
        message="Click this link to verify your email: " + verification_url,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    
def send_password_recovery_email(user,token):
    change_password_url = "http://localhost:8000/auth/change-password/" + token + "/"
    send_mail(
        subject="Change your password",
        message="Click this link to change your password: " + change_password_url,
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
        
        
class PasswordRecoveryLink(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        token = secrets.token_urlsafe(32)
        
        user = User.objects.filter(username=username, email=email).first()
        
        if user is None:
            return Response({"message": "No user with given username and email exists"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.account_status == User.AccountStatus.PENDING_VERIFICATION:
            return Response({"message": "Your email isn't verified"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        if user.account_status == User.AccountStatus.SUSPENDED:
            return Response({"message": "Your account has suspended"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        PasswordResetToken.objects.create(
            user=user,
            token=token
        )
        
        send_password_recovery_email(user,token)
        
        return Response({"message": "A password reset link has sent to your email"})
    
    
class PasswordChangeView(APIView):
    
    def get_renderers(self):
        if self.request.method == "POST":
            return [JSONRenderer()]
        return super().get_renderers()
    
    def get(self, request):
        pass
        
    def post(self, request, token): 
        password = request.data.get("password")
        if password is None:
            return Response({"Please give a password"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_column = PasswordResetToken.objects.filter(token = token).first()
        current_time = timezone.now()
        if token_column is None:
            return Response({"Invalid Password Reseting Link"}, status=status.HTTP_400_BAD_REQUEST)
            
        if token_column.expires_at > current_time:
            user = token_column.user
            validate_password(password, user=user)
            user.set_password(password)
            user.save(update_fields=["password"])
            return Response({"Your Password has successfully changed"})
            
        return Response({"Your Password Reset Link has expired"}, status=status.HTTP_410_GONE)
        
        
class EditProfileView(UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})
        
        
    
        
        