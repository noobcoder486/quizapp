from rest_framework import serializers

from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user