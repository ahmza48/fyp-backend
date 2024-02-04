from django.urls import path
from .views import RegistrationView,LoginView,PasswordResetRequestView,PasswordResetConfirmView

# Login Endpoint: /api/auth/login/ -> done
# Password Reset Request Endpoint: /api/auth/password-reset/request/
# Password Reset Confirm Endpoint: /api/auth/password-reset/confirm/
# JWT Refresh Endpoint (Optional): /api/auth/token/refresh/
# Google Sign-Up/Login Endpoint: /api/auth/google/

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('password-reset/request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    # path('password-reset/confirm/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')


    # Add more endpoints as needed
]
