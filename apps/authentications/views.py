from rest_framework import generics,permissions
from apps.basicusers.models import MidUser
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


class RegisterView(generics.CreateAPIView):
    queryset = MidUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)



class RequstPasswordResetEmail(generics.GenericAPIView):
    serializer_class=RequestPasswordEmailSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email=serializer.validated_data['email']
        user=MidUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        reset_url = request.build_absolute_uri(f"/api/auth/reset-password-confirm/{user.public_id}/{token}/")

        send_mail(
            subject="Reset Your Password",
            message=f"Click this link to reset your password: {reset_url}",
            from_email=None,
            recipient_list=[email]
        )

        return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, public_id, token):
        qs = MidUser.objects.filter(public_id=public_id)
        if qs.exists():
            user=qs.first()
            if not default_token_generator.check_token(user, token):
                return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                "detail": "Password reset successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

class LoginView(generics.CreateAPIView):
    queryset = MidUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"detail": "Username or password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user_id': user.public_id,
            'username': user.username,
            'email': user.email,
            'role': getattr(user, 'role', None),
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=LogoutSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


       

