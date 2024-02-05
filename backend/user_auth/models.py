from django.db import models
# from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.contrib.auth.hashers import make_password,check_password

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Hashed password will be stored
    first_name = models.CharField(max_length=255,blank=False)
    last_name = models.CharField(max_length=255,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False
    @property
    def is_authenticated(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return True


    def __str__(self):
        return self.first_name+' '+self.last_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # @staticmethod
    # def create_user(email, password, first_name, last_name):
    #     user = User(
    #         email=email,
    #         first_name=first_name,
    #         last_name=last_name
    #     )
    #     user.set_password(password)
    #     user.save()
    #     return user
