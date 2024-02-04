from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode #this will be used to generate unique url for user
from django.utils.encoding import force_bytes, force_str
from .models import User
from django.core.mail import EmailMessage



# registration endpoint
class RegistrationView(generics.CreateAPIView):
    # defining which serializer class should we map to
    serializer_class = UserSerializer

    # Overriding the default create method of the view. If the data is valid, it calls perform_create to create the user.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# login endpoint
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # since we are using custom model class so we have to re-write authenticate function as per our needs
        user = authenticate(request, username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class PasswordResetRequestView(APIView):
    def post(self,request):
        # frontend pr check lga kr lazmi email send krni ha
        email=request.data.get('email')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExists:
            return Response({'error':'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # now that user is found who has to reset password so generate unique url that has user_id for this specific user

        # Generate a password reset token
        token = default_token_generator.make_token(user)

        # Build the reset URL
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request) #this will get url of current page/site where user currently is.
        reset_url = f'http://{current_site.domain}/password-reset/confirm/{uid}/{token}/'

        # Sending the reset email
        # Using Django's EmailMessage:
        message = EmailMessage('Password Reset', f'Click the link to reset your password: {reset_url}', to=[user.email])
        message.send()

        return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
        # email send hony k bad reset password ka form open hoga



class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token or user.'}, status=status.HTTP_400_BAD_REQUEST)            