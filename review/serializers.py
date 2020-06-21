from rest_framework import serializers
from .models import Review, Comment, User, Category, Genre, Title
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
import random, string, base64
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Avg
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
            username=email.replace('@', '_').replace('.', '_'),
            email=email,
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
        fields = ('email', 'confirmation_code')

    def validate(self, data):
        email = self.initial_data['email']
        confirmation_code = data['confirmation_code']
        user = User.objects.get(email=email)
        if confirmation_code == user.confirmation_code:
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


class CategorySerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    
    class Meta:
        fields = ('name', 'slug')
        model = Genre



class CustomSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return {'name': obj.name, 'slug': obj.slug}


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    category = CustomSlugRelatedField(queryset=Category.objects.all(), slug_field='slug')
    genre = CustomSlugRelatedField(queryset=Genre.objects.all(), slug_field='slug', many=True)
    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
    
    def get_rating(self, title):
        scores = Review.objects.filter(title_id=title.id).aggregate(Avg('score'))
        if scores:
            rating = scores['score__avg']
            print('рэйтинг -', rating)
            return rating
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #title = serializers.CharField(source='title.id', read_only=True)
    
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')#, 'title')
        model = Review
        #read_only_fields = ('title',)

    def validate(self, data):
        if int(self.initial_data['score']) not in range(1, 11):
            raise serializers.ValidationError(f"The score must be in range from 1 to 10")
        return data



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')#, 'review')
        model = Comment
        #read_only_fields = ('review',)

