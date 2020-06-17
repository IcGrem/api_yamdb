from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError
import random, string, base64
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from urllib.parse import quote


def encode(text):
    enc_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(enc_bytes)
    base64_enc = base64_bytes.decode('ascii')
    return base64_enc


def decode(text):
    base64_bytes = text.encode('ascii')
    text_bytes = base64.b64decode(base64_bytes)
    decoded_text = text_bytes.decode('ascii')
    return decoded_text


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def create(self, validated_data):
        email = validated_data['email']
        payload = email
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        confirmation_code = encode(
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            )
        user = User.objects.create(
            username=quote(payload),
            email=email,
            is_active=False,
            confirmation_code=confirmation_code
        )
        send_mail(
            'Ваш код подтверждения',
            confirmation_code,
            'from@example.com',
            [f'{user.email}'],
            fail_silently=False,
        )       
        return self.data['email']


class MyAuthTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ( 'email', 'confirmation_code')

    def validate(self, data):
        email = self.initial_data['email']
        confirmation_code = data['confirmation_code']
        user = User.objects.get(email=email)
        if confirmation_code == user.confirmation_code:
            user.is_active = True
            user.save()
            refresh = TokenObtainPairSerializer.get_token(user)
            del data['email']
            del data['confirmation_code']
            data['token'] = str(refresh.access_token)
            return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'bio', 'role')