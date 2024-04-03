from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'phone', 'store_url', 'platform']
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_disallowed_fields(self, data, disallowed_fields):
        if any(field in data for field in disallowed_fields):
            disallowed = ', '.join(disallowed_fields)
            raise serializers.ValidationError(f"The following parameters are not allowed: {disallowed}")

    def validate(self, data):
        self.validate_disallowed_fields(data, ['store_url', 'platform'])
        return data
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'store_url', 'platform']
