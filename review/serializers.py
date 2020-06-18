from rest_framework import serializers
from .models import Review, Comment, User, Category, Genre, Title
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
import random, string, base64
from django.core.mail import send_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Avg


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
        if (email and User.objects.filter(email=email).exists()):
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        confirmation_code = encode(
            ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            )
        usename = email.replace('@','_').replace('.','_')
        user = User.objects.create(
            username=usename,
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


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    #rating = serializers.FloatField(source=Review.objects.filter(title=title.name).aggregate(Avg('score'))[score__avg])
    #category = CategorySerializer(read_only=True)
    #category = serializers.RelatedField(source='category', read_only=True)
    #category = serializers.CharField(source="category", read_only = True)
    category = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title
        
    def get_rating(self, title):
        scores = Review.objects.filter(title_id=title.id).aggregate(Avg('score'))
        if scores:
            rating = scores['score__avg']
            print(rating)
            return rating
        return None

    def get_category(self, title):
        print('тайтл',self.context['request'])
        category = Category.objects.filter(categories=title.id).values('name', 'slug')
        print('Категории', category)
        return category


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #title = serializers.ReadOnlyField(source='title_id')
    
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        #read_only_fields = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'text', 'created')#, 'review'
        model = Comment


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     following = serializers.CharField(source='following.username')

#     class Meta:
#         fields = ('id', 'user', 'following')
#         model = Follow


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     following = serializers.CharField(source='following.username')
#     class Meta:
#         fields = ('id', 'user', 'following')
#         model = Follow
       
#     def validate(self, data):
#         f = data['following']
#         following = get_object_or_404(User, username=f['username'])
#         user = self.context['request'].user
#         if not following:
#             raise serializers.ValidationError(f"Автор не найден {following}") 
#         if user == following:
#             raise serializers.ValidationError(f"Нельзя подписаться на самого себя") 
#         follows = Follow.objects.filter(user=user, following=following)
#         if follows:
#             raise serializers.ValidationError(f"Вы уже подписаны на автора {following}") 
#         data['following'] = following
#         data['user'] = user
#         return data
