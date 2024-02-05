from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_email(self, value):
        # Check if the given email already exists.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    def create(self, validated_data):
        # user = User.objects.create_user(**validated_data)
        # return user
        try:
            # Extract password separately to set it securely.
            password = validated_data.pop('password', None)

            # Creating the user without saving to the database yet.
            user = User(**validated_data)

            # Set the password securely.
            if password:
                user.set_password(password)

            # Save the user to the database.
            user.save()
            return user
        except Exception as e:
            raise serializers.ValidationError(f"Error creating user: {str(e)}")