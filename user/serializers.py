from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from .models import User


class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff',
                  'is_active', 'is_superuser', 'date_joined')


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class UserNestedSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
