from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializer import (
    RegistrationSerilizer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendApiSerializer,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth import get_user_model
from ...models import Profile
from mail_templated import EmailMessage
from ..utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerilizer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email, "detail": "khosh gamlisiz"}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)

            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "a@a.com",
                to=[email],
            )
            # TODO: Add more useful commands here.
            EmailThread(email_obj).start()

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            # 'refresh': str(refresh),
            "access": str(refresh.access_token),
        }


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


# distroy
class CustomDiscordAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_pass")
            ):
                return Response(
                    {"old_pass": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_pass"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class TestEmailSend(generics.GenericAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        self.email = "sina@s.com"
        user_obj = get_object_or_404(User, email="sina@s.com")
        token = self.get_tokens_for_user(user_obj)

        email_obj = EmailMessage(
            "email/hello.tpl", {"token": token}, "a@a.com", to=["sina@s.com"]
        )
        # TODO: Add more useful commands here.
        EmailThread(email_obj).start()
        return Response("email sent")


class ActivationApiView(APIView):
    def post(self, request, token, *args, **kwargs):
        # decode -> token
        try:
            token = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            user_id = token.get("user_id")
        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                {"details": "token has been expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.InvalidTokenError:
            return Response(
                {"details": "token is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # find object user
        user_object = User.objects.get(pk=user_id)

        # is_verified

        if user_object.is_verified:
            return Response("your account has alredy been activated")
        user_object.is_verified == True
        user_object.save()

        # if token not valid

        # if token is valid
        return Response(
            {"detail": "your account has been created and activeted properly"}
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendApiSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendApiSerializer(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.validated_data["user"]
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "a@a.com",
                to=[user_obj.email],
            )
            # TODO: Add more useful commands here.
            EmailThread(email_obj).start()
            return Response(
                {"detail": "user activation resend successfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"detail": "request faild"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            # 'refresh': str(refresh),
            "access": str(refresh.access_token),
        }


class ResetPasswordApiView(generics.UpdateAPIView):
    model = User
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(
                serializer.data.get("old_pass")
            ):
                return Response(
                    {"old_pass": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_pass"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
