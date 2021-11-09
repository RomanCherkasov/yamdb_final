from rest_framework import serializers
from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    role = serializers.CharField(max_length=128, default='user')

    class Meta:
        model = User
        fields = ('email', 'username', 'role')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'role',
                  'first_name',
                  'last_name',
                  'bio')
