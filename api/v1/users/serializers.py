from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api.v1.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'password'
        )
        exclude = ('email',)



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        min_length=4,
        max_length=25,
        validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                    message='This username already exists')
        ]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(),
                                    message='This email already exists')]
    )

    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'password', 'email'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        user = CustomUser.objects.create_user(username, password=password, **validated_data)
        return user

    # If validate is set, then data (all passed fields) is accepted.
    # validate_<field> can be set (field as a serializer field).
    # Then data only accepts the value of this field from the request.
    def validate(self, data):
        """
        Validates and returns the password
        """
        user = CustomUser(**data)
        password = data.get('password', None)

        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            raise ValidationError({'password_error': e.messages})
        return super(RegisterUserSerializer, self).validate(data)


