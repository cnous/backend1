from django.urls import path, include
from . import views
#from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'api-v1'
urlpatterns = [
    #registration
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    path('test-email/', views.TestEmailSend.as_view(), name='test-mail'),

    #activation
    path('activation/confirm/<str:token>', views.ActivationApiView.as_view(), name = 'activation'),

    #resend activation
    path('activation/resend', views.ActivationResendApiView.as_view(), name='activation-resend'),

    #login token
    path('token/login/', views.CustomAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscordAuthToken.as_view(), name='token-logout'),

    #login jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

    #change password
    path('password-change/', views.ChangePasswordApiView.as_view(), name='change-password'),

    #reset password
    path('password-reset/', views.ResetPasswordApiView.as_view() , name='password-reset'),

    #Profile
    path('profile/', views.ProfileApiView.as_view(), name='profile'),


]